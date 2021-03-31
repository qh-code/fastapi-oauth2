# Sample Rest API secured by AWS Cognito

# Local development

## AWS Region and Pool ID

Change `aws-region` and `cognito-pool-id` properties in `resources/appplication.yaml` file

Example
```
aws-region: "us-east-2"
cognito-pool-id: "us-east-2_CEDW1OT68"
```

## Roles in application

Currently, there are no roles defines in system, 
but as example of poc we can get them from groups.
In this example name of groups are name of roles.

Change `cognito-roles` property in `resources/appplication.yaml` file

Example
```
cognito-roles: "cognito:groups"
```

In command line, go to `fastapi-oauth2` dir and then execute `mvn spring-boot:run`


## Endpoints

`/api/messages/hello` - returns `Hello from messages REST API` message when run with valid Bearer token

When you call endpoint without Bearer token, example:

`curl -o /dev/null -s -w "%{http_code}\n" http://localhost:8080/api/messages/hello`

Then `401` should be returned because you didn't pass Bearer token in Header

When you replace `<bearer token>` with valid token and call

`curl -o /dev/null -s -w "%{http_code}\n" -H "Authorization: Bearer <bearer token>" http://localhost:8080/api/messages/hello`

Then `200` should be returned

## Swagger

Swagger endpoint `http://localhost:8080/swagger-ui/`
