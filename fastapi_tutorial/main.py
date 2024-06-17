from fastapi import FastAPI, Query
from pydantic import BaseModel

from typing import Annotated


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# You can declare path parameters and request body at the same time.
# FastAPI will recognize that the function parameters that match path
# parameters should be taken from the path, and that function parameters
# that are declared to be Pydantic models should be taken from the request body.

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.model_dump()}


# You can also declare body, path and query parameters, all at the same time.
# FastAPI will recognize each of them and take the data from the correct place.
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result |= {"q": q}
    return result


@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# When you define a query parameter explicitly with Query you can also declare
# it to receive a list of values, or said in other way, to receive multiple values.
@app.get("/items/")
async def read_items_list(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items


# Then, with a URL like: http://localhost:8000/items/?q=foo&q=bar
# you would receive the multiple q query parameters' values (foo and bar) in
# a Python list inside your path operation function, in the function parameter q.

#! To declare a query parameter with a type of list, like in the example above, you need
#! to explicitly use Query, otherwise it would be interpreted as a request body.


@app.get("/items/")
async def read_items_title(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items_alias(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Deprecated parameters
@app.get("/items/")
async def read_items_deprecated(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Hidden
@app.get("/items/")
async def read_items_hidden(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}
