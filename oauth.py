from http import HTTPStatus
from typing import Mapping, Any

import requests
from fastapi import HTTPException, Depends, Header
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, jwk  # type: ignore
from jose.utils import base64url_decode # type: ignore
from okta_jwt.utils import verify_iss, verify_aud, verify_exp, verify_iat  # type: ignore
from starlette.config import Config

_CONFIG = Config('oauth.env')
_TENANT_ID = _CONFIG("TENANT_ID")
_SERVER_ID = _CONFIG('SERVER_ID')
_SWAGGER_CLIENT_ID = _CONFIG("SWAGGER_CLIENT_ID")
_OIDC_METADATA_DOCUMENT = _CONFIG("OIDC_METADATA_DOCUMENT")
_SERVER_AUDIENCE = _CONFIG("SERVER_AUDIENCE").replace("{TenantId}", _TENANT_ID).replace("{ServerId}", _SERVER_ID)
_TOKEN_ISSUER = _CONFIG("TOKEN_ISSUER").replace("{TenantId}", _TENANT_ID).replace("{ServerId}", _SERVER_ID)
_TOKEN_URL = _CONFIG("TOKEN_URL").replace("{TenantId}", _TENANT_ID).replace("{SwaggerClientId}", _SWAGGER_CLIENT_ID)
_AUTHORIZE_URL = _CONFIG("AUTHORIZE_URL").replace("{TenantId}", _TENANT_ID).replace("{SwaggerClientId}", _SWAGGER_CLIENT_ID)
_OAUTH_ENABLED = not _CONFIG("OAUTH_ENABLED").upper() == "FALSE"
_SCOPE = _CONFIG("SCOPE").replace("{TenantId}", _TENANT_ID).replace("{ServerId}", _SERVER_ID)
_USER_ID_CLAIM = _CONFIG("USER_ID_CLAIM")

# noinspection SpellCheckingInspection
SWAGGER_UI_INIT_OAUTH = {
    "usePkceWithAuthorizationCodeGrant": True,
    "clientId": _SWAGGER_CLIENT_ID,
    "scopes": _SCOPE
}

ALLOW_ORIGIN_REGEX = _CONFIG("ALLOW_ORIGIN_REGEX")

_JWKS_CACHE = {}

_oauth2_scheme = OAuth2AuthorizationCodeBearer(
    # scopes={"api://c70e0ac4-7775-4615-b1a0-76eb1ca838a0/Items.Read.All": "Read All Items"},
    authorizationUrl=_AUTHORIZE_URL,
    tokenUrl=_TOKEN_URL,
    refreshUrl=_TOKEN_URL)


def _validate_token(access_token: str) -> Mapping[str, str]:
    # Decoding Header & Payload from token
    header = jwt.get_unverified_header(access_token)
    payload = jwt.get_unverified_claims(access_token)

    # Verifying Claims
    try:
        verify_iss(payload, _TOKEN_ISSUER)
    except Exception:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Wrong 'iss' claim.")

    try:
        verify_aud(payload, _SERVER_AUDIENCE)
    except Exception:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Wrong 'aud' claim.")

    try:
        verify_exp(payload)
    except Exception:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Wrong 'exp' claim.")

    try:
        verify_iat(payload)
    except Exception:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Wrong 'iat' claim.")

    global _JWKS_CACHE

    kid = header['kid']
    if kid not in _JWKS_CACHE:
        # retrieving key if not in cache

        # first metadata document
        try:
            metadata_response = requests.get(_OIDC_METADATA_DOCUMENT)

            # Consider any status other than 2xx an error
            if not metadata_response.status_code // 100 == 2:
                raise Exception(metadata_response.text, metadata_response.status_code)

        except requests.exceptions.RequestException as e:
            # A serious problem happened, like an SSLError or InvalidURL
            raise Exception("Error: {}".format(str(e)))

        # then key store
        jwks_url = metadata_response.json()["jwks_uri"]
        try:
            jwks_response = requests.get(jwks_url)

            # Consider any status other than 2xx an error
            if not jwks_response.status_code // 100 == 2:
                raise Exception(jwks_response.text, jwks_response.status_code)
        except requests.exceptions.RequestException as e:
            # A serious problem happened, like an SSLError or InvalidURL
            raise Exception("Error: {}".format(str(e)))

        # search for key by given 'kid' header
        jwks = list(filter(lambda x: x['kid'] == kid, jwks_response.json()['keys']))

        if not len(jwks):
            raise HTTPException(HTTPStatus.UNAUTHORIZED, "Error: Could not find jwk for kid: {}".format(kid))

        # put that in the cache
        _JWKS_CACHE[kid] = jwks[0]

    jwks_key = _JWKS_CACHE[kid]
    key = jwk.construct(jwks_key, header['alg'])
    message, encoded_sig = access_token.rsplit('.', 1)
    decoded_sig = base64url_decode(encoded_sig.encode('utf-8'))

    valid = key.verify(message.encode(), decoded_sig)

    # If the token is valid, it returns the payload
    if valid:
        return payload
    else:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Token signature invalid.")


def get_access_token_payload(access_token: str = Depends(_oauth2_scheme)) -> Mapping[str, Any]:
    return _validate_token(access_token)


def get_current_user_id_by_oauth(token_payload: Mapping[str, Any] = Depends(get_access_token_payload)) -> str:
    # print(f"get_current_user_id.token_payload = {token_payload}")
    return str(token_payload[_USER_ID_CLAIM])


if _OAUTH_ENABLED:
    def get_current_user_id(user: str = Depends(get_current_user_id_by_oauth)) -> str:
        return user
else:
    def get_current_user_id(x_test_user_id: str = Header("unknown-user",  # type: ignore
                                                         description="A value to be injected into service as user id.")
                            ) -> str:
        return x_test_user_id
