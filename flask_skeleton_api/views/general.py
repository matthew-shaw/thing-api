from flask import request, Blueprint, Response
from flask import current_app, g
import datetime
import json

# This is the blueprint object that gets registered into the app in blueprints.py.
general = Blueprint('general', __name__)


@general.route("/health")
def check_status():
    return Response(response=json.dumps({
        "app": current_app.config["APP_NAME"],
        "status": "OK",
        "headers": request.headers.to_list(),
        "commit": current_app.config["COMMIT"]
    }),  mimetype='application/json', status=200)


@general.route("/health/cascade/<str_depth>")
def cascade_health(str_depth):
    depth = int(str_depth)

    if (depth < 0) or (depth > int(current_app.config.get("MAX_HEALTH_CASCADE"))):
        current_app.logger.error("Cascade depth {} out of allowed range (0 - {})".format(depth, current_app.config.get("MAX_HEALTH_CASCADE")))
        return Response(response=json.dumps({
            "app": current_app.config.get("APP_NAME"),
            "cascade_depth": str_depth,
            "status": "ERROR",
            "timestamp": str(datetime.datetime.now())
        }),  mimetype='application/json', status=500)

    dbs = []
    services = []
    overall_status = 200  # if we encounter a failure at any point then this will be set to != 200
    if current_app.config.get("DEPENDENCIES") is not None:
        for dependency, value in current_app.config.get("DEPENDENCIES").items():
            # Below is an example of hitting a database dependency - in this instance postgresql
            # It requires a route to obtain the current timestamp to be declared somewhere in code
            # In the below example we have an sql.py script containing the get_current_timestamp() function
            # if "postgres" in value:
            #    # postgres db url - try calling current timestamp routine
            #    db = {}
            #    db["name"] = dependency
            #    try:
            #        db_timestamp = postgres.get_current_timestamp()
            #    except Exception as e:
            #        db_timestamp = None
            #    if db_timestamp is not None:
            #        db["current_timestamp"] = db_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'  # trim microseconds to 3 to match java
            #        db["status"] = "OK"
            #    else:
            #        overall_status = 500
            #        db["status"] = "BAD"
            #    dbs.append(db)
            # else:  # indent the following code to match the if..else block when database checks are included
            if (depth < 1):
                continue

            # As there is an inconsistant approach to url variables we need to check to see if we have a trailing '/' and add one if not
            if value[-1] != '/':
                value = value + '/'
            service = {}

            try:
                service["name"] = dependency
                service["type"] = "http"

                # assume it's a service url and call it's casecade route with depth -1
                resp = g.requests.get(value + 'health/cascade/' + str(depth - 1))

                service["status_code"] = resp.status_code
                service["content_type"] = resp.headers["content-type"]
                service["content"] = resp.json()

                if resp.status_code == 200:
                    service["status"] = "OK"
                elif resp.status_code == 500:
                    service["status"] = "BAD"
                    overall_status = 500
                else:
                    service["status"] = "UNKNOWN"
                    overall_status = 500

                services.append(service)

            except Exception as e:
                current_app.logger.error("Exception occured during health cascade: {}".format(e))
                # The three items below are omitted for consistency with the java implementation where null entries are
                # not added to the final json by the json parser, but included to show consideration
                # service["status_code"] = None
                # service["content_type"] = None
                # service["content"] = None
                service["status"] = "UNKNOWN"
                overall_status = 500

    return Response(response=json.dumps({
        "cascade_depth": depth,
        "server_timestamp": str(datetime.datetime.now()),
        "app": current_app.config.get("APP_NAME"),
        "status": "OK",
        "headers": request.headers.to_list(),
        "commit": current_app.config.get("COMMIT"),
        "db": dbs,
        "services": services
        }),  mimetype='application/json', status=overall_status)