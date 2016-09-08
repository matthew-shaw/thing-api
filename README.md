# flask-skeleton

This repository contains a flask application structured in the way that all
Land Registry flask APIs should be structured going forwards.

You can use this to create your own app.
Take a copy of all the files, and change all occurences of flask-skeleton-api/flask_skeleton_api to your app name. There will be other places to tweak too such as the exposed port in docker-compose-fragment, so please look through every file before starting to extend it for your own use.

## Quick start

```shell
# For Flask CLI
export FLASK_APP=flask_skeleton_api/main.py
export FLASK_DEBUG=1
# For Python
export PYTHONUNBUFFERED=yes
# For gunicorn
export PORT=9999
# For app's config.py
export FLASK_LOG_LEVEL=DEBUG
export COMMIT=LOCAL

# Run the app
flask run
```

or run the shell command:

```bash
python3 manage.py runserver
```

To see what other commands are available run:

```bash
python manage.py --help
```

## Unit tests

The unit tests are contained in the unit_tests folder. [Pytest](http://docs.pytest.org/en/latest/) is used for unit testing. To run the tests use the following command:

```bash
python3 manage.py unittest
(or just py.test)
```

To run them and output a coverage report and a junit xml file run:

```bash
python3 manage.py unittest -r
```

These files get added to a test-output folder. The test-output folder is created if doesn't exist.

To run the unit tests if you are using the common dev-env use the following command:

```bash
docker-compose exec flask-skeleton-api python3 manage.py unittest
or, using the alias
unit-test flask-skeleton-api
```

or

```bash
docker-compose exec flask-skeleton-api python3 manage.py unittest -r
or, using the alias
unit-test flask-skeleton-api -r
```

# Integration tests

The integration tests are contained in the integration_tests folder. [Pytest](http://docs.pytest.org/en/latest/) is used for integration testing. To run the tests use the following command:

```
python3 manage.py integrationtest
(or py.test integration_tests)
```

To run them and output a junit xml file run:

```
python3 manage.py integrationtest -r
```

This file gets added to the test-output folder. The test-output folder is created if doesn't exist.

To run the integration tests if you are using the common dev-env use the following command:

```
docker-compose exec flask-skeleton-api python3 manage.py integrationtest
```

## Notes

* This app contains the files necessary for Universal Dev Env support. See the [UDE readme](http://192.168.249.38/common/dev-env#tab-readme) for more info.
