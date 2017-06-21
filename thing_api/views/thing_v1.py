from flask import Blueprint, Response, request
from thing_api.extensions import db
from thing_api.models import Thing
from thing_api.exceptions import ApplicationError
from thing_api.dependencies.audit_api import AuditAPI
from flask_negotiate import consumes, produces
from datetime import datetime
from jsonschema import validate, ValidationError, FormatChecker
import json

# This is the blueprint object that gets registered into the app in blueprints.py.
thing_v1 = Blueprint('thing_v1', __name__)

# JSON schema for thing requests
with open('thing_api/swagger.json') as json_file:
    swagger = json.load(json_file)

thing_schema = swagger["definitions"]["ThingRequest"]


@thing_v1.route("/things", methods=['GET'])
@produces('application/json')
def get_things():
    """Get Things."""
    things = Thing.query.order_by(Thing.created_at).all()
    results = []
    for thing in things:
        results.append(json.loads(repr(thing)))

    audit = AuditAPI()
    audit.create("Retrieved Things")
    return Response(response=json.dumps(results, separators=(',', ':')),
                    mimetype='application/json',
                    status=200)


@thing_v1.route("/things", methods=['POST'])
@consumes("application/json")
@produces('application/json')
def create_thing():
    """Create a new Thing."""
    thing_request = request.json

    # Validate request against schema
    try:
        validate(thing_request, thing_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise ApplicationError(str(e), "E001", 400)

    # Create a new thing
    thing = Thing(foo=thing_request["foo"],
                  bar=thing_request["bar"])

    # Commit thing to db
    db.session.add(thing)
    db.session.commit()

    # Create new thing response
    response = Response(response=repr(thing),
                        mimetype='application/json',
                        status=201)

    # For newly created resources, always set the Location header to the GET request route of the new resource.
    response.headers["Location"] = "{0}/{1}".format(request.url, thing.thing_id)

    audit = AuditAPI()
    audit.create("Created Thing: " + thing.thing_id)
    return response


@thing_v1.route("/things/<uuid:thing_id>", methods=['GET'])
@produces('application/json')
def get_thing(thing_id):
    """Get a Thing for a given thing_id."""
    thing = Thing.query.filter_by(thing_id=str(thing_id)).first()
    if not thing:
        raise ApplicationError('Thing not found', 'Exxx', 404)

    audit = AuditAPI()
    audit.create("Retrieved Thing: " + thing.thing_id)
    return Response(response=repr(thing),
                    mimetype='application/json',
                    status=200)


@thing_v1.route("/things/<uuid:thing_id>", methods=['PUT'])
@consumes("application/json")
@produces('application/json')
def update_thing(thing_id):
    """Update a Thing for a given thing_id."""
    thing_request = request.json

    try:
        validate(thing_request, thing_schema, format_checker=FormatChecker())
    except ValidationError as e:
        raise ApplicationError(str(e), "E001", 400)

    thing = Thing.query.filter_by(thing_id=str(thing_id)).first()
    if not thing:
        raise ApplicationError('Thing not found', 'Exxx', 404)

    thing.foo = thing_request["foo"]
    thing.bar = thing_request["bar"]
    thing.updated_at = datetime.utcnow()

    db.session.add(thing)
    db.session.commit()

    audit = AuditAPI()
    audit.create("Updated Thing: " + thing.thing_id)
    return Response(response=repr(thing),
                    mimetype='application/json',
                    status=200)


@thing_v1.route("/things/<uuid:thing_id>", methods=['DELETE'])
@produces('application/json')
def delete_thing(thing_id):
    """Delete a Thing for a given thing_id."""
    thing = Thing.query.filter_by(thing_id=str(thing_id)).first()
    if not thing:
        raise ApplicationError('Thing not found', 'Exxx', 404)

    db.session.delete(thing)
    db.session.commit()

    audit = AuditAPI()
    audit.create("Deleted Thing: " + thing.thing_id)
    return Response(response=None,
                    mimetype='application/json',
                    status=204)
