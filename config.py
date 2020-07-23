from os.path import realpath, dirname
import json

cfg_file_path = realpath(dirname(__file__) + "/config/config.json")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
statuspage = 'https://magicthegatheringarena.statuspage.io/'
rotation = 'https://whatsinstandard.com/api/v6/standard.json'
max_cards = 4

with open(cfg_file_path, "r+") as f:
	config = json.load(f)

# parse paths in config
config["database"]["path"] = realpath(dirname(__file__) 
				+ "/"
				+ config["database"]["path"])
