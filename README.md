# pysmartthings
[![Build Status](https://travis-ci.org/andrewsayre/pysmartthings.svg?branch=master)](https://travis-ci.org/andrewsayre/pysmartthings)

A python library for interacting with the SmartThings cloud API.  This is an early (beta / incomplete) version of the package.
## Usage
Create an instance of the SmartThings class and pass in your personal access token.  This will make an initial service call to populate the `devices` array.
```
>>> import pysmartthings
>>> st = pysmartthings.SmartThings("PERSONAL_ACCESS_TOKEN")
>>> len(st.devices)
19
```
Each array element is an instance of `Device` which encapsulates information about the device in SmartThings.
```
>>> device = st.devices[0]
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
The current status of the device is populated when `Device.update()` or `SmartThings.update()` is called.  The later will retreive the current status for all devices in parallel.  The status dictionary represents the current values of select capabilities.
```
>>> st.update()
True
>> device.status
{'light': 'off', 'switchLevel': 100, 'switch': 'off'}
```