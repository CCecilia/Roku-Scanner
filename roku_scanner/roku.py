# coding=utf-8
import asyncio
import json
import requests
import xmltodict  # type: ignore

from collections import OrderedDict
from typing import List, Dict, Union

from .custom_types import DeviceInfoAttribute, DiscoveryData, EcpData, Player, Response, RokuApp, Task


class Roku:
    """
    Gets detailed device information and handles formatting.

    *Attributes:
        advertising_id (DeviceInfoAttribute): Device advertising id aka RIDA.
        apps (List[RokuApp] | None): List of any apps installed on device.
        build_number (DeviceInfoAttribute): Firmware version.
        can_use_wifi_extender (DeviceInfoAttribute): Can the device use a wifi extender.
        clock_format (DeviceInfoAttribute): Clock format of device 12 | 24 hour.
        country (DeviceInfoAttribute): Country code set on device.
        data (dict): Fetched data from ECP requests.
        davinci_version (DeviceInfoAttribute): Version of Davinci used.
        developer_enabled (DeviceInfoAttribute): Check if developer mode is active on device.
        default_device_name (DeviceInfoAttribute): Default name used device
        device_id (DeviceInfoAttribute): Unique Roku device ID.
        discovery_data (DiscoveryData): Device discovery data. See custom_types
        expert_pq_enabled (DeviceInfoAttribute):
        find_remote_is_possible (DeviceInfoAttribute): If device has find remote ping capability.
        friendly_device_name (DeviceInfoAttribute): Device name given by user.
        friendly_model_name (DeviceInfoAttribute): Friendly model name.
        grandcentral_version (DeviceInfoAttribute):
        has_mobile_screensaver (DeviceInfoAttribute):
        has_play_on_roku (DeviceInfoAttribute):
        has_wifi_extender (DeviceInfoAttribute):
        has_wifi_5G_support (DeviceInfoAttribute):
        headphones_connected (DeviceInfoAttribute):
        is_stick (DeviceInfoAttribute): Is the device a streaming stick.
        is_tv (DeviceInfoAttribute): Is the device a TV.
        keyed_developer_id (DeviceInfoAttribute):
        language (DeviceInfoAttribute): Language set on set device.
        locale (DeviceInfoAttribute):
        location (DeviceInfoAttribute): Location/IP of device on LAN.
        model_name (DeviceInfoAttribute): Device model name.
        model_number (DeviceInfoAttribute): Device model number.
        model_region (DeviceInfoAttribute):
        notifications_enabled (DeviceInfoAttribute):
        notifications_first_use (DeviceInfoAttribute):
        panel_id (DeviceInfoAttribute):
        player (DeviceInfoAttribute): Media player data, state, format.
        power_mode (DeviceInfoAttribute): Device current state on/off.
        screen_size (DeviceInfoAttribute): Screen size of tv.
        search_channels_enabled (DeviceInfoAttribute):
        search_enabled (DeviceInfoAttribute):
        secure_device (DeviceInfoAttribute):
        serial_number (DeviceInfoAttribute): Device's serial number
        software_build (DeviceInfoAttribute): Device's software build
        software_version (DeviceInfoAttribute): Device's software version
        supports_audio_guide (DeviceInfoAttribute):
        supports_ethernet (DeviceInfoAttribute):
        supports_find_remote (DeviceInfoAttribute):
        supports_private_listening (DeviceInfoAttribute):
        supports_private_listening_dtv (DeviceInfoAttribute):
        supports_rva (DeviceInfoAttribute):
        supports_wake_on_wlan (DeviceInfoAttribute): Device supports wake on LAN
        supports_warm_standby (DeviceInfoAttribute):
        supports_suspend (DeviceInfoAttribute):
        support_url (DeviceInfoAttribute):
        time_zone (DeviceInfoAttribute): Device's timezone
        time_zone_auto (DeviceInfoAttribute):
        time_zone_name (DeviceInfoAttribute):
        time_zone_offset (DeviceInfoAttribute):
        time_zone_tz (DeviceInfoAttribute):
        trc_channel_version (DeviceInfoAttribute):
        trc_version (DeviceInfoAttribute):
        tuner_type (DeviceInfoAttribute):
        udn (DeviceInfoAttribute): UUID for device
        uptime (DeviceInfoAttribute): How long the device ahas been on.
        user_device_name (DeviceInfoAttribute):
        user_device_location (DeviceInfoAttribute):
        vendor_name (DeviceInfoAttribute):
        voice_search_enabled (DeviceInfoAttribute):
        wifi_driver (DeviceInfoAttribute): Wifi driver used.
        wifi_mac (DeviceInfoAttribute): Mac address.

    *methods
        fetch_data()

        as_json(exclude: List[str]) -> str

        as_xml(exclude: List[str]) -> str
    """
    def __init__(self, location: str, discovery_data: DiscoveryData):
        self.advertising_id: DeviceInfoAttribute = None
        self.apps: Union[List[RokuApp], None] = None
        self.build_number: DeviceInfoAttribute = None
        self.can_use_wifi_extender: DeviceInfoAttribute = None
        self.clock_format: DeviceInfoAttribute = None
        self.country: DeviceInfoAttribute = None
        self.data: dict = {}
        self.davinci_version: DeviceInfoAttribute = None
        self.default_device_name: DeviceInfoAttribute = None
        self.developer_enabled: DeviceInfoAttribute = None
        self.device_id: DeviceInfoAttribute = None
        self.discovery_data: DiscoveryData = discovery_data
        self.expert_pq_enabled: DeviceInfoAttribute = None
        self.find_remote_is_possible: DeviceInfoAttribute = None
        self.friendly_device_name: DeviceInfoAttribute = None
        self.friendly_model_name: DeviceInfoAttribute = None
        self.grandcentral_version: DeviceInfoAttribute = None
        self.has_mobile_screensaver: DeviceInfoAttribute = None
        self.has_play_on_roku: DeviceInfoAttribute = None
        self.has_wifi_extender: DeviceInfoAttribute = None
        self.has_wifi_5G_support: DeviceInfoAttribute = None
        self.headphones_connected: DeviceInfoAttribute = None
        self.is_stick: DeviceInfoAttribute = None
        self.is_tv: DeviceInfoAttribute = None
        self.keyed_developer_id: DeviceInfoAttribute = None
        self.language: DeviceInfoAttribute = None
        self.locale: DeviceInfoAttribute = None
        self.location: str = location
        self.model_name: DeviceInfoAttribute = None
        self.model_number: DeviceInfoAttribute = None
        self.model_region: DeviceInfoAttribute = None
        self.notifications_enabled: DeviceInfoAttribute = None
        self.notifications_first_use: DeviceInfoAttribute = None
        self.panel_id: DeviceInfoAttribute = None
        self.player: Union[Player, None] = None
        self.power_mode: DeviceInfoAttribute = None
        self.screen_size: DeviceInfoAttribute = None
        self.search_channels_enabled: DeviceInfoAttribute = None
        self.search_enabled: DeviceInfoAttribute = None
        self.secure_device: DeviceInfoAttribute = None
        self.serial_number: DeviceInfoAttribute = None
        self.software_build: DeviceInfoAttribute = None
        self.software_version: DeviceInfoAttribute = None
        self.supports_audio_guide: DeviceInfoAttribute = None
        self.supports_ethernet: DeviceInfoAttribute = None
        self.supports_find_remote: DeviceInfoAttribute = None
        self.supports_private_listening: DeviceInfoAttribute = None
        self.supports_private_listening_dtv: DeviceInfoAttribute = None
        self.supports_rva: DeviceInfoAttribute = None
        self.supports_wake_on_wlan: DeviceInfoAttribute = None
        self.supports_warm_standby: DeviceInfoAttribute = None
        self.supports_suspend: DeviceInfoAttribute = None
        self.support_url: DeviceInfoAttribute = None
        self.time_zone: DeviceInfoAttribute = None
        self.time_zone_auto: DeviceInfoAttribute = None
        self.time_zone_name: DeviceInfoAttribute = None
        self.time_zone_offset: DeviceInfoAttribute = None
        self.time_zone_tz: DeviceInfoAttribute = None
        self.trc_channel_version: DeviceInfoAttribute = None
        self.trc_version: DeviceInfoAttribute = None
        self.tuner_type: DeviceInfoAttribute = None
        self.udn: DeviceInfoAttribute = None
        self.uptime: DeviceInfoAttribute = None
        self.user_device_name: DeviceInfoAttribute = None
        self.user_device_location: DeviceInfoAttribute = None
        self.vendor_name: DeviceInfoAttribute = None
        self.voice_search_enabled: DeviceInfoAttribute = None
        self.wifi_driver: DeviceInfoAttribute = None
        self.wifi_mac: DeviceInfoAttribute = None

    def fetch_data(self) -> None:
        """
        Intermediary function to request further device data from fetch_all_data()
        """
        self.data = asyncio.run(fetch_all_data(self.location))
        device_info: dict = self.data.get('device_info', None)
        apps: dict = self.data.get('apps', None)
        active_app: Union[None, OrderedDict] = self.data.get('active_app', None)
        media_player: Union[dict, OrderedDict] = self.data.get('media_player', None)

        if device_info is not None and isinstance(device_info['data'], OrderedDict):
            self.__set_device_info_attributes(device_info['data']['device-info'])

        if apps is not None and isinstance(apps['data'], OrderedDict):
            if active_app is not None and isinstance(active_app['data'], OrderedDict):
                active_app = active_app['data']['active-app']['app']

            self.__set_apps(apps['data']['apps']['app'], active_app)

        if media_player is not None and isinstance(media_player['data'], OrderedDict):
            self.__set_player_data(media_player['data']['player'])

    def __set_device_info_attributes(self, device_info: OrderedDict) -> None:
        """
        Sets all device info attributes with corresponding ECP device info data

        *Args:
            device_info (OrderedDict): Roku ECP device info parsed into a dict by xmlToDict
        """
        for key in device_info.keys():
            obj_key = key.replace('-', '_')
            if hasattr(self, obj_key):
                val: Union[None, str] = device_info.get(key, None)
                if isinstance(val, str):
                    if val.lower() == 'true' or val.lower() == 'false':
                        bool_val: bool = True if val.lower() == 'true' else False
                        setattr(self, obj_key, bool_val)
                    else:
                        setattr(self, obj_key, val)

    def __set_apps(self, apps: list, active_app: Union[OrderedDict, None]) -> None:
        """
        Sets apps attributes with corresponding ECP apps data

        *Args:
            apps (list): List of Roku ECP apps parsed into a dict by xmlToDict
            active_app (OrderedDict): Roku ECP active app parsed into a dict by xmlToDict
        """
        for app_data in apps:
            app: RokuApp = {
                'id': app_data.get('@id', None),
                'type': app_data.get('@type', None),
                'subtype': app_data.get('@subtype', None),
                'version': app_data.get('@version', None),
                'name': app_data.get('#text', None),
                'active': False
            }

            if isinstance(active_app, OrderedDict):
                active_app_id: str = active_app.get('@id', '')
                if active_app_id == app['id']:
                    app['active'] = True

            if self.apps is None:
                self.apps = []

            self.apps.append(app)

    def __set_player_data(self, player_data: OrderedDict) -> None:
        """
        Sets player data with corresponding ECP media player data

        *Args:
            player_data (OrderedDict): Roku ECP player data parsed into a dict by xmlToDict
        """
        self.player = {
            'error': player_data.get('@error', ''),
            'state': player_data.get('@state', ''),
            'is_live': player_data.get('is_live', False),
            'format': {}
        }
        if isinstance(player_data.get('format', None), OrderedDict):
            self.player['format'].update({
                'audio': player_data['format'].get('@audio', None),
                'captions': player_data['format'].get('@captions', None),
                'drm': player_data['format'].get('@drm', None),
                'video': player_data['format'].get('@video', None),
            })

    def as_json(self, exclude: Union[list, None] = None, pretty_format: bool = False) -> str:
        """
        Formats device data into JSON.
        """
        device_name: str = 'unknown-device'
        try:
            device_name = self.data["device_info"]["data"]["device-info"]["default-device-name"].replace(' ', '')
        except KeyError:
            pass

        temp: dict = {}

        for data_set in self.data.items():
            data: Union[dict, None] = None
            if exclude is not None:
                if data_set[0] not in exclude:
                    data = data_set[1].get('data', None)
            else:
                data = data_set[1].get('data', None)

            if data is not None:
                temp.update(data_set[1]['data'])

        if pretty_format:
            return json.dumps({device_name: temp}, indent=4, sort_keys=True)

        return json.dumps({device_name: temp})

    def as_xml(self, exclude: Union[list, None] = None) -> str:
        """
        Formats device data into XML.
        """
        device_name: str = 'unknown-device'
        try:
            device_name = self.data["device_info"]["data"]["device-info"]["default-device-name"]
        except KeyError:
            pass

        temp: str = f'<{device_name}>\n'

        for data_set in self.data.items():
            xml: Union[dict, None] = None
            if exclude is not None:
                if data_set[0] not in exclude:
                    xml = data_set[1].get('xml', None)
            else:
                xml = data_set[1].get('xml', None)

            if xml is not None:
                temp += data_set[1]['xml'].replace('<?xml version="1.0" encoding="UTF-8" ?>', '')

        temp += f'</{device_name}>\n'

        return temp


