from typing import List, Optional
from starlette.requests import Request
from loguru import logger

import uvicorn
from starlette_context import context, middleware, plugins, header_keys

from fastapi import FastAPI, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

get_method_name = "GET"
post_method_name = "POST"
trace_id_key = "unique_id"
default_trace_value = "unknown"
logger.add(lambda record: print(record, context[header_keys.HeaderKeys.request_id], context[trace_id_key]),
           level="INFO")
app = FastAPI()
app.add_middleware(
    middleware.ContextMiddleware,
    plugins=(
        plugins.RequestIdPlugin(),
    ),
)

router = APIRouter()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    logger.info(f"get: {item_id}")

    return items["foo"]


@router.post("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    logger.info("收到请求")
    # print(context.data)
    # print(context[header_keys.HeaderKeys.request_id])
    return update_item_encoded


#
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = Field(
#         None, title="The description of the item", max_length=300
#     )
#     price: float = Field(..., gt=0, description="The price must be greater than zero")
#     tax: Optional[float] = None
#
#
# @app.post("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(..., embed=True)):
#     results = {"item_id": item_id, "item": item}
#     return results
#


async def set_trace_info(request: Request):
    method = request.method
    if method == get_method_name:
        r_params = request.query_params
    elif method == post_method_name:
        r_params = await request.json()
    else:
        r_params = {}
    context[trace_id_key] = r_params.get(trace_id_key, default_trace_value)


app.include_router(router, dependencies=[Depends(set_trace_info)])

if __name__ == '__main__':

    uvicorn.run(app)
