from flask import jsonify
from flask_restful import Resource


class HealthCheck(Resource):

    def post(self):
        return jsonify("OK")
