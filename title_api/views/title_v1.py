from flask import Blueprint, Response, request
from title_api.extensions import db
from title_api.models import Title
from title_api.exceptions import ApplicationError
from title_api.dependencies.audit_api import AuditAPI
from flask_negotiate import consumes, produces
from datetime import datetime
from jsonschema import validate, ValidationError, FormatChecker
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
    """Get Titles."""
    titles = Title.query.order_by(Title.created_at).all()
    results = []
    for title in titles:
        results.append(json.loads(repr(title)))

    audit = AuditAPI()
    audit.create("Retrieved Titles")
    return Response(response=json.dumps(results, separators=(',', ':')),
                    mimetype='application/json',
                    status=200)


@title_v1.route("/titles", methods=['POST'])
@consumes("application/json")
@produces('application/json')
def create_title():
    """Create a new Title."""
    title_request = request.json

    # Validate request against schema
    try:
        validate(title_request, title_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise ApplicationError(str(e), "E001", 400)

    # Create a new title
    title = Title(foo=title_request["foo"],
                  bar=title_request["bar"])

    # Commit title to db
    db.session.add(title)
    db.session.commit()

    # Create new title response
    response = Response(response=repr(title),
                        mimetype='application/json',
                        status=201)

    # For newly created resources, always set the Location header to the GET request route of the new resource.
    response.headers["Location"] = "{0}/{1}".format(request.url, title.title_id)

    audit = AuditAPI()
    audit.create("Created new Title: " + title.title_id)
    return response


@title_v1.route("/titles/<uuid:title_id>", methods=['GET'])
@produces('application/json')
def get_title(title_id):
    """Get a Title for a given title_id."""
    title = Title.query.get_or_404(str(title_id))

    audit = AuditAPI()
    audit.create("Retrieved Title: " + title.title_id)
    return Response(response=repr(title),
                    mimetype='application/json',
                    status=200)


@title_v1.route("/titles/<uuid:title_id>", methods=['PUT'])
@consumes("application/json")
@produces('application/json')
def update_title(title_id):
    """Update a Title for a given title_id."""
    title_request = request.json

    try:
        validate(title_request, title_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise ApplicationError(str(e), "E001", 400)

    title = Title.query.get_or_404(str(title_id))

    title.foo = title_request["foo"]
    title.bar = title_request["bar"]
    title.updated_at = datetime.utcnow()

    db.session.add(title)
    db.session.commit()

    audit = AuditAPI()
    audit.create("Updated Title: " + title.title_id)
    return Response(response=repr(title),
                    mimetype='application/json',
                    status=200)


@title_v1.route("/titles/<uuid:title_id>", methods=['DELETE'])
@produces('application/json')
def delete_title(title_id):
    """Delete a Title for a given title_id."""
    title = Title.query.get_or_404(str(title_id))

    db.session.delete(title)
    db.session.commit()

    audit = AuditAPI()
    audit.create("Deleted Title: " + title.title_id)
    return Response(response=None,
                    mimetype='application/json',
                    status=204)
