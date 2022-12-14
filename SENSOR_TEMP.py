import time
import requests
from flask import Flask, request
from PREDCITING import create_data
from utils.configing import updateconf, readconf
from utils.data_menager import read_csv

app = Flask(__name__)
SOURCE = 'data/1temp.csv'

data_list = read_csv(SOURCE)
config_file = "5050.ini"

config_keys = {
    "switch": "wlacznik",
}

@app.route('/wlacznik', methods=['GET', 'POST'])
def wlacznik():
    client_data = request.args.to_dict()
    if "wlacz" in client_data:
        global wlacz
        wlacz = client_data["wlacz"]
        validation = [
            "True" == wlacz,
            "False" == wlacz
        ]
        if any(validation):
            topic = config_keys["switch"]
            updateconf(config_file, topic, client_data['wlacz'])
            status = readconf(config_file, topic)
            if status == 'True':
                for data in data_list:
                    status = readconf(config_file, topic)
                    if status == 'True':
                        print(create_data(float(data)))
                        data = {"data": data}
                        requests.post("http://127.0.0.1:5060/", data=data)
                    else:
                        return {"1": 1}
                    time.sleep(1)
            else:
                return {"1": 1}
        else:
            return {
                       "status": 400,
                       "message": "Wybrana opcja nie jest obslugiwana"
                   }, 400
    else:
        return {
                   "status": 400,
                   "message": "Zle argumenty"
               }, 400

app.run(port=5050, debug=True)
