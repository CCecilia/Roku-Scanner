import asyncio
import json

import requests
import xmltodict  # type: ignore

from .custom_types import DiscoveryData, Response, Task


class Roku:
    def __init__(self, location: str, discovery_data: DiscoveryData):
        self.location: str = location
        self.discovery_data: DiscoveryData = discovery_data
        self.data: dict = {}

    def fetch_data(self) -> None:
        self.data = asyncio.run(fetch_all_data(self.location))

    def as_json(self) -> str:
        device_name: str = 'unknown-device'
        try:
            device_name = self.data["device_info"]["data"]["device-info"]["default-device-name"]
        except KeyError:
            pass

        temp: dict = {}

        for data_set in self.data.items():
            data: dict = data_set[1].get('data', None)
            if data is not None:
                temp.update(data_set[1]['data'])

        return json.dumps({device_name: temp})

    def as_xml(self) -> str:
        device_name: str = 'unknown-device'
        try:
            device_name = self.data["device_info"]["data"]["device-info"]["default-device-name"]
        except KeyError:
            pass

        temp: str = f'<{device_name}>\n'

        for data_set in self.data.items():
            xml: str = data_set[1].get('xml', None)
            if xml is not None:
                temp += data_set[1]['xml'].replace('<?xml version="1.0" encoding="UTF-8" ?>', '')

        temp += f'</{device_name}>\n'

        return temp


async def fetch_all_data(roku_location: str) -> dict:
    device_info: Task = asyncio.create_task(fetch_device_info(roku_location))
    apps: Task = asyncio.create_task(fetch_apps(roku_location))
    active_app: Task = asyncio.create_task(fetch_active_app(roku_location))
    media_player: Task = asyncio.create_task(fetch_media_player(roku_location))

    return {
        'device_info': await device_info,
        'apps': await apps,
        'active_app': await active_app,
        'media_player': await media_player
    }


async def fetch_device_info(roku_location: str) -> dict:
    resp: Response = requests.get(f'{roku_location}query/device-info',
                                  headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        device_data_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': device_data_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}


async def fetch_apps(roku_location: str) -> dict:
    resp: Response = requests.get(f'{roku_location}query/apps',
                                  headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        apps_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': apps_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}


async def fetch_active_app(roku_location: str) -> dict:
    resp: Response = requests.get(f'{roku_location}query/active-app',
                                  headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        active_app_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': active_app_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}


async def fetch_media_player(roku_location: str) -> dict:
    resp: Response = requests.get(f'{roku_location}query/media-player',
                                  headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        media_player_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': media_player_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}
