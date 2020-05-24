import argparse
import asyncio
import pathlib
import requests
import socket

from typing import Dict, TypedDict, Union

"""
Type Descriptions

-*- any not listed are imported from modules -*-
    
DiscoveryData:
    Cache-Control: str
    ST: str
    USN: str
    Ext: str
    Server: str
    LOCATION: str
    device-group.roku.com: str
    WAKEUP: str
"""


class EcpData(TypedDict):
    """
    *Attributes
        data: dict
        xml: str
    """
    data: dict
    xml: str


class DeviceData(TypedDict):
    """
    *Attributes
        device_info: EcpData
        apps: EcpData
        active_app: EcpData
        media_player: EcpData
    """
    device_info: EcpData
    apps: EcpData
    active_app: EcpData
    media_player: EcpData


class RokuApp(TypedDict):
    """
    *Attributes
        id: str
        type: str
        subtype: str
        version: str
        name: str
    """
    id: str
    type: str
    subtype: Union[None, str]
    version: str
    name: str
    active: bool


class Player(TypedDict):
    """
    *Attributes
        error: str
        state: str
    """
    error: str
    state: str
    is_live: bool
    format: dict

ArgList = argparse.Namespace
ArgParser = argparse.ArgumentParser
SocketConnection = socket.socket
DiscoveryData = Dict[str, str]
Response = requests.models.Response
Task = asyncio.Task
PathType = pathlib.Path
DeviceInfoAttribute = Union[str, None]
