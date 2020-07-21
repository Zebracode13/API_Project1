from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
                        type=float,
                        required=True,
                        help="This field should not be empty!"
                        )

    parser.add_argument('store_id', 
                        type=int,
                        required=True,
                        help="Every item needs an id#"
                        )

    @jwt_required() #creates a token for send a sucre message
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}

   
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name'{}'already exists.".format(name)}

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return{"message": "an error happend"}
        return item.json(), 201

    def delete(self, name):   
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "{} has been deleted".format(name)}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item:
            item.price = data['price']
        else:
            item =  ItemModel(name, **data)
        item.save_to_db()

        return item.json()

    
#create a new class 
class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}