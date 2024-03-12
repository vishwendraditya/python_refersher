from flask import Flask
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint


app= Flask(__name__ )

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Store REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)












# # stores = [
# #     {
# #         "name": "My Store", "item": [{"item 1": "my item", "price": 15.99}]
# #     }
# #         ]



# @app.route("/store",methods= ['GET']) 
# def get_all_store():
#    return {"stores" : list(stores.values())}


# @app.route("/item",methods= ['GET'])
# def get_all_item():
#     # return "Hello World"
#     return {"item" : list(items.values())}

# @app.route("/store",methods=["POST"])
# def create_store():
#     store_data=request.get_json()
#     if "name" not in store_data:
#         # return {"message":"Bad request. Ensure 'name' is included in the JSON payload."},400
#         abort(400,message="Bad request. Ensure 'name' is included in the JSON payload.",)

#     for store in stores.values():
#         if store_data["name"] == store["name"]:
#             abort(400,message=f"Store already exist.")

#     store_id = uuid.uuid4().hex
#     store= {**store_data,"id": store_id}
#     stores[store_id] = store
#     # stores.append(new_store)
#     return store, 201


# @app.route("/item",methods=["POST"])
# def create_item():
#     item_data=request.get_json()

#     if ("price" not in item_data
#         or "store_id" not in item_data
#         or "name" not in item_data):

#         abort(400,
#               message="Bad request. Ensure 'price','store' and 'name' are included in the JSON payload.",
#             )
#     for item in items.values():
#         if( 
#             item_data["name"] == item["name"]
#             and item_data["store_id"] == item["store_id"]
#             ):
#             abort(404,message= "Items already exists")
            

#     if item_data["store_id"] not in stores:
#         # return {"message": "Store not found"},404
#         abort(404,message= "Store not found")
#     print(item_data)
#     item_id = uuid.uuid4().hex
#     item = {**item_data,"id": item_id}
#     items[item_id]=item
#     return item,201

#     # for store in stores:
#     #     if store["name"] == name:
#     #         new_item= {"name" : request_data["name"], "price" : request_data["price"]}
#     #         store["item"].append(new_item)
#     #         return new_item,201
#     # return {"message": "error"},404


# @app.route("/item/<string:item_id>",methods=["GET"])
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         return{"message": "Item not found"},404
#     # for store in stores:
#     #     if store["name"] == name:
#     #         return { "item":store["item"]},201
#     # return {"message":"error"},404

# @app.route("/store/<string:store_id>",methods=["GET"])
# def get_store(store_id):
#     try:
#         return stores[store_id]
#     except KeyError:
#         return{"message": "Store not found"},404

# @app.route("/item/<string:item_id>",methods=["DELETE"])
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message": "Item deleted."}
#     except KeyError:
#         abort(404,message="Item not found")


# @app.route("/item/<string:item_id>",methods=["PUT"])
# def update_item(item_id):
#     item_data = request.get_json()
#     if "price" not in item_data or "name" not in item_data:
#         abort(400,message= "Bad request. Ensure 'price' and 'name' are included in the JSON payload.")
#     try:
#         item = items[item_id]
#         item |= item_data
#         return item
#     except KeyError:
#         abort(404,message = "Item not found.")


# @app.route("/store/<string:store_id>",methods=["DELETE"])
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "Store deleted."}
#     except KeyError:
#         abort(404,message="Store not found")

