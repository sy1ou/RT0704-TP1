from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

import requests
import sys
import json

app = Flask(__name__)

url_site = "http://rt0704-tp1-backend-1:8000"

## Library management

# Find video library
@app.route('/')
def index():
    error = None
    libs = []

    # Check if a library video exist
    try:
        # Search a library video
        r = requests.get(f"{url_site}/library")
        libs = json.loads(r.text)
    except requests.RequestException as error:
        print(error, file=sys.stderr)

    return render_template('index.html', libs=libs)

# Create a new video library
@app.route('/new-library', methods=['GET', 'POST'])
def new_library():
    if request.method == 'POST':
        name = request.form['name']
        owner = request.form['owner']
        error = None

        if not name:
            error = 'Name is required.'
        elif not owner:
            error = 'Owner is required.'

        if error is None:
            try:
                r = requests.post(f"{url_site}/library/")
            except requests.HTTPError as error:
                print(error, file=sys.stderr)
                if r.status_code == 404:
                    return redirect(url_for("library.new"))
            except requests.RequestException as error:
                print(error, file=sys.stderr)
        else:
            return redirect(url_for("index"))

        flash(error)

    return render_template('library/new.html')

# Display films in video library
@app.route('/library/<string:library>')
def show_library(library):
    error = None
    # Check if the library exist
    try:
        # Retrieve library content
        r = requests.get(f"{url_site}/library/")

        library

    except requests.HTTPError as error:
        print(error, file=sys.stderr)
        if r.status_code == 404:
            abort(404, f"The library {library} doesn't exist.")
    except requests.RequestException as error:
        print(error, file=sys.stderr)

    return render_template('library/show.html')

# Manage a video library based on the existence of a library (else abort(403) or error)
@app.route('/library/<string:library>/settings')
def settings(library):
    return render_template('library/edit.html')

# Manage a video library based on the existence of a library (else abort(403) or error)
@app.route('/library/<string:library>/settings/delete', methods=['POST'])
def delete_library(library):
    try:
        # Delete library
        r = requests.post(f"{url_site}/library/")
    except requests.HTTPError as error:
        print(error, file=sys.stderr)
        if r.status_code == 404:
            abort(404, f"The library {library} doesn't exist.")
    except requests.RequestException as error:
        print(error, file=sys.stderr)

    abort(404, f"The library {library} doesn't exist.")

## Video management

# Add a new video
@app.route('/new-video', methods=['GET', 'POST'])
def new_video():
    if request.method == 'POST':
        name = request.form['name']
        owner = request.form['owner']
        library = request.form['library']
        error = None

        if not name:
            error = 'Name is required.'
        elif not owner:
            error = 'Owner is required.'
        elif not library:
            error = 'Library is required.'

        if error is None:
            try:
                r = requests.post(f"{url_site}/library/")
            except requests.RequestException as error:
                print(error, file=sys.stderr)
        else:
            return redirect(url_for("home"))

        flash(error)

    return render_template('library/video/new.html')

# Edit a video
@app.route('/library/<string:library>/video/<video_id>/edit', methods=['GET', 'POST'])
def edit_video(library,video_id):
    return render_template('library/video/edit.html')

# Delete a video
@app.route('/library/<string:library>/video/<video_id>/delete', methods=['POST'])
def delete_video(library,video_id):
    try:
        # Delete library
        r = requests.post(f"{url_site}/library/")
    except requests.HTTPError as error:
        print(error, file=sys.stderr)
        if r.status_code == 404:
            abort(404, f"The library {library} doesn't exist.")
    except requests.RequestException as error:
        print(error, file=sys.stderr)

    return redirect(url_for(f"library.{library}.settings"))

# Search film in video library
@app.route('/search')
def search_video():
    if "type" in request.args:
        match request.args["type"]:
            case "title":
                # request.args["name"]
                return render_template('search/result.html')
            case "actor":
                # request.args["name"]
                return render_template('search/result.html')

    return render_template('search/search.html')

# /search?name=Pulp+Fiction
# /search?name=Pulp%20Fiction ?
