import argparse
import asyncio
import socket
from pathlib import Path
from typing import Dict, Union

import requests

Address = Dict[str, str]
ArgList = argparse.Namespace
ArgParser = argparse.ArgumentParser
SocketConnection = socket.socket
"""
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
DiscoveryData = Dict[str, Union[str, Address]]
Response = requests.models.Response
Task = asyncio.Task
PathType = Path
