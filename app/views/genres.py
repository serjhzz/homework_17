from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import GenreSchema, Genre

genre_ns = Namespace('genres')

genre_schema = GenreSchema()


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genre_schema.dump(genres, many=True), 200

    def post(self):
        genre_data = request.json
        new_genre = Genre(**genre_data)
        db.session.add(new_genre)
        db.session.commit()
        return f'Добавлен новый жанр, id: {new_genre.id}', 201


@genre_ns.route('/<int:gid>/')
class GenreView(Resource):
    def get(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return '', 404
        return genre_schema.dump(genre), 200

    def put(self, gid: int):
        genre = Genre.query.get(gid)

        if not genre:
            return '', 404

        genre_data = request.json

        genre.name = genre_data('name')

        db.session.add(genre)
        db.session.commit()

        return f'Жанр {gid} изменен', 204

    def delete(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return '', 404
        db.session.delete(genre)
        db.session.commit()
        return '', 204
