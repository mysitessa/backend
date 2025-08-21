from data.db_session import create_session, global_init
from data.models import InitGames, Items, Weapons, Matches, Clients, Events, ItemPickups, Kills
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  
global_init()
session = create_session()

@app.route('/kills')
def get_kills():
    data = session.query(Kills).count()
    print(data)
    return jsonify({"kills":data})

@app.route('/players')
def get_players():
    data = session.query(Clients).count()
    print(data)
    return jsonify({"players":data})

    

if __name__ == '__main__':
    app.run(debug=True)

    