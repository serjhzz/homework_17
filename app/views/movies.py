from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import MovieSchema, Movie

movie_ns = Namespace('movies')

movie_schema = MovieSchema()


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        stmt = Movie.query
        if director_id:
            stmt = stmt.filter(Movie.director_id == director_id)
        if genre_id:
            stmt = stmt.filter(Movie.genre_id == genre_id)
        movies = stmt.all()
        return movie_schema.dump(movies, many=True), 200

    def post(self):
        movie_data = request.json
        new_movie = Movie(**movie_data)
        db.session.add(new_movie)
        db.session.commit()
        return f'Добавлен новый фильм, id: {new_movie.id}', 201


@movie_ns.route('/<int:mid>/')
class MovieView(Resource):
    def get(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return '', 404
        return movie_schema.dump(movie), 200

    def put(self, mid: int):
        movie = Movie.query.get(mid)

        if not movie:
            return '', 404

        movie_data = request.json

        movie.title = movie_data('title')
        movie.description = movie_data('description')
        movie.trailer = movie_data('trailer')
        movie.year = movie_data('year')
        movie.rating = movie_data('rating')
        movie.genre_id = movie_data('genre_id')
        movie.director_id = movie_data('director_id')

        db.session.add(movie)
        db.session.commit()

        return f'Фильм {mid} изменен', 204

    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return '', 404
        db.session.delete(movie)
        db.session.commit()
        return '', 204
