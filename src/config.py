import toml, sys, logging
from marshmallow import Schema, fields, post_load, EXCLUDE
from marshmallow import exceptions as marsh_exc
from dataclasses import dataclass
from typing import Union, Tuple
from ipaddress import IPv4Address, IPv6Address
from marshmallow_enum import EnumField
from enum import Enum

logger = logging.getLogger(__name__)

class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40

class ConfigSchema(Schema):
    log_level = EnumField(LogLevel, missing=LogLevel.WARNING)
    listen_addr = fields.IP(required=True)
    log_port_range = fields.Tuple((fields.Integer(), fields.Integer()), required=True)

    @post_load
    def make_config(self, data, **kwargs):
        return Config(**data)

@dataclass
class Config:
    log_level: LogLevel
    listen_addr: Union[IPv4Address, IPv6Address]
    log_port_range: Tuple[int, int]

class ConfigStore:
    cfg: Config

def load_config_from_file():
    try:
        # TODO: add a CLI param for the config file path
        with open("config.toml", "r") as f:
            try:
                d = toml.loads("".join(f.readlines()))
                schema = ConfigSchema()
                return schema.load(d, unknown=EXCLUDE)
            except toml.decoder.TomlDecodeError as e:
                logger.error("Bad TOML syntax in config file : {}".format(e))
            except marsh_exc.ValidationError as e:
                for field, err in e.normalized_messages().items():
                    logger.error("Validation errors encountered on field '{}': {}".format(field, ",".join(err).lower()))
            sys.exit(1) 
    except IOError:
        logger.error("Could not open config.toml file in your current working dir")
        sys.exit(1)

