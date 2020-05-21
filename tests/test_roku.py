from pathlib import Path
from typing import Dict

import pytest
import xmltodict  # type: ignore

from roku_scanner.custom_types import PathType
from roku_scanner.roku import Roku

MOCK_DATA = Path(__file__).parent / 'mock_data'


@pytest.fixture
def discovery_data() -> bytes:
    discovery_data_file: PathType = MOCK_DATA / 'discovery_data.txt'
    with discovery_data_file.open('rb') as f:
        mock_device_data = f.read()

    return mock_device_data


@pytest.fixture
def mock_device_data():
    mock_active_app: PathType = MOCK_DATA / 'active-app.xml'
    mock_apps: PathType = MOCK_DATA / 'apps.xml'
    mock_device_info: PathType = MOCK_DATA / 'device-info.xml'
    mock_media_player: PathType = MOCK_DATA / 'media-player.xml'
    mock_file_paths: Dict[str, PathType] = {
        'device_info': mock_device_info,
        'apps': mock_apps,
        'active_app': mock_active_app,
        'media_player': mock_media_player
    }
    mock_data: dict = {}

    for mock_path in mock_file_paths:
        with mock_file_paths[mock_path].open('r') as mock_file:
            lines: list = mock_file.readlines()
            mock_xml: str = ''.join(lines)
            data: dict = xmltodict.parse(mock_xml)
            mock_data[mock_path] = {
                'data': data,
                'xml': mock_xml
            }

    return mock_data


def test_roku_as_json(mock_device_data):
    roku: Roku = Roku(location='http://127.0.0.1:8060/', discovery_data=discovery_data)
    roku.data = mock_device_data
    formatted = roku.as_json()
    assert isinstance(formatted, str)
    assert len(formatted) != 0


def test_roku_as_xml(mock_device_data, discovery_data):
    roku: Roku = Roku(location='http://127.0.0.1:8060/', discovery_data=discovery_data)
    roku.data = mock_device_data
    formatted = roku.as_xml()
    assert isinstance(formatted, str)
    assert len(formatted) != 0


def test_roku_as_xml_with_exclusions(mock_device_data, discovery_data):
    roku: Roku = Roku(location='http://127.0.0.1:8060/', discovery_data=discovery_data)
    roku.data = mock_device_data
    formatted = roku.as_xml(exclude=['device_info'])
    assert isinstance(formatted, str)
    assert len(formatted) != 0


def test_roku_as_json_with_exclusions(mock_device_data):
    roku: Roku = Roku(location='http://127.0.0.1:8060/', discovery_data=discovery_data)
    roku.data = mock_device_data
    formatted = roku.as_json(exclude=['device_info'])
    assert isinstance(formatted, str)
    assert len(formatted) != 0
