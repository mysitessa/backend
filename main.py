from data.db_session import create_session, global_init
from data.models import InitGames, Items, Weapons, Matches, Clients, Events, ItemPickups, Kills
from flask import Flask, jsonify
from flask_cors import CORS
from collections import Counter
import logging


app = Flask(__name__)
CORS(app)  
global_init()
session = create_session()

#запись логов
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('main.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(format)

logger.addHandler(file_handler)

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('main.log', encoding='utf-8'),
                             logging.StreamHandler()])

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

@app.route('/matches')
def get_matches():
    data = session.query(InitGames).count()
    print(data)
    return jsonify({"matches":data})


@app.route('/top_maps')
def get_top_maps():
    map_names = [i[0] for i in session.query(InitGames.map_name).all()]
    maps_count = Counter(map_names)
    maps_count = maps_count.most_common()
    #print("maps_count:", maps_count)
    
    while len(maps_count) < 3:
        maps_count.append(("не занято", 0))
    
    sp_most_popular_maps = [f"{i[0]} - {i[1]}" for i in maps_count[:3]]
    #print("sp_most_popular_maps", sp_most_popular_maps)
    
    return jsonify({
        "1.": sp_most_popular_maps[0],
        "2.": sp_most_popular_maps[1],
        "3.": sp_most_popular_maps[2]
    })

if __name__ == '__main__':
    app.run(debug=True)

    