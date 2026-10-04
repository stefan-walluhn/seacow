from flask import Flask, render_template

from seacow.mqtt import MQTTClient
from seacow.settings import settings

app = Flask(__name__)
app.config.from_mapping(settings)

mqtt_client = MQTTClient(app.config["MQTT_URL"], "seacow/trigger")


@app.get("/")
def show():
    return render_template("show.html")


@app.post("/trigger")
def trigger():
    mqtt_client.publish()
    return {"triggered": True}, 201
