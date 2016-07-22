from flask import request, Blueprint, Response
from flask import current_app
import json

# This is the blueprint object that gets registered into the app in blueprints.py.
general = Blueprint('general', __name__)


@general.route("/health")
def check_status():
    return Response(response=json.dumps({
        "app": "flask-skeleton-api",
        "status": "OK",
        "headers": str(request.headers),
        "commit": current_app.config["COMMIT"]
    }),  mimetype='application/json', status=200)

