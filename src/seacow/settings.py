from environs import Env

env = Env(prefix="SEACOW_")
env.read_env()

url_kwargs = {"schemes": ["mqtt", "mqtts"], "require_tld": False}

settings = {
    "DEBUG": env.bool("DEBUG", default=False),
    "MQTT_URL": env.url("MQTT_URL", **url_kwargs),
}
