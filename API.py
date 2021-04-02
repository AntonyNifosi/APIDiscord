import flask
import sqlite3
import random

from flask import g, jsonify, request

app = flask.Flask(__name__)

random.seed(15)
DATABASE = 'database/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/wordpair', methods=['GET'])
def get_word_pair():
    total = query_db('SELECT COUNT(*) as COUNT FROM word_pair', one=True)

    pair_db = query_db('SELECT bystander_word, undercover_word FROM word_pair WHERE id = ?', [random.randint(1, total[0])], one=True)

    pair = {
        'bystander_word':pair_db[0],
        'undercover_word':pair_db[1]
    }
    return jsonify(pair)

@app.route('/user/', methods=['POST'])
def add_user():
    query_db('INSERT INTO user (u_id, username) VALUES  (?, ?)', [request.form['u_id'], request.form['username']])

@app.route('/user/<int:u_id>', methods=['GET'])
def get_user(u_id):
    user_db = query_db('SELECT * FROM user WHERE u_id = ?', [u_id], one=True)

    user = {
        'u_id':user_db[0],
        'username':user_db[1],
        'bystander_victory':user_db[2],
        'undercover_victory':user_db[3]
    }

    return jsonify(user)

@app.route('/user/<int:u_id>/achievements/', methods=['POST'])
def give_achievement(u_id):
    query_db('INSERT INTO user_achievement (u_id, a_id) VALUES (?, ?)', [u_id, request.form['a_id']])

@app.route('/user/<int:u_id>/achievements', methods=['GET'])
def get_user_achievements(u_id):
    achievements_db = query_db('SELECT * FROM user_achievement NATURAL JOIN achievement WHERE u_id = ?', [u_id])
    achievements = []

    for achievement in achievements_db :
        achievements.append(
            {
                'a_id':achievement[0],
                'title':achievement[1],
                'description':achievement[2]
            }
        )

    return jsonify(achievements)

@app.route('/achievements', methods=['GET'])
def get_achievements():
    achievements_db = query_db('SELECT * FROM achievement')

    achievements = []

    for achievement in achievements_db :
        achievements.append(
            {
                'a_id':achievement[0],
                'title':achievement[1],
                'description':achievement[2]
            }
        )

    return jsonify(achievements)

@app.route('/user/<int:u_id>/win', methods=['PUT'])
def add_win(u_id):
    query_db('UPDATE user SET ? = (? + 1) WHERE u_id = ? ', request.form['win'] [u_id])

app.config["DEBUG"] = True
app.run()
