# Import every blueprint file
from thing_api.views import general, thing_v1


def register_blueprints(app):
    """Adds all blueprint objects into the app."""
    app.register_blueprint(general.general)
    app.register_blueprint(thing_v1.thing_v1, url_prefix='/v1')

    # All done!
    app.logger.info("Blueprints registered")
