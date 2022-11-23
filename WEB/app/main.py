from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

import requests
import json

app = Flask(__name__)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY="dev",
    # url of the API
    API_URL="http://rt0704-tp1-backend-1:8000",
)

def libs_list():
    """
    Retrieves the list of video libraries via an API request.

    :return: the list of available video libraries
    :raise 500: if an error occurs during the API request
    """
    libs = None
    try:
        r = requests.get(f"{app.config['API_URL']}/library")
        r.raise_for_status()
        libs = json.loads(r.text)
    except (requests.RequestException, json.decoder.JSONDecodeError) as e:
        abort(500, e)
    return libs

def get_lib(library):
    """
    Retrieves the content of a video library via an API request.

    :return: the content of the video library
    :raise 404: if the video library does not exist
    :raise 500: if an error occurs during the API request
    """
    decoded_lib = None
    try:
        # request the contents of the library at the API
        r = requests.get(f"{app.config['API_URL']}/library/{library}")
        r.raise_for_status()
        decoded_lib = json.loads(r.text)
    except requests.HTTPError as e:
        abort(404, "The video library does not exist.") if r.status_code == 404 else abort(500, e)
    except (requests.RequestException, json.decoder.JSONDecodeError) as e:
        abort(500, e)
    return decoded_lib

def check_video_format():
    """
    Check the format of the video form.

    :return: the formatted payload and the state of the error variable
    """
    title = request.form["title"]
    year = request.form["year"]
    director_name = request.form["director_name"]
    director_surname = request.form["director_surname"]
    actor1_name = request.form["actor1_name"]
    actor1_surname = request.form["actor1_surname"]
    actor2_name = request.form["actor2_name"]
    actor2_surname = request.form["actor2_surname"]
    actor3_name = request.form["actor3_name"]
    actor3_surname = request.form["actor3_surname"]
    payload = None
    error = None

    if not title:
        error = "Title is required."
    elif not year:
        error = "Year is required."
    elif not director_name:
        error = "Director's name is required."
    elif not director_surname:
        error = "Director's surname is required."
    elif not actor1_name:
        error = "Actor 1's name is required."
    elif not actor1_surname:
        error = "Actor 1's surname is required."
    elif not actor2_name:
        error = "Actor 2's name is required."
    elif not actor2_surname:
        error = "Actor 2's surname is required."
    elif not actor3_name:
        error = "Actor 3's name is required."
    elif not actor3_surname:
        error = "Actor 3's surname is required."

    if "/" in title:
        error = "The character '/' is not allowed in the title field."

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

    return (payload, error)

# Video library section

@app.route("/")
def index():
    """List of available video libraries."""
    return render_template("index.html", libs=libs_list())

@app.route("/new-library", methods=["GET", "POST"])
def new_library():
    """Create a new video library."""
    if request.method == "POST":
        name = request.form["name"]
        owner_name = request.form["owner_name"]
        owner_surname = request.form["owner_surname"]
        error = None

        if not name:
            error = "Name is required."
        elif not owner_name:
            error = "Owner's name is required."
        elif not owner_surname:
            error = "Owner's surname is required."

        if error is None:
            payload = {'name': name, 'owner': {'name': owner_name, 'surname': owner_surname}}
            try:
                # request the API to create a new video library
                r = requests.post(f"{app.config['API_URL']}/library/{name}", json=payload)
                r.raise_for_status()
            except requests.HTTPError as e:
                error = "The video library already exists." if r.status_code == 409 else abort(500, e)
            except requests.RequestException as e:
                abort(500, e)

        if error is None:
            flash("Successful creation of the video library.")
        else:
            flash(error)

    return render_template("library/new.html")

@app.route("/library/<string:library>")
def show_library(library):
    """Display the list of videos in a video library."""
    return render_template("library/show.html", library=library, content=get_lib(library))

