from data.db_session import create_session, global_init
from data.models import InitGames, Items, Weapons, Matches, Clients, Events, ItemPickups, Kills
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  
global_init()
session = create_session()

def get_data():
    data = session.query(Clients).all()
    for client in data:
        print(f"айди клиента: {client.id}, имя: {client.name}, айди матча: {client.match_id}")

        return jsonify({
            'айди клиента': client.id,
            'имя': client.name,
            'айди матча': client.match_id
        }
        )
    
if __name__ == '__main__':
    app.run(debug=True)
    