import flask
from flask_cors import CORS, cross_origin

import requests as req
import re

from grape import Grape

grape = Grape()
app = flask.Flask(__name__)
CORS(app)

@app.get("/")
def welcome():
    return flask.jsonify({"message": "Hello Friend."}), 200

@app.post("/api/v1/nick-checker")
def checker():
    response = flask.request.json
    region = response["region"]
    nicks = response["nicks"]
    result = grape.start_nick_checker(nicks, region)
    if result == False:
        return flask.jsonify({"error": True, "message": "you can't check more than 300 nicks."}), 400
    else:
        return flask.jsonify(result), 200

@app.post("/api/v1/generate-nick-list")
def generate_nick_list():
    response = flask.request.json
    if str(response["type"]).upper() == "CHAMPIONS":
        if response["raw"] == True:
            nick_list = []
            current_patch = req.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]    
            champions = req.get(f"http://ddragon.leagueoflegends.com/cdn/{current_patch}/data/en_US/champion.json").json()
            for champion in champions["data"]:
                champion_name = re.sub(r'[^a-zA-Z]', '', champion)
                nick_list.append(champion_name)            
            
            return flask.jsonify(nick_list)

        elif response["raw"] == False:
            nick_list = ""
            current_patch = req.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]    
            champions = req.get(f"http://ddragon.leagueoflegends.com/cdn/{current_patch}/data/en_US/champion.json").json()
            for champion in champions["data"]:
                champion_name = re.sub(r'[^a-zA-Z]', '', champion)
                nick_list += f"{champion_name}<br>"
            
            return nick_list

    elif str(response["type"]).upper() == "BOT":
        if response["raw"] == True:
            nick_list = []
            current_patch = req.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]    
            champions = req.get(f"http://ddragon.leagueoflegends.com/cdn/{current_patch}/data/en_US/champion.json").json()
            for champion in champions["data"]:
                champion_name = re.sub(r'[^a-zA-Z]', '', champion)
                nick_list.append(champion_name + " Bot")            
            
            return flask.jsonify(nick_list)

        elif response["raw"] == False:
            nick_list = ""
            current_patch = req.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]    
            champions = req.get(f"http://ddragon.leagueoflegends.com/cdn/{current_patch}/data/en_US/champion.json").json()
            for champion in champions["data"]:
                champion_name = re.sub(r'[^a-zA-Z]', '', champion)
                nick_list += f"{champion_name} Bot<br>"
            
            return nick_list

    elif str(response["type"]).upper() == "ENGLISH":
        if response["raw"] == True:
            nick_list = req.get("https://random-words.irftools.repl.co/word?number=218").json()
            return flask.jsonify(nick_list)
        elif response["raw"] == False:
            nick_list = ""
            get_random_nicks = req.get("https://random-words.irftools.repl.co/word?number=218").json()
            for nick in get_random_nicks:
                if len(nick) > 15:
                    continue
                else:
                    nick_list += f"{nick}<br>"
            return nick_list
        
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
