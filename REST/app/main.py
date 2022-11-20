from flask import Flask
from flask import request
from flask import json
from werkzeug.exceptions import abort

import os
from datetime import date

app = Flask(__name__)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY = "dev",
    # define the database folder
    DATABASE = "app/database"
)

# List video libraries
@app.route('/library')
def library_list():
    """
    List library files in database folder.

    :return: list of available video libraries
    """
    res = []
    for path in os.listdir(path=app.config["DATABASE"]):
        # Check if the current path exists and if it is a file
        if os.path.isfile(os.path.join(app.config["DATABASE"], path)):
            res.append(os.path.splitext(path)[0])
    return(json.dumps(res))

@app.route('/library/<string:library>', methods=['GET', 'POST', 'DELETE'])
def library_management(library):
    """
    Create/Return/Delete a video library

    GET >
    :return: the video library requested
    :raise 404: if the video library was not found

    POST >
    :return: acknolegement of creation video libraries
    :raise 400: if the request is malformated
    :raise 409: if the video library already exists
    :raise 500: if an error occurs when creating the new file

    DELETE >
    :return: list of available video libraries
    :raise 503: if an error occurs during the request to the api
    """
    if request.method == "GET":
        target_library = os.path.join(app.config["DATABASE"], library)+".json"
        # Check if the file exists in the database folder and if it is a file
        if os.path.isfile(target_library):
            with open(target_library, "r") as file:
                return json.dumps(json.load(file))
        else:
            abort(404)

    elif request.method == "POST":
        new_library = os.path.join(app.config["DATABASE"], library)+".json"
        error = None

        # Extract payload from POST's data
        try:
            payload = request.get_json()
        except json.decoder.JSONDecodeError as e:
            abort(400, e)

        if not payload["name"]:
            error = "Name is required."
        elif not payload["owner"]["name"]:
            error = "Owner: Name is required."
        elif not payload["owner"]["surname"]:
            error = "Owner: Surname is required."

        if error is None:
            # Prepare content to write in the new file
            content = {
                "owner" : {"name": payload["owner"]["name"], "surname": payload["owner"]["surname"]},
                "last_modify": date.today().strftime("%d/%m/%Y")
                }
            try:
                with open(new_library, "x") as file:
                    json.dump(content, file)
                    return "Success"
            except FileExistsError as e:
                abort(409, e)
            except OSError as e:
                abort(500, e)
        else:
            abort(400, error)

    elif request.method == "DELETE":
        pass

# - Create parametres
#   - Nom du fichier
#   - Proprietaire
# - Creation de la liste des films vide

# - Delete parametres
#   - Nom du fichier
# - Destruction du fichier

# Add/Edit/Delete a video
@app.route('/library/<string:library>/video/<string:title>', methods=['POST', 'PUT', 'DELETE'])
def video_management(library,title):
    return "soon"

# Search film in video library
@app.route('/library/<string:library>/by-name/<string:name>')
def search_by_name(library,name):
    return "soon"

# /search/name/Pulp+Fiction

# Search for films by an actor in video library
@app.route('/library/<string:library>/by-actor/<string:name>')
def search_by_actor(library,name):
    return "soon"
