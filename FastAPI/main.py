from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float 


app = FastAPI()


@app.post("/items/")
def create_item(item: Item):
    return {'data':f"item is created as {item.name}"}