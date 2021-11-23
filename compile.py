#!/usr/bin/python3

"""
SPDX-License-Identifier: LGPL-2.1-only OR LGPL-3.0-only OR LicenseRef-KDE-Accepted-LGPL
SPDX-FileCopyrightText: 2021 Ken Vermette <vermette@gmail.com>
"""

import os
import sys
import utilities as utils
import xml_soup as xml

"""
Builds icons from src assets using specifications from cookbook.ini files
"""



has_imports = True;

try:
	import configparser
except ImportError:
	print("ConfigParser library required. Run \"pip install configparser\" to correct this issue.")
	has_imports = False

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
else:
	print("Note: If you have a version of BeautifulSoup lower than 4.7.0 this tool will not work correctly.")

## Paths
export_path    = os.getcwd() + "/build"
assets_path    = os.getcwd() + "/assets"
masters_path   = assets_path + "/masters"
template_path  = assets_path + "/templates"
cookbooks_path = os.getcwd() + "/cookbooks"


## Misc
tag_parser = "xml"
build_log  = []
singletons_loaded = []
namespaces = ["svg", "xml", "sodipodi", "inkscape"]
g_colors = {"foo":"bar"}


## Run one individual cookbook
def run_cookbook(path):
	global g_colors
	print("\nOpening Cookbook \"" + f + "\"\n")
	parser = configparser.ConfigParser(strict=False,delimiters=["="])
	parser.optionxform=str
	parser.read(path)
	
	settings = parser._sections["Cookbook"];
	sizes    = settings["sizes"].split(",") if "sizes" in settings else []
	context  = settings["context"] if "context" in settings else "Generic"
	folder   = settings["folder"] if "folder" in settings else "generic"
	g_colors = parser._sections["CookbookColors"] if "CookbookColors" in parser._sections else {}
	global_recipe = parser._sections["GlobalRecipes"] if "GlobalRecipes" in parser._sections else {}
	global_mixins = {
		"classes": extract_subvalue("classes", global_recipe),
		"replacements": extract_subvalue("replace", global_recipe),
	}
	
	if "Cookbook" in parser:
		del parser["Cookbook"]
		
	if "GlobalRecipes" in parser:
		del parser["GlobalRecipes"]
		
	if "CookbookColors" in parser:
		del parser["CookbookColors"]
	
	for section in parser.sections():
		icon = parser[section]
		
		for size in sizes:
			recipe = {
				"name": section,
				"context": folder,
				"size": size,
				"template": icon["template"] if "template" in icon else "undefined",
				"aliases": icon["aliases"].split(",") if "aliases" in icon else [],
				"classes": extract_subvalue("classes", icon),
				"attrs": utils.key_to_dict("attr", icon),
				"replacements": extract_subvalue("replace", icon),
			}
			
			build_result = build_recipe(recipe, global_mixins)
			
			# If the build failed stop here so we don't write garbage files
			if build_result == False:
				continue
			
			file_contents = build_result.prettify()
			file_dir = os.path.join(export_path, folder, size)
			file_dest = os.path.join(file_dir, section + ".svg")
			
			file_contents = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>' + "\n" + file_contents
			
			for ns in namespaces:
				file_contents = file_contents.replace("<" + ns + ":", "<").replace("</" + ns + ":", "</")
			
			if not os.path.exists(file_dir):
				os.makedirs(file_dir)
				
			with open(file_dest, "w") as file_handle:
				file_handle.write(file_contents)
			
			#recipe["aliases"].append(section + ".gen")
			
			for alias in recipe["aliases"]:
				alias_name = alias.strip()
				alias_path = os.path.join(file_dir, alias_name + ".svg")
				alias_target = section + ".svg"
				
				if alias_name == "":
					continue
				if os.path.isfile(alias_path):
					if os.path.islink(alias_path) and os.readlink(alias_path) != alias_target:
						os.remove(alias_path)
					elif os.path.islink(alias_path):
						#log_icon_state("done", recipe, "Alias " + alias_name)
						continue
					else:
						#log_icon_state("skip", recipe, "Alias not created: " + alias_name + " is a real file")
						continue
				
				#log_icon_state("done", recipe, "Alias " + alias_name)
				os.symlink(alias_target, alias_path)
	#print(build_log)


