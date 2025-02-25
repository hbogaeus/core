"""Common fixtures for the ista EcoTrend tests."""

from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from homeassistant.components.ista_ecotrend.const import DOMAIN
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

from tests.common import MockConfigEntry


@pytest.fixture(name="ista_config_entry")
def mock_ista_config_entry() -> MockConfigEntry:
    """Mock ista EcoTrend configuration entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_EMAIL: "test@example.com",
            CONF_PASSWORD: "test-password",
        },
        unique_id="26e93f1a-c828-11ea-87d0-0242ac130003",
    )


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock, None, None]:
    """Override async_setup_entry."""
    with patch(
        "homeassistant.components.ista_ecotrend.async_setup_entry", return_value=True
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
def mock_ista() -> Generator[MagicMock, None, None]:
    """Mock Pyecotrend_ista client."""

    with (
        patch(
            "homeassistant.components.ista_ecotrend.PyEcotrendIsta",
            autospec=True,
        ) as mock_client,
        patch(
            "homeassistant.components.ista_ecotrend.config_flow.PyEcotrendIsta",
            new=mock_client,
        ),
        patch(
            "homeassistant.components.ista_ecotrend.coordinator.PyEcotrendIsta",
            new=mock_client,
        ),
    ):
        client = mock_client.return_value
        client._uuid = "26e93f1a-c828-11ea-87d0-0242ac130003"
        client._a_firstName = "Max"
        client._a_lastName = "Istamann"
        client.get_consumption_unit_details.return_value = {
            "consumptionUnits": [
                {
                    "id": "26e93f1a-c828-11ea-87d0-0242ac130003",
                    "address": {
                        "street": "Luxemburger Str.",
                        "houseNumber": "1",
                    },
                },
                {
                    "id": "eaf5c5c8-889f-4a3c-b68c-e9a676505762",
                    "address": {
                        "street": "Bahnhofsstr.",
                        "houseNumber": "1A",
                    },
                },
            ]
        }
        client.getUUIDs.return_value = [
            "26e93f1a-c828-11ea-87d0-0242ac130003",
            "eaf5c5c8-889f-4a3c-b68c-e9a676505762",
        ]
        client.get_raw = get_raw

        yield client


def get_raw(obj_uuid: str | None = None) -> dict[str, Any]:
    """Mock function get_raw."""
    return {
        "consumptionUnitId": obj_uuid,
        "consumptions": [
            {
                "date": {"month": 5, "year": 2024},
                "readings": [
                    {
                        "type": "heating",
                        "value": "35",
                        "additionalValue": "38,0",
                    },
                    {
                        "type": "warmwater",
                        "value": "1,0",
                        "additionalValue": "57,0",
                    },
                    {
                        "type": "water",
                        "value": "5,0",
                    },
                ],
            },
            {
                "date": {"month": 4, "year": 2024},
                "readings": [
                    {
                        "type": "heating",
                        "value": "104",
                        "additionalValue": "113,0",
                    },
                    {
                        "type": "warmwater",
                        "value": "1,1",
                        "additionalValue": "61,1",
                    },
                    {
                        "type": "water",
                        "value": "6,8",
                    },
                ],
            },
        ],
        "costs": [
            {
                "date": {"month": 5, "year": 2024},
                "costsByEnergyType": [
                    {
                        "type": "heating",
                        "value": 21,
                    },
                    {
                        "type": "warmwater",
                        "value": 7,
                    },
                    {
                        "type": "water",
                        "value": 3,
                    },
                ],
            },
            {
                "date": {"month": 4, "year": 2024},
                "costsByEnergyType": [
                    {
                        "type": "heating",
                        "value": 62,
                    },
                    {
                        "type": "warmwater",
                        "value": 7,
                    },
                    {
                        "type": "water",
                        "value": 2,
                    },
                ],
            },
        ],
    }
