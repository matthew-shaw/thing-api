# Title API

## Dependencies
* [Audit API](http://192.168.249.38/transaction-monitoring/audit-api)
* PostgreSQL

## Specification

This API is defined using [OpenAPI Specification 2.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) compliant [`swagger.json`](title_api/swagger.json) code.

## Examples

Copy the contents of [`swagger.json`](title_api/swagger.json) into the [Swagger Editor](http://editor.swagger.io/) to visualise the interface and see example requests and responses.

## Error Codes
* E027 - Failed to create title.
* E028 - Failed to get title.
* E029 - Failed to search for titles.
* E030 - Failed to update a whole title.
* E031 - Failed to update part of a title.
* E032 - Failed to delete title.

## Skeleton Documentation

This app is derived from the Flask Skeleton API, for further documentation please refer to the [README](http://192.168.249.38/skeletons/flask-skeleton-api/blob/master/README.md).
