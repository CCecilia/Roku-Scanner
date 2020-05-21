import argparse
import asyncio
import pathlib
import requests
import socket

from typing import Dict, TypedDict

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


ArgList = argparse.Namespace
ArgParser = argparse.ArgumentParser
SocketConnection = socket.socket
DiscoveryData = Dict[str, str]
Response = requests.models.Response
Task = asyncio.Task
PathType = pathlib.Path
