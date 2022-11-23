from flask import Flask
from flask import request
from werkzeug.exceptions import abort

import os
import json
from datetime import date

app = Flask(__name__)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY = "dev",
    # define the database folder
    DATABASE = "app/database"
)

def check_video_payload(payload):
    """
    Check payload format of video before processing the request.

    :return: error
    """
    error = None
    if not payload['title']:
        error = "Title is required."
    elif not payload['year']:
        error = "Year is required."
    elif not payload['director']['name']:
        error = "Director's name is required."
    elif not payload['director']['surname']:
        error = "Director's surname is required."
    for actor in payload['actors']:
        if not actor['name']:
            error = "Actor's name is required."
        elif not actor['surname']:
            error = "Actor's surname is required."
    return error

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
    Create/Retrieve/Delete a video library

    GET >
    :return 200: the video library requested
    :raise 404: if the video library was not found

    POST >
    :return 201: Success if created new video library
    :raise 400: if the request is malformated
    :raise 409: if the video library already exists
    :raise 500: if an error occurs when creating the new file

    DELETE >
    :return 204: Success if deleted the video library
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
            error = "Owner's name is required."
        elif not payload["owner"]["surname"]:
            error = "Owner's surname is required."

        if error is None:
            # Prepare content to write in the new file
            content = {
                "owner" : {"name": payload["owner"]["name"], "surname": payload["owner"]["surname"]},
                "last_modify": date.today().strftime("%d/%m/%Y"),
                "videos": []
                }
            try:
                with open(new_library, "x") as file:
                    json.dump(content, file)
                    return "Success", 201
            except FileExistsError as e:
                abort(409, e)
            except OSError as e:
                abort(500, e)
        else:
            abort(400, error)

    elif request.method == "DELETE":
        target_library = os.path.join(app.config["DATABASE"], library)+".json"
        try:
            os.remove(target_library)
            return "Success", 204
        except FileNotFoundError as e:
            abort(404, e)

@app.route('/library/<string:library>/video/<string:title>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def video_management(library,title):
    """
    Add/Retrieve/Update/Delete a video in a video library

    GET >
    :return 200: the video library requested
    :raise 404: if the video library was not found

    POST >
    :return 201: Success if correct created
    :raise 400: if the request is malformated
    :raise 409: if the video already exists
    :raise 500: if an error occurs during the edition of the file

    PUT >
    :return 204: Success if correct edited
    :raise 400: if the request is malformated
    :raise 400: if the request is malformated
    :raise 404: if the video library or the video was not found
    :raise 500: if an error occurs during the edition of the file

    DELETE >
    :return 204: Success if correct deleted
    :raise 404: if the video library or the video was not found
    :raise 500: if an error occurs during the edition of the file
    """
    if request.method == "GET":
        target_library = os.path.join(app.config["DATABASE"], library)+".json"
        # Check if the file exists in the database folder and if it is a file
        if os.path.isfile(target_library):
            try:
                with open(target_library, "r") as file:
                    content = json.load(file)
                    for video in content['videos']:
                        if video['title'] == title:
                            return json.dumps(video)
            except (OSError, json.decoder.JSONDecodeError) as e:
                abort(500, e)
        else:
            abort(404)

    elif request.method == "POST":
        target_library = os.path.join(app.config["DATABASE"], library)+".json"
        # Extract payload from POST's data
        try:
            payload = request.get_json()
        except json.decoder.JSONDecodeError as e:
            abort(400, e)
        error = check_video_payload(payload)

        if error is None:
            if os.path.isfile(target_library):
                try:
                    with open(target_library, "r") as file:
                        content = json.load(file)
                        for video in content['videos']:
                            if video['title'] == title:
                                abort(409, "The video already exists.")
                        content['videos'].append(payload)
                    with open(target_library, "w") as file:
                        content['last_modify'] = date.today().strftime("%d/%m/%Y")
                        json.dump(content, file)
                        return "Succes", 201
                except (OSError, json.decoder.JSONDecodeError) as e:
                    abort(500, e)
            else:
                abort(404, "The library does not exist.")
        else:
            abort(400, error)

    elif request.method == "PUT":
        target_library = os.path.join(app.config["DATABASE"], library)+".json"
        # Extract payload from POST's data
        try:
            payload = request.get_json()
        except json.decoder.JSONDecodeError as e:
            abort(400, e)
        error = check_video_payload(payload)

        if error is None:
            if os.path.isfile(target_library):
                try:
                    with open(target_library, "r") as file:
                        content = json.load(file)
                        find = False
                        for video in content['videos']:
                            if video['title'] == title:
                                find = True
                                content['videos'] = [payload if video['title'] == title else video for video in content['videos']]
                        if not find: abort(404, "The video does not exists.")
                    with open(target_library, "w") as file:
                        content['last_modify'] = date.today().strftime("%d/%m/%Y")
                        json.dump(content, file)
                        return "Succes", 204
                except (OSError, json.decoder.JSONDecodeError) as e:
                    abort(500, e)
            else:
                abort(404, "The library does not exist.")
        else:
            abort(400, error)

    elif request.method == "DELETE":
        target_library = os.path.join(app.config["DATABASE"], library)+".json"
        if os.path.isfile(target_library):
            try:
                with open(target_library, "r") as file:
                    content = json.load(file)
                    find = False
                    for video in content['videos']:
                        if video['title'] == title:
                            find = True
                            content['videos'].pop(content['videos'].index(video))
                if not find: abort(404, "The video does not exists.")
                with open(target_library, "w") as file:
                    content['last_modify'] = date.today().strftime("%d/%m/%Y")
                    json.dump(content, file)
                    return "Succes", 204
            except (OSError, json.decoder.JSONDecodeError) as e:
                abort(500, e)
        else:
            abort(404, "The library does not exist.")

@app.route('/library/<string:library>/by-name/<string:name>')
def search_by_name(library,name):
    """
    Search videos in a video library filter by name.

    :return: list of videos matching the search
    """
    target_library = os.path.join(app.config["DATABASE"], library)+".json"
    # Check if the file exists in the database folder and if it is a file
    if os.path.isfile(target_library):
        try:
            with open(target_library, "r") as file:
                content = json.load(file)
                match = []
                for video in content['videos']:
                    # Match without case sensitivity
                    if name.lower() in video['title'].lower(): match.append(video)
            # Return list of matches
            return json.dumps(match)
        except (OSError, json.decoder.JSONDecodeError) as e:
            abort(500, e)
    else:
        abort(404)

@app.route('/library/<string:library>/by-actor/<string:name>')
def search_by_actor(library,name):
    """
    Search videos in a video library filter by actor.

    :return: list of videos matching the search
    """
    target_library = os.path.join(app.config["DATABASE"], library)+".json"
    # Check if the file exists in the database folder and if it is a file
    if os.path.isfile(target_library):
        try:
            with open(target_library, "r") as file:
                content = json.load(file)
                match = []
                for video in content['videos']:
                    for actor in video['actors']:
                        # Match without case sensitivity
                        if any(name.lower() in info.lower() for info in [actor["name"], actor["surname"]]):
                            match.append(video)
            # Return list of matches
            return json.dumps(match)
        except (OSError, json.decoder.JSONDecodeError) as e:
            abort(500, e)
    else:
        abort(404)
