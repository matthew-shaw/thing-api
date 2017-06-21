# Thing API

## Dependencies
* [Audit API](http://192.168.249.38/transaction-monitoring/audit-api)
* PostgreSQL

## Specification

This API is defined using [OpenAPI Specification 2.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) compliant [`swagger.json`](thing_api/swagger.json) code.

## Examples

Copy the contents of [`swagger.json`](thing_api/swagger.json) into the [Swagger Editor](http://editor.swagger.io/) to visualise the interface and see example requests and responses.

## Database Tables

### Thing
```
Table "public.thing"
   Column    |            Type             | Modifiers 
-------------+-----------------------------+-----------
 thing_id    | uuid                        | not null
 foo         | character varying           | not null
 bar         | character varying           | not null
 created_at  | timestamp without time zone | not null
 updated_at  | timestamp without time zone | 
 archived_at | timestamp without time zone | 

Indexes:
"thing_pkey" PRIMARY KEY, btree (thing_id)
```

## Error Codes
* E027 - Failed to create thing.
* E028 - Thing not found.
* E029 - Failed to search for things.
* E030 - Failed to update a whole thing.
* E031 - Failed to update part of a thing.
* E032 - Failed to delete thing.

## Skeleton Documentation

This app is derived from the Flask Skeleton API, for further documentation please refer to the [README](http://192.168.249.38/skeletons/flask-skeleton-api/blob/master/README.md).
