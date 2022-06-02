from unicodedata import name
import requests
from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_parameter


app = Flask(__name__, static_url_path="/static")

api_key = "05159cb3f7a10f4e876ea3579592cd55"


def get_movies(page):

    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&page={page}"
    response = requests.get(url)
    print(url)
    data = response.json()
    return data["results"]


def get_tv_shows(page):
    url = f"https://api.themoviedb.org/3/tv/popular?api_key={api_key}&page={page}"
    response = requests.get(url)
    data = response.json()
    return data["results"]


def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits,videos"
    response = requests.get(url)
    data = response.json()
    return data


def get_tv_show_details(tv_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={api_key}&append_to_response=credits,videos"
    response = requests.get(url)
    data = response.json()
    return data


def search_movie(query, page):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}&page={page}"
    response = requests.get(url)
    data = response.json()
    return data["results"]


def search_shows(query, page):
    url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={query}&page={page}"
    response = requests.get(url)
    data = response.json()
    return data["results"]


# create a route
@app.route("/movies")
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    movies = get_movies(page)

    pagination = Pagination(page=page, total=4500, css_framework="bootstrap4")
    return render_template("movies.html", movies=movies, pagination=pagination)


@app.route("/shows")
def tv():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    tv_shows = get_tv_shows(page)

    pagination = Pagination(page=page, total=450, css_framework="bootstrap4")
    return render_template("shows.html", tv_shows=tv_shows, pagination=pagination)


@app.route("/get_movie")
def get_movie():
    movie_id = request.args.get("id")
    movie = get_movie_details(movie_id)
    return render_template("MovieDetails.html", movie=movie, len=len)


@app.route("/get_show")
def get_tv():
    tv_id = request.args.get("id")
    tv = get_tv_show_details(tv_id)
    if tv["seasons"][0]["name"] == "Specials":
        tv["seasons"].pop(0)
    return render_template("ShowDetails.html", tv=tv, len=len)


@app.route("/search_movies")
def search():
    query = request.args.get("query")
    page = request.args.get(get_page_parameter(), type=int, default=1)
    movies = search_movie(query, page)
    pagination = Pagination(page=page, total=100, css_framework="bootstrap4")

    return render_template("movies.html", movies=movies, pagination=pagination)


@app.route("/search_shows")
def search_showss():
    query = request.args.get("query")
    page = request.args.get(get_page_parameter(), type=int, default=1)
    tv_shows = search_shows(query, page)

    pagination = Pagination(page=page, total=100, css_framework="bootstrap4")

    return render_template("shows.html", tv_shows=tv_shows, pagination=pagination)


@app.route("/play_episode")
def play_episode():
    tmdb_id = request.args.get("tmdb_id")
    season_no = request.args.get("season")
    episode_no = request.args.get("episode")
    show_name = request.args.get("name")
    url = f"https://openvids.io/tmdb/episode/{tmdb_id}-{season_no}-{episode_no}"
    return render_template(
        "episodePlayer.html",
        url=url,
        show_name=show_name,
        season_no=season_no,
        episode_no=episode_no,
    )


if __name__ == "__main__":
    app.run(debug=True)
