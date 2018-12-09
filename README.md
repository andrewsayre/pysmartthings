# pysmartthings
[![Build Status](https://travis-ci.org/andrewsayre/pysmartthings.svg?branch=master)](https://travis-ci.org/andrewsayre/pysmartthings)
[![Coverage Status](https://coveralls.io/repos/github/andrewsayre/pysmartthings/badge.svg?branch=master)](https://coveralls.io/github/andrewsayre/pysmartthings?branch=master)
[![image](https://img.shields.io/pypi/v/pysmartthings.svg)](https://pypi.org/project/pysmartthings/)
[![image](https://img.shields.io/pypi/pyversions/pysmartthings.svg)](https://pypi.org/project/pysmartthings/)
[![image](https://img.shields.io/pypi/l/pysmartthings.svg)](https://pypi.org/project/pysmartthings/)
[![image](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)](https://houndci.com)

A python library for interacting with the SmartThings cloud API.  This is an early (beta / incomplete) version of the package.
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
Call the create function and pass in your [personal access token](https://account.smartthings.com/tokens).  This will initially populate `locations` and `devices`.
```
>>> import pysmartthings
>>> st = pysmartthings.create("PERSONAL_ACCESS_TOKEN")
```
### Locations
A list of locations in SmartThings can be retrieved by invoking `SmartThings.locations()`.
```
>>> locations = st.locations()
>>> len(locations)
2
>>> location = locations[0]
>>> location.name
'Test Home'
>>> location.location_id
'5c03e518-118a-44cb-85ad-7877d0b302e4' 
```
### Devices
A list of devices across all locations in SmartThings can be retrieved by invoking `SmartThings.devices()`.
```
>>> devices = st.devices()
>>> len(devices)
19
>>> device = devices[0]
>>> device.device_id
'0d38d5ca-705f-44f7-89bd-36a8cf73678d'
>>> device.name
'GE In-Wall Smart Dimmer'
>>> device.label
'Back Patio Light'
>>> device.capabilities
['switch', 'switchLevel', 'refresh', 'indicator', 'button', 'sensor', 'actuator', 'healthCheck', 'light']
```
For Device Type Handlers (DTH) additional information is available about the handler:
```
>>> device.type
'DTH'
>>> device.device_type_name
'GE Dimmer Switch 14294'
>>> device.device_type_network
'ZWAVE'
>>> device.device_type_id
'23a143cf-bad9-4dc1-a56b-fd93ff01e9f9'
```
The current status of the device is populated when `Device.update()` is called.  The status dictionary represents the current values of select capabilities.
```
>>> device.update()
True
>> device.status
{'light': 'off', 'switchLevel': 100, 'switch': 'off'}
```
#### Device Commands
You can execute a command on a device by calling the `Device.command(capability, command, args=None)` function.  The `capability` parameter corresponds to one of the capabilities detected and `command` is one of the define commands. `args` is an array of parameters to pass to the command (optional).  See the [SmartThings Capability Reference](https://smartthings.developer.samsung.com/develop/api-ref/capabilities.html) for more information.
```
>>> device.command("switch", "on")
True
>>> device.command("switchLevel", "setLevel", [75, 2])
True
```
Devices with the `switch` capability have the following functions:
```
>>> device.switch_on()
True
>>> device.switch_off()
True
```
Devices with the `switchLevel` capability have the following function that sets the target brightness level and transitions using a specific duration (seconds).
```
>>> device.set_level(75, 2)
True
```