from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask("pre-fixlist")
api = Api(app)

class PrefixListList(Resource):

    def get(self):
        # Return a list of all prefix lists we know about
        return None

class PrefixList(Resource):

    def get(self, listid):
        # Return a list of versions 
        return None

    def post(self):
        # Create a new prefixlist
        return None

    def put(self, listid):
        # Update a prefixlist
        return None

    def delete(self, listid):
        return None

class PrefixListVersion(Resource):

    def get(self, listid, version):
        # Return a list of prefixes contained in the specific version of the prefixlist
        return None

api.add_resource(PrefixListList, "/prefixlist")
api.add_resource(PrefixList, "/prefixlist/<int:listid>")
api.add_resource(PrefixListVersion, "/prefixlist/<int:listid>/<string:version>")

if __name__ == '__main__':
    app.run(debug=True)
