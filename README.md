# Title API

## Dependencies
* [Audit API](http://192.168.249.38/transaction-monitoring/audit-api)

## Specification

This API is defined using [OpenAPI Specification 2.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) compliant [`swagger.json`](title_api/swagger.json) code.

## Examples

### Create title

Request: `POST /v1/titles`
```json
```

Response: `201`
```json
```

### Get title

Request: `GET /v1/titles/<uuid:title_id>`

Response: `200`
```json
```

### Get titles

Request: `GET /v1/titles`

Response: `200`
```json
```

### Search titles

Request: `GET /v1/titles?q=<string:query>`

Response: `200`
```json
```

### Update whole title

Request: `PUT /v1/titles/<uuid:title_id>`
```json
```

Response: `200`
```json
```

### Update part title

Request: `PATCH /v1/titles/<uuid:title_id>`
```json
```

Response: `200`
```json
```

### Delete title

Request: `DELETE /v1/titles/<uuid:title_id>`

Response: `204`

## Skeleton Documentation

This app is derived from the Flask Skeleton API, for further documentation please refer to the [README](http://192.168.249.38/skeletons/flask-skeleton-api/blob/master/README.md).
