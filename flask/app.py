from flask import Flask, render_template
import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "doubanTop250.db")


def connect_db():
    return sqlite3.connect(db_path)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')
def home():
    return index()


@app.route('/movie')
def movie():
    moviesList = []
    conn = connect_db()
    cur = conn.cursor()
    sql = "select * from movie250"
    data = cur.execute(sql)
    for item in data:
        moviesList.append(item)
    cur.close()
    conn.close()
    return render_template("movie.html", movies=moviesList)


@app.route('/score')
def score():
    return render_template("score.html")


@app.route('/word')
def word():
    return render_template("word.html")


@app.route('/team')
def team():
    return render_template("team.html")


if __name__ == '__main__':
    app.run()
