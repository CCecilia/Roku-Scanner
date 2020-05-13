import argparse
import asyncio
import socket
from pathlib import Path
from typing import Dict

import requests

ArgList = argparse.Namespace
ArgParser = argparse.ArgumentParser
SocketConnection = socket.socket
DiscoveryData = Dict[str, any]
Response = requests.models.Response
Task = asyncio.Task
PathType = Path
