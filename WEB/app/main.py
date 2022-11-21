from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import json
from werkzeug.exceptions import abort

import requests
import sys

app = Flask(__name__)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY="dev",
    # define the api url
    API_URL="http://rt0704-tp1-backend-1:8000",
)

def get_libs():
    """
    Retrieves the list of video libraries via an api request.

    :return: list of video libraries
    :raise 500: if an error occurs during the request to the api
    """
    try:
        r = requests.get(f"{app.config['API_URL']}/library")
        r.raise_for_status()
        libs = json.loads(r.text)
    except (requests.RequestException, json.decoder.JSONDecodeError) as e:
        abort(500, e)
    return (libs)

@app.route("/")
def index():
    """List of available video libraries"""
    libs = get_libs()
    return render_template("index.html", libs=libs)

@app.route("/new-library", methods=["GET", "POST"])
def new_library():
    """Create a new library."""
    if request.method == "POST":
        name = request.form["name"]
        owner_name = request.form["owner_name"]
        owner_surname = request.form["owner_surname"]
        error = None

        if not name:
            error = "Name is required."
        elif not owner_name:
            error = "Owner: Name is required."
        elif not owner_surname:
            error = "Owner: Surname is required."

        if error is None:
            payload = {'name': name, 'owner': {'name': owner_name, 'surname': owner_surname}}
            try:
                # Request the api to create a new video library
                r = requests.post(f"{app.config['API_URL']}/library/{name}", json=payload)
                r.raise_for_status()
            except requests.HTTPError as e:
                if r.status_code == 409:
                    error = "The video library already exists."
                else:
                    abort(500, e)
            except requests.RequestException as e:
                abort(500, e)

        if error is None:
            flash("Successfully created video library")
        else:
            flash(error)

    return render_template("library/new.html")

# Display films in video library
@app.route("/library/<string:library>")
def show_library(library):
    decoded_lib = None
    error = None

    try:
        # Retrieve library content
        r = requests.get(f"{app.config['API_URL']}/library/{library}")
        r.raise_for_status()
        decoded_lib = json.loads(r.text)
    except requests.HTTPError as e:
        if r.status_code == 404:
            error = "The video library does not exist."
        else:
            abort(500, e)
    except (requests.RequestException, json.decoder.JSONDecodeError) as e:
        abort(500, e)

    return render_template("library/show.html", lib=decoded_lib, error=error)

# Manage a video library based on the existence of a library (else abort(403) or error)
@app.route("/library/<string:library>/settings")
def settings(library):
    return render_template("library/edit.html")

# Manage a video library based on the existence of a library (else abort(403) or error)
@app.route("/library/<string:library>/settings/delete", methods=["GET"]) #methods=["POST"] ???
def delete_library(library):
    try:
        # Delete library
        r = requests.delete(f"{app.config['API_URL']}/library/{library}")
        r.raise_for_status()
        return "Succes"
    except requests.HTTPError as e:
        if r.status_code == 404:
            abort(404, f"The video library doesn't exist.")
        else:
            abort(400, e)
    except requests.RequestException as e:
        abort(500, e)

@app.route("/new-video", methods=["GET", "POST"])
def new_video():
    """Add a new video in a video library."""
    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        director = request.form["director"]
        actor1_name = request.form["actor1_name"]
        actor1_surname = request.form["actor1_surname"]
        actor2_name = request.form["actor2_name"]
        actor2_surname = request.form["actor2_surname"]
        actor3_name = request.form["actor3_name"]
        actor3_surname = request.form["actor3_surname"]
        library = request.form["library"]
        error = None

        if not title:
            error = "Title is required."
        elif not year:
            error = "Year is required."
        elif not director_name:
            error = "Director: Name is required."
        elif not director_surname:
            error = "Director: Surname is required."
        elif not actor1_name:
            error = "Actor 1: Name is required."
        elif not actor1_surname:
            error = "Actor 1: Surname is required."
        elif not actor2_name:
            error = "Actor 2: Name is required."
        elif not actor2_surname:
            error = "Actor 2: Surname is required."
        elif not actor3_name:
            error = "Actor 3: Name is required."
        elif not actor3_surname:
            error = "Actor 3: Surname is required."
        elif not library:
            error = "Library is required."

        if error is None:
            payload = {
                'title': title,
                'year': year,
                'director': {'name': director_name, 'surname': director_surname},
                'actors': [
                    {'name': actor1_name, 'surname': actor1_surname},
                    {'name': actor2_name, 'surname': actor2_surname},
                    {'name': actor3_name, 'surname': actor3_surname}
                ]}

            try:
                # Request the api to add a new video in a video library
                r = requests.post(f"{app.config['API_URL']}/library/{library}/video/{title}", json=payload)
                r.raise_for_status()
            except requests.HTTPError as e:
                if r.status_code == 409:
                    error = "The video already exists."
                else:
                    abort(500, e)
            except requests.RequestException as e:
                abort(500, e)

        if error is None:
            flash("Successfully add video in the video library")
        else:
            flash(error)

    return render_template("library/video/new.html", libs=get_libs())

# Edit a video
@app.route("/library/<string:library>/video/<video_id>/edit", methods=["GET", "POST"])
def edit_video(library,video_id):
    return render_template("library/video/edit.html")

# Delete a video
@app.route("/library/<string:library>/video/<video_id>/delete", methods=["POST"])
def delete_video(library,video_id):
    try:
        # Delete library
        r = requests.post(f"{app.config['API_URL']}/library/")
    except requests.HTTPError as e:
        print(e, file=sys.stderr)
        if r.status_code == 404:
            abort(404, f"The video library doesn't exist.")
    except requests.RequestException as e:
        print(e, file=sys.stderr)

    return redirect(url_for(f"library.{library}.settings"))

@app.route("/search")
def search_video():
    """Search for a video in a video library by name or by actor."""
    error = None

    # Check if all required arguments are defined in the search.
    if all(arg in request.args for arg in ["name", "type", "lib"]):
        name = request.args["name"]
        type = request.args["type"]
        lib = request.args["lib"]

        if not name:
            error = "Name is required."
        elif not type:
            error = "Type is required."
        elif not lib:
            error = "Library is required."

        # raise error if lib is not in libs ? get_libs on top of function ?
        # libs = get_libs()
        # if lib not in libs:
        #     error = "This video library does not exist."
        # Manage by try  ... except (below)

        if error is None:
            try:
                match type:
                    case "title":
                        r = requests.get(f"{app.config['API_URL']}/library/{lib}/by-name/{name}")
                        r.raise_for_status()
                        return "Succes"
                    case "actor":
                        r = requests.get(f"{app.config['API_URL']}/library/{lib}/by-actor/{name}")
                        r.raise_for_status()
                        return "Succes"
                    case _:
                        error = "Unknown search type."
            except requests.HTTPError as e:
                if r.status_code == 404:
                    abort(404, f"The video library doesn't exist.")
                else:
                    abort(400, e)
            except requests.RequestException as e:
                abort(500, e)

            if error is None:
                result = json.loads(r.text)
                return result
                return render_template("search/result.html", result=result)

    return render_template("search/search.html", libs=get_libs(), error=error)
