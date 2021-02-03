from flask import Flask
from flask import jsonify, request, json

from app.models.movies_model import Film
from app import app

import os


@app.route('/')

@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/movies', methods=['GET'])
def get_all_movies():
    all_movies = Film.get_all_films()
    return jsonify(
        movies = [movie.films_serializer for movie in all_movies]
        )

@app.route('/movies/<int:film_id>', methods=['GET'])
def get_film(film_id):
    movie = Film.get_one_film(film_id)
    return jsonify(movie)

@app.route("/submit_film", methods=["POST"])
def submit_film():
    incoming = request.get_json()

    print(incoming, "hello incoming")
    success, id = Film.save(Film (
        incoming["film_name"],
        incoming["img_url"],
        incoming["release_year"],
        incoming["summary"],
        incoming["director"],
        incoming["genre"],
        incoming["rating"],
        incoming["film_runtime"],
        incoming["meta_score"]
        ))

    if not success:
        return jsonify(message="Error submitting film", id=None), 409

    return jsonify(success=True, id=id)

@app.route("/delete_film/<int:film_id>", methods=["DELETE", "POST"])
def delete_film(film_id):
    success = Film.delete(film_id)
    if not success:
        return jsonify(message="Error deleting film"), 409

    return jsonify(success="Movie deleted!")


@app.route("/edit_film/<int:film_id>", methods=["POST", "PUT"])
def edit_film(film_id):
    incoming = request.get_json()

    print(film_id, incoming, "hello incoming")

    success = Film.update(film_id, Film(
        incoming["film_name"],
        incoming["img_url"],
        incoming["release_year"],
        incoming["summary"],
        incoming["director"],
        incoming["genre"],
        incoming["rating"],
        incoming["film_runtime"],
        incoming["meta_score"]
        ))

    if not success:
        return jsonify(message="Error editing film, could not find the movie"), 409

    return jsonify(message="Movie updated!")