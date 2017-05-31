from flask import Blueprint, Response
from flask_negotiate import consumes, produces
from jsonschema import validate, ValidationError
import json

# This is the blueprint object that gets registered into the app in blueprints.py.
title_v1 = Blueprint('title_v1', __name__)

# JSON schema for title requests
with open('title_api/swagger.json') as json_file:
    swagger = json.load(json_file)

title_schema = swagger["definitions"]["TitleRequest"]


@title_v1.route("/titles", methods=['GET'])
@produces('application/json')
def get_titles():
    """Get all titles."""
    return Response(response=json.dumps({"foo": "bar"}, separators=(',', ':')),
                    mimetype='application/json',
                    status=200)


@title_v1.route("/titles", methods=['POST'])
@consumes("application/json")
@produces('application/json')
def create_title():
    """Create a new title."""
    return Response(response=json.dumps({"foo": "bar"}, separators=(',', ':')),
                    mimetype='application/json',
                    status=201)


@title_v1.route("/titles/<uuid:title_id>", methods=['GET'])
@produces('application/json')
def get_title(title_id):
    """Get a title for a given title_id."""
    return Response(response=json.dumps({"foo": "bar"}, separators=(',', ':')),
                    mimetype='application/json',
                    status=200)


@title_v1.route("/titles/<uuid:title_id>", methods=['PUT'])
@consumes("application/json")
@produces('application/json')
def update_title(title_id):
    """Update a title for a given title_id."""
    return Response(response=json.dumps({"foo": "bar"}, separators=(',', ':')),
                    mimetype='application/json',
                    status=200)


@title_v1.route("/titles/<uuid:title_id>", methods=['DELETE'])
@produces('application/json')
def delete_title(title_id):
    """Delete a title for a given title_id."""
    return Response(response=None,
                    mimetype='application/json',
                    status=204)
