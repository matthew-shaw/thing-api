from flask import current_app, g
from datetime import datetime
from title_api.app import app
from title_api.exceptions import ApplicationError
import json
import requests


class AuditAPI(object):
    """Encapsulating class for Audit API access."""
    def __init__(self):
        self.base_url = current_app.config["AUDIT_API_URL"]
        self.version = current_app.config["AUDIT_API_VERSION"]
        self.timeout = current_app.config["TIMEOUT"]

    def create(self, activity):
        """Create a new audit record."""
        url = '{0}/{1}/records'.format(self.base_url, self.version)
        record = {
            "activity": activity,
            "activity_timestamp": str(datetime.now().isoformat()),
            "origin_id": current_app.config['APP_NAME'],
            "component_name": current_app.config['APP_NAME'],
            "business_service": "Title Service"
        }
        headers = {"Content-Type": "application/json"}
        try:
            response = g.requests.post(url, data=json.dumps(record), headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise ApplicationError("Connection to Audit API timed out", "E100", 408)
        else:
            if response.status_code != 201:
                raise ApplicationError("Failed to create record.", "E002", 500)
            else:
                app.logger.info(activity)