## Build an icon
def build_recipe (recipe, mixins):
	mas_path = os.path.join(masters_path, "master." + recipe["size"] + ".svg")
	tpl_path = os.path.join(template_path, recipe["template"] + "." + recipe["size"] + ".svg")
	
	if not os.path.isfile(mas_path):
		log_icon_state("fail", recipe, "Missing master: " + mas_path)
		return False
	
	if not os.path.isfile(tpl_path):
		log_icon_state("fail", recipe, "Missing base template: " + tpl_path)
		return False
	
	master_src = utils.get_file_contents(mas_path)
	template_src = utils.get_file_contents(tpl_path)
	
	soup = BeautifulSoup(master_src, tag_parser)
	template_soup = BeautifulSoup(template_src, tag_parser)
	
	for contents in soup.select("#content"):
		xml.merge_singleton_tag("defs", template_soup, soup, tpl_path)
		contents.replace_with(xml.select_to_g("svg > *:not(defs)", template_soup, "content"))
	
	for target in recipe["replacements"]:
		soup = xml.do_positioned_replacement(target, recipe["replacements"][target], soup, recipe)
		if not soup:
			return False
	
	for selector in recipe["classes"]:
		soup = xml.select_class_mod(selector, recipe["classes"][selector], soup)
	
	
	for selector in recipe["attrs"]:
		for tag in soup.select(selector):
			for attr_key in recipe["attrs"][selector]:
				attr_value = recipe["attrs"][selector][attr_key]
				tag[attr_key] = string_alias(attr_value)
	
	
	xml.clean_classes(soup)
	log_icon_state("done", recipe)
	return soup.svg


def string_alias (selector):
	global g_colors
	selector = selector.strip("\"' \t\n\r")
	if selector.startswith("@") and selector[1:] in g_colors:
		return g_colors[selector[1:]].strip("\"' \t\n\r")
	return selector


def log_icon_state (status, recipe, message = ""):
	build_log.append({
		"status": status,
		"context": recipe["context"],
		"name": recipe["name"],
		"size": recipe["size"],
		"message": message,
	})
	
	#print("[" + status + "]", recipe["context"].ljust(12), recipe["name"].ljust(24), recipe["size"].ljust(8), message)
	
	icon_label_len = 24
	
	if len(recipe["name"]) > icon_label_len:
		recipe["name"] = recipe["name"][0:icon_label_len - 3] + "..."
	
	print("[" + status + "]", recipe["name"].ljust(icon_label_len), recipe["size"].ljust(6), message)


##
def validate_str_list (string):
		if isinstance(string, str):
			return string.split()
		else:
			return string


##
def extract_subvalue (key, dictionary):
	output = {}
	for raw in dictionary:
		if raw.startswith(key + '["') and raw.endswith('"]'):
			newkey = raw.replace(key + '["',"").replace('"]',"")
			output[newkey] = dictionary[raw].strip("\"' \t\n\r")
	return output


## 
def position_to_offset (position):
	if position == "left" or position == "top":
		return -1
	elif position == "center":
		return 0
	elif position == "right" or position == "bottom":
		return -1
	return position


##
def log_icon (icon, sizes, state, text):
	pass


##
## Zhu Li, do the thing!
##
cookbooks = sys.argv
cookbooks.pop(0)

if len(cookbooks) == 0:
	print("Looking for all cookbooks in the /cookbooks folder")
	for f in os.listdir(cookbooks_path):
		if f.endswith(".cookbook"):
			run_cookbook(os.path.join(cookbooks_path, f))
else:
	for f in cookbooks:
		if os.path.isfile(os.path.join(os.getcwd(), f)):
			run_cookbook(os.path.join(os.getcwd(), f))
		else:
			print("File not found: \"" + f + '"')