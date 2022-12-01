import requests
from flask import Flask, request, render_template
from utils.configing import readconf
app = Flask(__name__)

PATH = 'data'


def on_message(message):
    config_file = f"{serwer}.ini"
    m_decode = str(message.payload.decode("utf-8"))
    if int(m_decode) > int(readconf(config_file, "breakpoint")):
        signal = {"signal": 1}
        new_data = int(m_decode)
        new_data -= int(readconf(config_file, "active"))
        message_signal = readconf(config_file, "message")
        message_dict = {"message": message_signal}
        with open(f"{PATH}/data{serwer}.txt", "a") as file:
            file.write(str(new_data))
            file.write("\n")
        requests.post("http://127.0.0.1:5000/updater/sygnal", message_dict)
        requests.post("http://127.0.0.1:5000/odbieranie", signal)
    else:
        signal = {"signal": 1}
        requests.post("http://127.0.0.1:5000/odbieranie", signal)
    print(f"Received message:{m_decode}")
    return m_decode


@app.route('/', methods=['GET', 'POST'])
def main():
    data = request.form.to_dict()
    data = data["data"]
    config_file = f"{serwer}.ini"
    new_data = int(data)
    if int(new_data):
        data = {"data": data}
        print(data)
        message_signal = readconf(config_file, "message")
        message_dict = {"message": message_signal}
        requests.post("http://127.0.0.1:5000/updater/sygnal", message_dict)
        requests.post("http://127.0.0.1:5000/odbieranie", params=data)
    else:
        data = {"data": data}
        requests.post("http://127.0.0.1:5000/odbieranie", params=data)
    return render_template("agregator.html")


@app.route('/serwer', methods=['GET', 'POST'])
def serwer():
    data = request.args.to_dict()
    global serwer
    serwer = data["serwer"]
    print(serwer)
    return render_template("agregator.html")


app.run(debug=True, port=5060)
