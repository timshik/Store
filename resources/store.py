from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the store."}

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"massage": "Store deleted"}


class StoreList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
