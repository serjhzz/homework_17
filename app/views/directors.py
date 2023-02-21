from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import DirectorSchema, Director

director_ns = Namespace('directors')

director_schema = DirectorSchema()


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return director_schema.dump(directors, many=True), 200

    def post(self):
        director_data = request.json
        new_director = Director(**director_data)
        db.session.add(new_director)
        db.session.commit()
        return f'Добавлен новый фильм, id: {new_director.id}', 201


@director_ns.route('/<int:did>/')
class DirectorView(Resource):
    def get(self, did: int):
        director = Director.query.get(did)
        if not director:
            return '', 404
        return director_schema.dump(director), 200

    def put(self, mid: int):
        director = Director.query.get(mid)

        if not director:
            return '', 404

        director_data = request.json

        director.name = director_data('name')

        db.session.add(director)
        db.session.commit()

        return f'Директор {mid} изменен', 204

    def delete(self, did: int):
        director = Director.query.get(did)
        if not director:
            return '', 404
        db.session.delete(director)
        db.session.commit()
        return '', 204
