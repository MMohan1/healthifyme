from flask import Flask, request
import json
from config_parser import read_config
from controller import recipe_store, get_recipe_details, delete_recipe_details
import os
config_path = os.getcwd()
configFilePath = config_path + "/config.ini"
config_dict = read_config(configFilePath)
app = Flask(__name__)


@app.route('/recipe', methods=['GET', 'POST', "PUT", "DELETE"])
def recipe():
    if request.method == 'GET':
        name = request.args.get("recipe_name")
        if not name:
            {"success": False, "message": "Please provide recipe name"}
        data = get_recipe_details(name)
        return json.dumps(data)
    if request.method in ['POST', "PUT"]:
        incoming_request = json.loads(request.data)
        return recipe_store(incoming_request)
    if request.method == 'DELETE':
        name = request.args.get("recipe_name")
        if not name:
            {"success": False, "message": "Please provide recipe name"}
        data = delete_recipe_details(name)
        return json.dumps(data)
