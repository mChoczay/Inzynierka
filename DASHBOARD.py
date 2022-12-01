import requests
from flask import Flask, request, render_template

from utils.configing import updateconf, readconf
from utils.counter import counter
from utils.newconfig import createConfig
from utils.newserwerconfig import createServerConfig

serwer_file = "serwers.ini"
app = Flask(__name__)


def on_message(message):
    m_decode = str(message.payload.decode("utf-8"))
    print(f"Received message:{m_decode}")
    return m_decode


@app.route('/')
def main():
    try:
        with open('serwers.ini') as f:
            f.readlines()
    except IOError:
        createServerConfig('serwers')
    return render_template("main.html")


@app.route('/odbieranie', methods=['GET', 'POST'])
def odbieranie():
    client_data = request.args.to_dict()
    print(client_data['data'])
    return render_template("index.html")


@app.route('/panel', methods=["GET", "POST"])
def panel():
    name = request.form.to_dict()
    createConfig(name['rejestracja'])
    server_number = str(abs(counter()))
    print(server_number)
    new_serwer = name['rejestracja']
    updateconf(serwer_file, server_number, new_serwer)
    global current_serwer
    current_serwer = new_serwer
    print(current_serwer)
    return render_template("index.html")


@app.route("/switch", methods=["GET", "POST"])
def wlacznik():
    if request.method == "GET":
        return render_template("index.html")
    else:
        data = request.form.to_dict()
        requests.post(f"http://127.0.0.1:{current_serwer}/wlacznik", params=data)
        return render_template("index.html")


@app.route("/sourcestatus", methods=["GET", "POST"])
def status():
    # noinspection PyShadowingNames
    status = readconf(f'{current_serwer}.ini', "wlacznik")
    return render_template("index.html", value2=status, value3=current_serwer)


@app.route('/updater/sygnal', methods=['GET', 'POST'])
def syngal():
    client_data = request.form.to_dict()
    print(client_data['message'])
    return render_template("index.html")


@app.route("/updater", methods=["GET", "POST"])
def aktuator():
    if request.method == "GET":
        return render_template("index.html")
    else:
        data = request.form.to_dict()
        requests.post(f"http://127.0.0.1:{current_serwer}/aktuator", params=data)
        return render_template("index.html")


@app.route('/serwer', methods=["GET", "POST"])
def serwer():
    number = request.form.to_dict()['serwer']
    server_adress = readconf(serwer_file, number)

    global current_serwer
    current_serwer = server_adress
    data = {"serwer": current_serwer}
    requests.post("http://127.0.0.1:5060/serwer", params=data)

    print(current_serwer)

    return render_template("index.html", value=number)


@app.route('/wyswietlanie', methods=["GET", "POST"])
def wyswietlanie():
    n = int(request.form.to_dict()['wyswietlanie'])
    file = open("data/data5050.txt", "r")
    for i in file:
        print(i)
        n -= 1
        if n <= 0:
            break
    return render_template("index.html")


app.run(debug=True)
