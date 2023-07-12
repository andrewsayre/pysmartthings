# pysmartthings

[![CI Status](https://github.com/andrewsayre/pysmartthings/workflows/CI/badge.svg)](https://github.com/andrewsayre/pysmartthings/actions)
[![codecov](https://codecov.io/gh/andrewsayre/pysmartthings/branch/dev/graph/badge.svg?token=Q13LDPU5MF)](https://codecov.io/gh/andrewsayre/pysmartthings)
[![image](https://img.shields.io/pypi/v/pysmartthings.svg)](https://pypi.org/project/pysmartthings/)
[![image](https://img.shields.io/pypi/pyversions/pysmartthings.svg)](https://pypi.org/project/pysmartthings/)
[![image](https://img.shields.io/pypi/l/pysmartthings.svg)](https://pypi.org/project/pysmartthings/)

A python library for interacting with the SmartThings cloud API build with [asyncio](https://docs.python.org/3/library/asyncio.html) and [aiohttp](https://aiohttp.readthedocs.io/en/stable/).

## Features

The package is still in beta, but the following features are available:

1. Locations: List, Get
1. Rooms: List, Get, Create, Update, Deletegit
1. Devices: List, Get, Command, Status
1. Apps: List, Get, Create, Update, Delete, Settings Get & Update, OAuth: Get, Update, & Generate
1. InstalledApps: List, Get, Delete
1. Subscriptions: List, Get, Create, Delete, Delete All
1. Scenes: List, Execute
1. OAuth: Generate refresh/access token pair

## Installation

```commandline
pip install pysmartthings
```

or

```commandline
pip install --use-wheel pysmartthings
```

## Usage

### Initialization

The SmartThings class encapsulates the API operations and the constructor accepts the aiohttp `WebSession` and your [personal access token](https://account.smartthings.com/tokens).

```pythonstub
import aiohttp
import pysmartthings

token = 'PERSONAL_ACCESS_TOKEN'

async with aiohttp.ClientSession() as session:
    api = pysmartthings.SmartThings(session, token)
    # ...
```

### Locations

A list of locations in SmartThings can be retrieved by invoking the coroutine `locations()`.

```pythonstub
    locations = await api.locations()
    print(len(locations))

    location = locations[0]
    print(location.name)
    print(location.location_id)
```

Outputs:

```pythonstub
2
'Test Home'
'5c03e518-118a-44cb-85ad-7877d0b302e4'
```

### Devices

A list of devices can be retrieved by invoking the coroutine `devices(location_ids=None, capabilities=None, device_ids=None)`. The optional parameters allow filtering the returned list.

```pythonstub
    devices = await api.devices()
    print(len(devices))

    device = devices[0]
    print(device.device_id)
    print(device.name)
    print(device.label)
    print(device.capabilities)
```

Outputs:

```pythonstub
19
'0d38d5ca-705f-44f7-89bd-36a8cf73678d'
'GE In-Wall Smart Dimmer'
'Back Patio Light'
['switch', 'switchLevel', 'refresh', 'indicator', 'button', 'sensor', 'actuator', 'healthCheck', 'light']
```

The current status of the device is populated when the coroutine `status.refresh()` is called. The DeviceStatus class represents the current values of the capabilities and provides several normalized property accessors.

```pythonstub
    await device.status.refresh()
    print(device.status.values)
    print(device.status.switch)
    print(device.status.level)
```

Outputs:

```pythonstub
{'button': 'pressed', 'numberOfButtons': None, 'supportedButtonValues': None, 'indicatorStatus': 'when off', 'switch': 'on', 'checkInterval': 1920, 'healthStatus': None, 'DeviceWatch-DeviceStatus': None, 'level': 100}
True
100
```

#### Device Commands

You can execute a command on a device by calling the coroutine `command(component_id, capability, command, args=None)` function. The `component_id` parameter is the identifier of the component within the device (`main` is the device itself); `capability` is the name of the capability implemented by the device; and `command` is one of the defined operations within the capability. `args` is an array of parameters to pass to the command when it accepts parameters (optional). See the [SmartThings Capability Reference](https://smartthings.developer.samsung.com/develop/api-ref/capabilities.html) for more information.

```pythonstub
    result = await device.command("main", "switch", "on")
    assert result == True

    result = await device.command("main", "switchLevel", "setLevel", [75, 2])
    assert result == True
```

Devices with the `switch` capability have the following coroutines:

```pythonstub
    result = await device.switch_on()
    assert result == True

    result = await device.switch_off()
    assert result == True
```

Devices with the `switchLevel` capability have the following function that sets the target brightness level and transitions using a specific duration (seconds).

```pythonstub
    result = await device.set_level(75, 2)
    assert result == True
```

Devices with the `windowShadeLevel` capability have the following function that sets the target shade level.

```pythonstub
    result = await device.set_window_shade_level(50)
    assert result == True
```
