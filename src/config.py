import toml, sys
from marshmallow import Schema, fields, post_load, EXCLUDE
from marshmallow import exceptions as marsh_exc
from dataclasses import dataclass
from typing import Union, Tuple
from ipaddress import IPv4Address, IPv6Address

class ConfigSchema(Schema):
    listen_addr = fields.IP(required=True)
    log_port_range = fields.Tuple((fields.Integer(), fields.Integer()))

    @post_load
    def make_config(self, data, **kwargs):
        return Config(**data)

@dataclass
class Config:
    listen_addr: Union[IPv4Address, IPv6Address]
    log_port_range: Tuple[int, int]

class ConfigStore:
    current: Config

def populate_config():
    with open("config.toml", "r") as f:
        try:
            d = toml.loads("".join(f.readlines()))
            schema = ConfigSchema()
            ConfigStore.current = schema.load(d, unknown=EXCLUDE)
        except toml.decoder.TomlDecodeError as e:
            print("Bad TOML syntax in config file : {}".format(e))
            sys.exit(1)
        except marsh_exc.ValidationError as e:
            print()
            print("The following validation errors were encountered in config file:")
            for k,v in e.normalized_messages().items():
                print("  - {}: {}".format(k, ",".join(v).lower()))

            print()
            sys.exit(1)

    #print("Could not open config.toml file in your current working dir")
    #sys.exit(1)