async def fetch_all_data(roku_location: str) -> dict:
    """
    Create async tasks for requesting more data from device.

    *Args:
        roku_location (str): IP address to device.

    *Returns (dict): {
        'device_info': data from {roku_location}:8060/query/device-info
        'apps': data from {roku_location}:8060/query/apps,
        'active_app': data from {roku_location}:8060/query/active-app,
        'media_player': data from {roku_location}:8060/query/media-player
    }

    *Note:
        Roku ECP
        https://developer.roku.com/docs/developer-program/debugging/external-control-api.md
    """
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


async def fetch_device_info(roku_location: str) -> Union[EcpData, Dict[str, str]]:
    """
    Makes GET request for device info following Roku ECP.

    *Args:
        roku_location (str): IP address to device.

    *Returns
        (EcpData): device data in dict form and the raw xml returned or error.
    """
    resp: Response = requests.get(f'{roku_location}query/device-info', headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        device_data_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': device_data_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}


async def fetch_apps(roku_location: str) -> Union[EcpData, Dict[str, str]]:
    """
    Makes GET request for apps following Roku ECP.

    *Args:
        roku_location (str): IP address to device.

    *Returns
        (EcpData): app data in dict form and the raw xml returned or error.
    """
    resp: Response = requests.get(f'{roku_location}query/apps', headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        apps_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': apps_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}


async def fetch_active_app(roku_location: str) -> Union[EcpData, Dict[str, str]]:
    """
    Makes GET request for active-app following Roku ECP.

    *Args:
        roku_location (str): IP address to device.

    *Returns
        (EcpData): active-app data in dict form and the raw xml returned or error.
    """
    resp: Response = requests.get(f'{roku_location}query/active-app', headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        active_app_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': active_app_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}


async def fetch_media_player(roku_location: str) -> Union[EcpData, Dict[str, str]]:
    """
    Makes GET request for media player following Roku ECP.

    *Args:
        roku_location (str): IP address to device.

    *Returns
        (EcpData): media player data in dict form and the raw xml returned or error.
    """
    resp: Response = requests.get(f'{roku_location}query/media-player', headers={'Content-Type': 'application/xml'})

    if resp.status_code == requests.codes.ok:
        xml_str: str = resp.text
        media_player_dict: dict = xmltodict.parse(xml_str)

        return {
            'data': media_player_dict,
            'xml': xml_str
        }
    else:
        return {'Error': f'Unable to reach device at {roku_location}'}
