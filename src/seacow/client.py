import ssl
from typing import Any

import click
from paho.mqtt.client import CallbackAPIVersion, Client, MQTTMessage
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode


# The callback for when the client receives a CONNACK response from the server.
def on_connect(
    client: Client,
    _userdata: Any,
    _flags: dict[str, Any],
    reason_code: ReasonCode,
    _properties: Properties | None,
):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("seacow/trigger")


# The callback for when a PUBLISH message is received from the server.
def on_message(_client: Client, _userdata: Any, msg: MQTTMessage):
    print(msg.topic + " " + str(msg.payload))


@click.command()
@click.option("--host", "-h")
@click.option("--port", "-p", type=click.INT, default=8883)
@click.option("--username", "-u")
@click.option("--password", prompt=True, hide_input=True)
def client(host: str, port: int, username: str, password: str):
    mqttc = Client(CallbackAPIVersion.VERSION2)
    mqttc.username_pw_set(username, password)
    mqttc.tls_set(
        certfile=None,
        keyfile=None,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLS_CLIENT,
    )

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(host, port)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    mqttc.loop_forever()
