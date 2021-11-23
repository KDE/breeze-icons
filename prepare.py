#!/usr/bin/python3

import os
import sys
import utilities as utils
import xml_soup as xml

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
export_path = os.getcwd() + "/export"
assets_path = os.getcwd() + "/assets"
config_path = os.getcwd() + "/config"


## Misc
file_cache = {}
tag_parser = "xml"
build_log  = []
singletons_loaded = []
namespaces = ["svg", "xml", "sodipodi", "inkscape"]


#
#
def run_prep (ini_path):
	config = configparser.ConfigParser(strict=False,delimiters=["="])
	config.optionxform=str
	config.read(ini_path)
	
	for s in config:
		if s == "DEFAULT":
			continue
		
		section=config[s]
		directory=os.path.join(os.getcwd(), s)
		prep_settings = {
			"master": section["master"] if "master" in section else "",
			"palettize": utils.key_to_dict("palettize", section),
			"destylize": utils.key_to_dict("destylize", section),
			"attribute": utils.key_to_dict("attribute", section),
		}
		
		if not os.path.isdir(directory):
			continue
		
		for file_path in os.listdir(directory):
			if not file_path.endswith(".svg"): 
				continue
			else:
				prep_file (os.path.join(os.getcwd(), s, file_path), prep_settings)


def prep_file (file_path, prep_settings):
	subject_src = utils.get_file_contents(file_path)
	subject_soup = BeautifulSoup(subject_src, tag_parser)
	
	print(file_path)
	
	if prep_settings["master"] != "":
		master_path = os.path.join(os.getcwd(), prep_settings["master"])
		
		if not os.path.isfile(master_path):
			print("[fail]", file_path, master_path)
			return False
		
		master_src = utils.get_file_contents(master_path)
		master_soup = BeautifulSoup(master_src, tag_parser)
		
		#master_soup.svg.attrs = subject_soup.svg.attrs
		
		if subject_soup.svg.has_attr("width"):
			master_soup.svg["width"] = subject_soup.svg["width"]
			
		if subject_soup.svg.has_attr("height"):
			master_soup.svg["height"] = subject_soup.svg["height"]
			
		if subject_soup.svg.has_attr("viewBox"):
			master_soup.svg["viewBox"] = subject_soup.svg["viewBox"]
		
		for tag in subject_soup.select("svg > :not(defs, namedview)"):
			master_soup.svg.append(tag)
		
		subject_soup = master_soup
		
		
	for tag in subject_soup.select("[style]"):
		xml.styles_to_attrs(tag)
	
	for tag in subject_soup.select("svg"):
		xml.remove_svg_viewbox(tag)
		
	for tag in subject_soup.select("svg :not(defs, namedview, rect#badge)"):
		xml.clean_attributes(tag)
		del tag["id"]
		del tag["color"]
		if tag.name != "g":
			tag["class"] = "ColorScheme-Background"
			tag["fill"] = "currentColor"
			tag["opacity"] = "0.6"
		else:
			del tag["opacity"]
		
	for tag in subject_soup.select("svg rect#badge"):
		tag["fill"] = "#FFCC00"
	
	
	for tag in subject_soup.select("xml"):
		subject_soup[tag].decompose()
	
	
	
	
	file_contents = subject_soup.prettify()
	#file_contents = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>' + "\n" + file_contents
	
	for ns in namespaces:
		file_contents = file_contents.replace("<" + ns + ":", "<").replace("</" + ns + ":", "</")
	
	with open(file_path, "w") as file_handle:
		file_handle.write(file_contents)

##
## Zhu Li, do the thing!
##
args = sys.argv
args.pop(0)

if len(args) == 0:
	print("Formatting all icons based on icon-prep.ini")
	run_prep(os.path.join(config_path, "icon-prep.ini"))
else:
	run_prep(os.path.join(config_path, "icon-prep.ini"), args[1])