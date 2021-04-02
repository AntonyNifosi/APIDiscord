import flask
import sqlite3
import random

from flask import g, jsonify, request
from flasgger import Swagger

app = flask.Flask(__name__)
swagger = Swagger(app)

random.seed(15)
DATABASE = 'database/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def update_db(query, args=()):
    db = get_db()
    cur = db.cursor()
    cur.execute(query, args)
    db.commit()

def query_db(query, args=(), one=False):
    print(query)
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/wordpair', methods=['GET'])
def get_word_pair():
    """Return a random WordPair from the database
    ---
    responses:
      200:
        description: A pair of words
        schema:
            type: object
            properties:
                bystander_word:
                    type: string
                undercover_word:
                    type: string
    """
    total = query_db('SELECT COUNT(*) as COUNT FROM word_pairs', one=True)

    pair_db = query_db('SELECT bystander_word, undercover_word FROM word_pairs WHERE id = ?', [random.randint(1, total[0])], one=True)

    pair = {
        'bystander_word':pair_db[0],
        'undercover_word':pair_db[1]
    }
    return jsonify(pair)

@app.route('/user', methods=['GET'])
def get_users():
    """Return all users
    ---
    responses:
      200:
        description: All users
        schema:
        examples:
    """
    pair_db = query_db('SELECT * FROM users', one=False)

    return jsonify(pair_db)

@app.route('/ranking/<string:ranking_type>', methods=['GET'])
def get_rankings(ranking_type):
    """Return the ranking of the users
    ---
    parameters:
      - in: path
        name: ranking_type
        required: true
        schema:
            type: string
            example: "bystander_victory"
        required: true
        description: Type of ranking wanted
    responses:
      200:
        description: All users
    """
    pair_db = query_db('SELECT * FROM users ORDER BY ' + ranking_type + ' DESC', one=False)

    return jsonify(pair_db)


@app.route('/user/', methods=['POST'])
def add_user():
    """
    Post a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - u_id
            - username
          properties:
            u_id:
              type: string
              example: "208662022160777216"
            username:
              type: string
              description: The user username in Discord
              example: "kekun#2126"
    responses:
      200:
        description: User successfully added
        schema:
    """
    user = {
        'u_id':request.json['u_id'], 
        'username':request.json['username']
    } 

    update_db('INSERT INTO users (u_id, username) VALUES  (?, ?)', [user['u_id'], user['username']])

    return user

@app.route('/user/<string:u_id>', methods=['GET'])
def get_user(u_id):
    """
    Get the user ith the specified id
    ---
    parameters:
      - in: path
        name: u_id
        required: true
        schema:
            type: string
            example: "208662022160777216"
        required: true
        description: User id
    responses:
      200:
        description: A user
        schema:
            type: object
            properties:
                u_id:
                    type: string
                username:
                    type: string
                bystander_victory:
                    type: number
                undercover_victory:
                    type: number
    """
    print(u_id)
    user_db = query_db('SELECT * FROM users WHERE u_id = ?', [u_id], one=True)

    user = {
        'u_id':user_db[0],
        'username':user_db[1],
        'bystander_victory':user_db[2],
        'undercover_victory':user_db[3]
    }

    return jsonify(user)

@app.route('/user/<string:u_id>/achievements/', methods=['POST'])
def give_achievement(u_id):
    """
    Grant an achievement to the specified user
    ---
    parameters:
      - in: path
        name: u_id
        required: true
        schema:
            type: string
            example: "208662022160777216"
        required: true
        description: User
      - name: body
        in: body
        required: true
        schema:
          required:
            - a_id
          properties:
            a_id:
              type: number
              description: Achievement_id
              example: 1
    responses:
      200:
        description: Achievement successfully added
    """
    update_db('INSERT INTO users_achievements (u_id, a_id) VALUES (?, ?)', [u_id, request.json['a_id']])

    return "Sucess"

@app.route('/user/<string:u_id>/achievements', methods=['GET'])
def get_user_achievements(u_id):
    """Return all achievements of a user
    ---
    parameters:
      - in: path
        name: u_id
        required: true
        schema:
            type: string
            example: "208662022160777216"
        required: true
        description: User id 
    responses:
      200:
        description: All achievements
    """
    achievements_db = query_db('SELECT * FROM users_achievements NATURAL JOIN achievements WHERE u_id = ?', [u_id])
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
    """Return all achievements 
    ---
    responses:
      200:
        description: All achievements
    """
    achievements_db = query_db('SELECT * FROM achievements')

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

@app.route('/user/<string:u_id>/win', methods=['PUT'])
def add_win(u_id):
    """
    Grant a win to the specified user
    ---
    parameters:
      - in: path
        name: u_id
        required: true
        schema:
            type: string
            example: "208662022160777216"
        required: true
        description: User id 
      - name: body
        in: body
        required: true
        schema:
          required:
            - win_type
          properties:
            win_type:
              type: string
              description: Achievement_id
              example: undercover_victory
    responses:
      200:
        description: Victory successfully added
    """
    win_type = request.json['win_type']
    actual = query_db('SELECT ' + win_type + ' FROM users WHERE u_id = ?',  [u_id], one=True)
    update_db('UPDATE users SET ' + win_type + ' = ? + 1 WHERE u_id = ? ', [actual[0], u_id])

    return "Success"

app.config["DEBUG"] = True
app.run()
