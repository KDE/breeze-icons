
import os
import utilities as utils

has_imports = True
singletons_loaded = []
tag_parser = "xml"

# TODO: Get rid of this.
assets_path    = os.getcwd() + "/assets"

try:
	from lxml import etree
except ImportError:
	print("LXML library required. Run \"pip install lxml\" to correct this issue.")
	has_imports = False

try:
	from bs4 import BeautifulSoup
except ImportError:
	print("BeautifulSoup library required. Run \"pip install beautifulsoup4\" to correct this issue.")
	has_imports = False

if not has_imports:
	print("One of more libraries are missing, please install them to continue.")
	exit()

def do_positioned_replacement(target_selector, replacement, soup, recipe):
	rep_spec = replacement.split(",")
	selector = "rect" + target_selector
	rep_base = rep_spec[0].strip()
	rep_align = rep_spec[1].strip() if len(rep_spec) > 1 else "center"
	
	if rep_align not in ["top", "center", "middle", "bottom"]:
		utils.log_icon_state("warn", recipe, "Unknown vertical alignment " + rep_align)
		rep_align = "center"
	
	for t in soup.select(selector):
		pos_x = t["x"] if t.has_attr("x") else "0"
		pos_y = t["y"] if t.has_attr("y") else "0"
		size_w = t["width"] if t.has_attr("width") else 2
		size_h = t["height"] if t.has_attr("height") else 2
		tag_id = t["id"] if t.has_attr("id") else ""
		rep_path = os.path.join(assets_path, rep_base + "." + size_w + ".svg")
		
		if not os.path.isfile(rep_path):
			utils.log_icon_state("fail", recipe, "Missing component: " + rep_base + "." + size_w + ".svg @" + size_w + "x" + size_h)
			return False
		
		rep_src = utils.get_file_contents(rep_path)
		rep_soup = BeautifulSoup(rep_src, tag_parser)
		
		# The width and heigh of the SVG should be set.
		# TODO Maybe have it fall-back to the viewbox if not present?
		rep_w = t["width"] if rep_soup.svg.has_attr("width") else size_w
		rep_h = t["height"] if rep_soup.svg.has_attr("height") else size_h
		offset_x = int(pos_x)
		offset_y = int(pos_y)
		
		if rep_align == "top":
			pass
		elif rep_align == "bottom":
			offset_y += int(size_h) - int(rep_h)
		elif rep_align in ["middle", "center"]:
			offset_y += round((int(size_h) - int(rep_h)) / 2)
		
		attr_transform = 'transform="translate(' + str(offset_x) + ',' + str(offset_y) + ')"'
		group_tag = "<g " + attr_transform + "></g>"
		
		if tag_id != "":
			group_tag = "<g id=\"" + tag_id + "\" " + attr_transform + "></g>"
		
		insert_soup = BeautifulSoup(group_tag, tag_parser)
		
		for tag in rep_soup.select("svg > *:not(defs, namedview)"):
			insert_soup.g.append(tag)
			
		t.replace_with(insert_soup)
	
	return soup


##
def select_to_g (selector, soup, group_id = ""):
	group_tag = "<g></g>"
	
	if group_id != "":
		group_tag = "<g id=\"" + group_id + "\"></g>"
	
	insert_soup = BeautifulSoup(group_tag, tag_parser)
	
	for tag in soup.select(selector):
		insert_soup.g.append(tag)
		
	return insert_soup


##
def select_class_mod (selector, modifications, soup):
	mods = modifications.split(",")
	
	for tag in soup.select(selector):
		if not tag.has_attr("class"):
			tag["class"] = []
		for mod in mods:
			mod = mod.strip(" \n\t\r")
			mod_base_class = mod.strip("-")
			classes = validate_str_list(tag["class"])
			if mod.startswith("-"):
				if mod_base_class in tag["class"]:
					classes.remove(mod_base_class)
			elif mod_base_class not in classes:
				classes.append(mod)
			tag["class"] = classes
	
	return soup


##
def styles_to_attrs (soup):
	css = {}
	
	if not soup.has_attr("style"):
		return
	
	styles = soup["style"].split(";")
	
	for style in styles:
		style = style.split(":")
		soup[style[0].strip()] = style[1].strip()
	
	del soup["style"]


##
def clean_classes (soup):
	for tag in soup.select("[class]"):
		classes = validate_str_list(tag["class"])
		for i in range(len(classes)):
			classes[i] = classes[i].replace("-Placeholder", "").replace("-placeholder", "")
		if len(classes) == 0:
			del tag["class"]
		else:
			tag["class"] = " ".join(classes)


##
def clean_attributes (soup):
	del soup["stroke"]
	del soup["stroke-style"]
	del soup["stroke-width"]
	del soup["fill-opacity"]
	del soup["sodipodi:nodetypes"]
	del soup["-inkscape-stroke"]


##
def remove_svg_viewbox (soup):
	viewbox = ["0","0","1","1"]
	
	if soup.has_attr("viewBox"):
		viewbox = soup["viewBox"].split(" ")
	
	if not soup.has_attr("width"):
		soup["width"] = viewbox[2]
		
	if not soup.has_attr("height"):
		soup["height"] = viewbox[3]
	
	


## If a singleton tag has already been loaded into the icon,
## this function will not load it in a second time to avoid
## duplicating id-less tags
def merge_singleton_tag (tag, soup_from, soup_to, from_path):
	#if from_path + "::" + tag in singletons_loaded:
	#	return
	
	singletons_loaded.append(from_path + "::" + tag)
	
	from_single  = soup_from.find(tag)
	to_single    = soup_to.find(tag)
	reserved_ids = []
	
	for reserved in soup_to.select(tag + " > [id]"):
		reserved_ids.append(reserved["id"])
	
	for t in soup_from.select(tag + " > *"):
		if t.has_attr("id") and t["id"] != "":
			if t["id"] not in reserved_ids:
				to_single.append(t)
		else:
			to_single.append(t)


##
def validate_str_list (string):
		if isinstance(string, str):
			return string.split()
		else:
			return string