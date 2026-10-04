import ssl
from typing import Any
from urllib.parse import ParseResult

from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode


class MQTTClient:
    def __init__(self, url: ParseResult, topic: str):
        self.topic = topic

        self.msg_queue = set()

        self.mqttc = Client(CallbackAPIVersion.VERSION2)
        self.mqttc.username_pw_set(url.username, url.password)
        self.mqttc.tls_set(
            certfile=None,
            keyfile=None,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLS_CLIENT,
        )
        self.mqttc.on_publish = self.__on_publish__
        self.mqttc.user_data_set(self.msg_queue)

        self.__connect__(url)

    def __connect__(self, url: ParseResult):
        assert url.hostname is not None

        self.mqttc.connect(host=url.hostname, port=url.port or 1883)
        self.mqttc.loop_start()

    def __on_publish__(
        self,
        _client: Client,
        _userdata: Any,
        mid: int,
        _reason_code: ReasonCode,
        _properties: Properties,
    ):
        self.msg_queue.remove(mid)

    def publish(self, msg: str | None = None):
        self.msg_queue.add(self.mqttc.publish(self.topic, msg).mid)
