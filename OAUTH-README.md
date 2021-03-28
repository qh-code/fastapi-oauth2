# Configuration for authentication with Microsoft Identity Platform

## Default configuration

Default configuration put into the `oauth.env` file (and preconfigured in MS Identity Platform) allows two user to use the api:
* User: `jtest@nnmdrtest.onmicrosoft.com` (password: `QTtnD327ctmzPy3A`)
* User: `stest@nnmdrtest.onmicrosoft.com` (password: `TP8CJ8ChEZws63vF`)
Assuming swagger UI of the API is exposed at `http://localhost:8000`.

`OAUTH_ENABLED` constant is set to `False` which means that only test endpoint (`/access-token-payload-test`) is
protected. Other endpoints are not protected and allow for (optional) user id injection with `X-Test-User-Id` HTTP header.

To define other configuration follow steps described below.

## Register API server as application in Microsoft Identity Platform

* Choose or create a tenant (note its id as `TENANT_ID`)

* Create new app registration (note its application id as `SERVER_ID`)
    * Choose supported account types as _Accounts in this organizational directory only (... only - Single Tenant)_

* define single scope for the app and make it require only admin consent (note it's URI as `SCOPE`)

## Register swagger UI as (another) application in Microsoft Identity Platform

* use the same tenant as for the API server app

* create new app registration (note its application id as `SWAGGER_CLIENT_ID`)
    * Choose supported account types as _Accounts in this organizational directory only (... only - Single Tenant)_

* set redirect URI for `.../docs/oauth2-redirect`
  (where `...` stays for protocol and host name where swagger UI is exposed, you can use e.g. 
  `http://localhost:8000/docs/oauth2-redirec` if setting up for local dev environment). **Note**: You must register
  redirect in _Single Page Application (SPA)_ as platform (by default azure portal proposes _Web_ platform, which will 
  not work with Swagger UI).
  
* in _API permissions_ page of the application registration add a permission for the app to use scope you defined
  above for API Server (and choose _Grant admin consent for mdr_test_)
  
## Grant admin consent for all tenant for both registered applications

* You can do that in _Enterprise applications > ... > Permissions_


## Put noted values into `oauth.env` file

* put/replace values of `TENANT_ID`, `SERVER_ID`, `SWAGGER_CLIENT_ID` and `SCOPE` you noted from above steps as 
  environment constants in `oauth.env` file (leave other values intact unless you know what you're doing)
  
## Turn API protection on/off

* Set value of `OAUTH_ENABLED` constant to:
  * `True` to engage protection of all API endpoints or
  * `False` to leave only `/access-token-payload` endpoint protected (this is test endpoint)
    
**Note**: In the latter case an API is going to inject some default user id value into the endpoints routers 
unless client provides some specific value to inject in `X-Test-User-Id` HTTP header.


