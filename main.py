from typing import List, Mapping, Any

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from oauth import SWAGGER_UI_INIT_OAUTH, get_access_token_payload, get_current_user_id, ALLOW_ORIGIN_REGEX

# Load environment variables


# Define the auth scheme and access token URL


app = FastAPI(swagger_ui_init_oauth=SWAGGER_UI_INIT_OAUTH)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=ALLOW_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Data model
class Item(BaseModel):
    id: int
    name: str


# Protected, get items route
@app.get('/items', response_model=List[Item])
def read_items(current_user_id: str = Depends(get_current_user_id)):
    print(f"current_user_id = {current_user_id}")
    return [
        Item.parse_obj({'id': 1, 'name': 'red ball'}),
        Item.parse_obj({'id': 2, 'name': 'blue square'}),
        Item.parse_obj({'id': 3, 'name': 'purple ellipse'}),
    ]


@app.get('/access-token-payload', response_model=Mapping[str, str])
def read_access_token(token_payload: Mapping[str, Any] = Depends(get_access_token_payload)):
    return {claim: str(token_payload[claim]) for claim in token_payload}
