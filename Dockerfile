# Set the base image to the base image
FROM hmlandregistry/dev_base_python_flask:3

RUN yum install -y -q postgresql-devel

# SQL_HOST: This must match the database created in postgres-init-fragment:
# SQL_DATABASE: This is the root user specified in the postgres Dockerfile:
# ALEMBIC_SQL_USERNAME: (This will be temporarily overidden to yes when the alembic database upgrade is run)
# The following entries must match the user created in the fragments/postgres-init-fragment.sql:
# APP_SQL_USERNAME, SQL_PASSWORD (This will be temporarily overidden to be the root password when the alembic database upgrade is run)
ENV SQL_HOST=postgres \
 SQL_DATABASE=thing \
 ALEMBIC_SQL_USERNAME=root \
 SQL_USE_ALEMBIC_USER=no \
 APP_SQL_USERNAME=thinguser \
 SQL_PASSWORD=thingpassword

# ----
# Put your app-specific stuff here (extra yum installs etc).
# Any unique environment variables your config.py needs should also be added as ENV entries here

ENV APP_NAME="thing-api" \
    MAX_HEALTH_CASCADE=6 \
    TIMEOUT="5"

# Dependencies
ENV AUDIT_API_URL="http://audit-api:8080" \
    AUDIT_API_VERSION="v1"

# ----

# The command to run the app is inherited from lr_base_python_flask

# Get the python environment ready.
# Have this at the end so if the files change, all the other steps don't need to be rerun. Same reason why _test is
# first. This ensures the container always has just what is in the requirements files as it will rerun this in a
# clean image.
ADD requirements_test.txt requirements_test.txt
ADD requirements.txt requirements.txt
RUN pip3 install -q -r requirements.txt && \
  pip3 install -q -r requirements_test.txt
