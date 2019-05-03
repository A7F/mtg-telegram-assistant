from os.path import realpath, dirname
import json

cfg_file_path = realpath(dirname(__file__) + "/config/config.json")

with open(cfg_file_path, "r+") as f:
	config = json.load(f)

# parse paths in config
config["database"]["path"] = realpath(dirname(__file__) 
				+ "/"
				+ config["database"]["path"])
