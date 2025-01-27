import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from db import stores

blp = Blueprint("items",__name__, "Operations on stores")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            return{"message": "Item not found"},404
        # for store in stores:
        #     if store["name"] == name:
        #         return { "item":store["item"]},201
        # return {"message":"error"},404
    def delete(self,item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404,message="Item not found")

    def put(self,item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(400,message= "Bad request. Ensure 'price' and 'name' are included in the JSON payload.")
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404,message = "Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        # return "Hello World"
            return {"item" : list(items.values())}

    def post(self): # create new item
        item_data=request.get_json()

        if ("price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data):

            abort(400,
                message="Bad request. Ensure 'price','store' and 'name' are included in the JSON payload.",
                )
        for item in items.values():
            if( 
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
                ):
                abort(404,message= "Items already exists")
                

        if item_data["store_id"] not in stores:
            # return {"message": "Store not found"},404
            abort(404,message= "Store not found")
        print(item_data)
        item_id = uuid.uuid4().hex
        item = {**item_data,"id": item_id}
        items[item_id]=item
        return item,201