@app.route("/library/<string:library>/settings")
def settings(library):
    """Manage a video library."""
    return render_template("library/settings.html", library=library, content=get_lib(library))

@app.route("/library/<string:library>/settings/delete", methods=["POST"])
def delete_library(library):
    """Delete a video library."""
    try:
        # request the API to delete video library's file
        r = requests.delete(f"{app.config['API_URL']}/library/{library}")
        r.raise_for_status()
        return redirect(url_for("index"))
    except requests.HTTPError as e:
        abort(404, "The video library does not exist.") if r.status_code == 404 else abort(500, e)
    except requests.RequestException as e:
        abort(500, e)

# Video section

@app.route("/new-video", methods=["GET", "POST"])
def new_video():
    """Add a new video to a video library."""
    if request.method == "POST":
        payload, error = check_video_format()
        library = request.form["library"]
        if not library:
            error = "Library is required."

        if error is None:
            try:
                # request the API to add a new video to a video library
                r = requests.post(f"{app.config['API_URL']}/library/{library}/video/{payload['title']}", json=payload)
                r.raise_for_status()
            except requests.HTTPError as e:
                error = "The video already exists." if r.status_code == 409 else abort(500, e)
            except requests.RequestException as e:
                abort(500, e)

        if error is None:
            flash("Successful addition of the video to the video library.")
        else:
            flash(error)

    return render_template("library/video/new.html", libs=libs_list())

@app.route("/library/<string:library>/video/<video_id>/update", methods=["GET", "POST"])
def update_video(library,video_id):
    """Update a video in a video library."""
    decoded_video = None
    try:
        # request the API video information
        r = requests.get(f"{app.config['API_URL']}/library/{library}/video/{video_id}")
        r.raise_for_status()
        decoded_video = json.loads(r.text)
    except requests.HTTPError as e:
        abort(404, "The video does not exist.") if r.status_code == 404 else abort(500, e)
    except (requests.RequestException, json.decoder.JSONDecodeError) as e:
        abort(500, e)

    if request.method == "POST":
        payload, error = check_video_format()

        if error is None:
            try:
                # request the API to update the video in the video library
                r = requests.put(f"{app.config['API_URL']}/library/{library}/video/{video_id}", json=payload)
                r.raise_for_status()
            except requests.RequestException as e:
                abort(500, e)

            return redirect(url_for("settings", library=library))
        else:
            flash(error)

    return render_template("library/video/update.html", library=library, video=decoded_video)

@app.route("/library/<string:library>/video/<video_id>/delete", methods=["POST"])
def delete_video(library,video_id):
    """Delete a video in a video library."""
    try:
        r = requests.delete(f"{app.config['API_URL']}/library/{library}/video/{video_id}")
    except requests.HTTPError as e:
        abort(404, f"The video does not exist.") if r.status_code == 404 else abort(500, e)
    except requests.RequestException as e:
        abort(500, e)

    return redirect(url_for("settings", library=library))

# Search section

@app.route("/search")
def search_video():
    """Search for a video in a video library by name or by actor."""
    error = None

    # check if all the required arguments are correctly defined in the search.
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

        if error is None:
            try:
                match type:
                    case "title":
                        r = requests.get(f"{app.config['API_URL']}/library/{lib}/by-name/{name}")
                        r.raise_for_status()
                    case "actor":
                        r = requests.get(f"{app.config['API_URL']}/library/{lib}/by-actor/{name}")
                        r.raise_for_status()
                    case _:
                        error = "Unknown search type."
            except requests.HTTPError as e:
                abort(404, "The video library does not exist.") if r.status_code == 404 else abort(500, e)
            except requests.RequestException as e:
                abort(500, e)

            if error is None:
                try:
                    result = json.loads(r.text)
                except json.decoder.JSONDecodeError as e:
                    abort(500, e)
                return render_template("search/result.html", result=result)

    return render_template("search/search.html", libs=libs_list(), error=error)
