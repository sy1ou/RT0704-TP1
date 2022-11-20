from flask import Flask
from flask import request

import os
import json

app = Flask(__name__)
db_path = "app/database"

# List video libraries
@app.route('/library')
def library_list():
    res = []

    for path in os.listdir(path=db_path):
        # check if current path is a file
        print(path)
        if os.path.isfile(os.path.join(db_path, path)):
            res.append(os.path.splitext(path)[0])
    return(json.dumps(res))

# Create/Return/Delete a video library
@app.route('/library/<string:library>', methods=['GET', 'POST', 'DELETE'])
def library_management(library):
    return "soon"
    # if request.method == 'GET':
        # Search in all files

# - Create parametres
#   - Nom du fichier
#   - Proprietaire
# - Creation de la liste des films vide

# - Delete parametres
#   - Nom du fichier
# - Destruction du fichier

# Search film in video library
@app.route('/library/<string:library>/by-name/<string:name>')
def search_by_name():
    return "soon"

# /search/name/Pulp+Fiction

# Search for films by an actor in video library
@app.route('/library/<string:library>/by-actor/<string:name>')
def search_by_actor():
    return "soon"

# Add/Edit/Delete a video
@app.route('/library/<string:library>/video/<video_id>', methods=['POST', 'PUT', 'DELETE'])
def video_management():
    return "soon"
