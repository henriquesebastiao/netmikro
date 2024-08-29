from ipaddress import IPv4Address
from typing import Annotated

from pydantic import BaseModel, Field, IPvAnyAddress

PortInt = Annotated[int, Field(ge=0, le=65535)]


class Auth(BaseModel):
    host: IPvAnyAddress
    username: str
    password: str
    port: int
    global_delay_factor: float = 0


class Port(BaseModel):
    port: PortInt


class IfRouterboard(BaseModel):
    model: str
    revision: str
    serial_number: str
    firmware_type: str
    factory_firmware: str
    current_firmware: str
    upgrade_firmware: str


class License(BaseModel):
    software_id: str
    level: int
    features: str


class Resources(BaseModel):
    cpu: str
    cpu_frequency: int
    memory: int
    storage: int
    architecture: str
    board_name: str
    version: str


class NTPClient(BaseModel):
    enabled: bool
    mode: str
    servers: list[IPv4Address]
    vrf: str
    freq_diff: int
    status: str
    synced_server: IPv4Address
    synced_stratum: int
    system_offset: int


class NTPServer(BaseModel):
    enabled: bool
    broadcast: bool
    multicast: bool
    manycast: bool
    broadcast_address: IPv4Address | None
    vrf: str
