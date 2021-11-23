

##
def key_to_dict (key, dictionary):
	output = {}
	for raw in dictionary:
		raw = raw.strip()
		if raw.startswith(key + '["') and raw.endswith('"]'):
			arrlist = raw[len(key) + 2:-2].replace("::", "=").split('"]["')
			list_to_dict_path(arrlist, output, dictionary[raw])
	return output


##
def list_to_dict_path (list_items, output, terminal_value):
	current_item = list_items.pop(0)
	if current_item in output:
		if len(list_items) == 0:
			output[current_item] = terminal_value
		else:
			output[current_item] = list_to_dict_path(list_items, output[current_item], terminal_value)
	else:
		if len(list_items) == 0:
			output[current_item] = terminal_value
		else:
			output[current_item] = {}
			output[current_item] = list_to_dict_path(list_items, output[current_item], terminal_value)
	return output



##
g_file_cache = {}

def get_file_contents (filename):
	if filename not in g_file_cache:
		f = open(filename, "r")
		g_file_cache[filename] = f.read()
	
	return g_file_cache[filename]



##
g_build_log  = []

def log_icon_state (status, recipe, message = ""):
	g_build_log.append({
		"status": status,
		"context": recipe["context"],
		"name": recipe["name"],
		"size": recipe["size"],
		"message": message,
	})
	
	print("[" + status + "]", recipe["context"].ljust(12), recipe["name"].ljust(24), recipe["size"].ljust(8), message)