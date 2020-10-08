"""
Defines SmartThings capabilities and attributes.

https://smartthings.developer.samsung.com/docs/api-ref/capabilities.html
"""

CAPABILITIES_TO_ATTRIBUTES = {
    "accelerationSensor": ["acceleration"],
    "activityLightingMode": ["lightingMode"],
    "airConditionerFanMode": ["fanMode", "supportedAcFanModes"],
    "airConditionerMode": ["airConditionerMode", "supportedAcModes"],
    "airFlowDirection": ["airFlowDirection"],
    "airQualitySensor": ["airQuality"],
    "alarm": ["alarm"],
    "audioMute": ["mute"],
    "audioVolume": ["volume"],
    "battery": ["battery"],
    "bodyMassIndexMeasurement": ["bmiMeasurement"],
    "bodyWeightMeasurement": ["bodyWeightMeasurement"],
    "button": ["button", "numberOfButtons", "supportedButtonValues"],
    "carbonDioxideMeasurement": ["carbonDioxide"],
    "carbonMonoxideDetector": ["carbonMonoxide"],
    "carbonMonoxideMeasurement": ["carbonMonoxideLevel"],
    "colorControl": ["color", "hue", "saturation"],
    "colorTemperature": ["colorTemperature"],
    "contactSensor": ["contact"],
    "demandResponseLoadControl": ["drlcStatus"],
    "dishwasherMode": ["dishwasherMode"],
    "dishwasherOperatingState": [
        "machineState",
        "supportedMachineStates",
        "dishwasherJobState",
        "completionTime",
    ],
    "doorControl": ["door"],
    "dryerMode": ["dryerMode"],
    "dryerOperatingState": [
        "machineState",
        "supportedMachineStates",
        "dryerJobState",
        "completionTime",
    ],
    "dustSensor": ["fineDustLevel", "dustLevel"],
    "energyMeter": ["energy"],
    "equivalentCarbonDioxideMeasurement": ["equivalentCarbonDioxideMeasurement"],
    "execute": ["data"],
    "fanSpeed": ["fanSpeed"],
    "filterStatus": ["filterStatus"],
    "formaldehydeMeasurement": ["formaldehydeLevel"],
    "garageDoorControl": ["door"],
    "gasMeter": [
        "gasMeter",
        "gasMeterCalorific",
        "gasMeterConversion",
        "gasMeterPrecision",
        "gasMeterTime",
        "gasMeterVolume",
    ],
    "illuminanceMeasurement": ["illuminance"],
    "infraredLevel": ["infraredLevel"],
    "lock": ["lock"],
    "mediaInputSource": ["inputSource", "supportedInputSources"],
    "mediaPlaybackRepeat": ["playbackRepeatMode"],
    "mediaPlaybackShuffle": ["playbackShuffle"],
    "mediaPlayback": ["playbackStatus", "supportedPlaybackCommands"],
    "motionSensor": ["motion"],
    "ocf": [
        "st",
        "mnfv",
        "mndt",
        "mnhw",
        "di",
        "mnsl",
        "dmv",
        "n",
        "vid",
        "mnmo",
        "mnmn",
        "mnml",
        "mnpv",
        "mnos",
        "pi",
        "icv",
    ],
    "odorSensor": ["odorLevel"],
    "ovenMode": ["ovenMode"],
    "ovenOperatingState": [
        "machineState",
        "supportedMachineStates",
        "ovenJobState",
        "completionTime",
        "operationTime",
        "progress",
    ],
    "ovenSetpoint": ["ovenSetpoint"],
    "powerConsumptionReport": ["powerConsumption"],
    "powerMeter": ["power"],
    "powerSource": ["powerSource"],
    "presenceSensor": ["presence"],
    "rapidCooling": ["rapidCooling"],
    "refrigerationSetpoint": ["refrigerationSetpoint"],
    "relativeHumidityMeasurement": ["humidity"],
    "robotCleanerCleaningMode": ["robotCleanerCleaningMode"],
    "robotCleanerMovement": ["robotCleanerMovement"],
    "robotCleanerTurboMode": ["robotCleanerTurboMode"],
    "signalStrength": ["lqi", "rssi"],
    "smokeDetector": ["smoke"],
    "soundSensor": ["sound"],
    "switchLevel": ["level"],
    "switch": ["switch"],
    "tamperAlert": ["tamper"],
    "temperatureMeasurement": ["temperature"],
    "thermostat": [
        "coolingSetpoint",
        "coolingSetpointRange",
        "heatingSetpoint",
        "heatingSetpointRange",
        "schedule",
        "temperature",
        "thermostatFanMode",
        "supportedThermostatFanModes",
        "thermostatMode",
        "supportedThermostatModes",
        "thermostatOperatingState",
        "thermostatSetpoint",
        "thermostatSetpointRange",
    ],
    "thermostatCoolingSetpoint": ["coolingSetpoint"],
    "thermostatFanMode": ["thermostatFanMode", "supportedThermostatFanModes"],
    "thermostatHeatingSetpoint": ["heatingSetpoint"],
    "thermostatMode": ["thermostatMode", "supportedThermostatModes"],
    "thermostatOperatingState": ["thermostatOperatingState"],
    "thermostatSetpoint": ["thermostatSetpoint"],
    "threeAxis": ["threeAxis"],
    "tvChannel": ["tvChannel", "tvChannelName"],
    "tvocMeasurement": ["tvocLevel"],
    "ultravioletIndex": ["ultravioletIndex"],
    "valve": ["valve"],
    "voltageMeasurement": ["voltage"],
    "washerMode": ["washerMode"],
    "washerOperatingState": [
        "machineState",
        "supportedMachineStates",
        "washerJobState",
        "completionTime",
    ],
    "waterSensor": ["water"],
    "windowShade": ["windowShade"],
}
CAPABILITIES = list(CAPABILITIES_TO_ATTRIBUTES)
ATTRIBUTES = {
    attrib
    for attributes in CAPABILITIES_TO_ATTRIBUTES.values()
    for attrib in attributes
}


class Capability:
    """Define common capabilities."""

    acceleration_sensor = "accelerationSensor"
    activity_lighting_mode = "activityLightingMode"
    air_conditioner_fan_mode = "airConditionerFanMode"
    air_conditioner_mode = "airConditionerMode"
    air_flow_direction = "airFlowDirection"
    air_quality_sensor = "airQualitySensor"
    alarm = "alarm"
    audio_mute = "audioMute"
    audio_volume = "audioVolume"
    battery = "battery"
    body_mass_index_measurement = "bodyMassIndexMeasurement"
    body_weight_measurement = "bodyWeightMeasurement"
    button = "button"
    carbon_dioxide_measurement = "carbonDioxideMeasurement"
    carbon_monoxide_detector = "carbonMonoxideDetector"
    carbon_monoxide_measurement = "carbonMonoxideMeasurement"
    color_control = "colorControl"
    color_temperature = "colorTemperature"
    contact_sensor = "contactSensor"
    demand_response_load_control = "demandResponseLoadControl"
    dishwasher_mode = "dishwasherMode"
    dishwasher_operating_state = "dishwasherOperatingState"
    door_control = "doorControl"
    dryer_mode = "dryerMode"
    dryer_operating_state = "dryerOperatingState"
    dust_sensor = "dustSensor"
    energy_meter = "energyMeter"
    equivalent_carbon_dioxide_measurement = "equivalentCarbonDioxideMeasurement"
    execute = "execute"
    fan_speed = "fanSpeed"
    filter_status = "filterStatus"
    formaldehyde_measurement = "formaldehydeMeasurement"
    garage_door_control = "garageDoorControl"
    gas_meter = "gasMeter"
    illuminance_measurement = "illuminanceMeasurement"
    infrared_level = "infraredLevel"
    lock = "lock"
    media_input_source = "mediaInputSource"
    media_playback = "mediaPlayback"
    media_playback_repeat = "mediaPlaybackRepeat"
    media_playback_shuffle = "mediaPlaybackShuffle"
    motion_sensor = "motionSensor"
    ocf = "ocf"
    odor_sensor = "odorSensor"
    oven_mode = "ovenMode"
    oven_operating_state = "ovenOperatingState"
    oven_setpoint = "ovenSetpoint"
    power_consumption_report = "powerConsumptionReport"
    power_meter = "powerMeter"
    power_source = "powerSource"
    presence_sensor = "presenceSensor"
    rapid_cooling = "rapidCooling"
    refrigeration_setpoint = "refrigerationSetpoint"
    relative_humidity_measurement = "relativeHumidityMeasurement"
    robot_cleaner_cleaning_mode = "robotCleanerCleaningMode"
    robot_cleaner_movement = "robotCleanerMovement"
    robot_cleaner_turbo_mode = "robotCleanerTurboMode"
    signal_strength = "signalStrength"
    smoke_detector = "smokeDetector"
    sound_sensor = "soundSensor"
    switch = "switch"
    switch_level = "switchLevel"
    tamper_alert = "tamperAlert"
    temperature_measurement = "temperatureMeasurement"
    thermostat = "thermostat"
    thermostat_cooling_setpoint = "thermostatCoolingSetpoint"
    thermostat_fan_mode = "thermostatFanMode"
    thermostat_heating_setpoint = "thermostatHeatingSetpoint"
    thermostat_mode = "thermostatMode"
    thermostat_operating_state = "thermostatOperatingState"
    thermostat_setpoint = "thermostatSetpoint"
    three_axis = "threeAxis"
    tv_channel = "tvChannel"
    tvoc_measurement = "tvocMeasurement"
    ultraviolet_index = "ultravioletIndex"
    valve = "valve"
    voltage_measurement = "voltageMeasurement"
    washer_mode = "washerMode"
    washer_operating_state = "washerOperatingState"
    water_sensor = "waterSensor"
    window_shade = "windowShade"


class Attribute:
    """Define common attributes."""

    acceleration = "acceleration"
    air_conditioner_mode = "airConditionerMode"
    air_flow_direction = "airFlowDirection"
    air_quality = "airQuality"
    alarm = "alarm"
    battery = "battery"
    bmi_measurement = "bmiMeasurement"
    body_weight_measurement = "bodyWeightMeasurement"
    button = "button"
    carbon_dioxide = "carbonDioxide"
    carbon_monoxide = "carbonMonoxide"
    carbon_monoxide_level = "carbonMonoxideLevel"
    color = "color"
    color_temperature = "colorTemperature"
    completion_time = "completionTime"
    contact = "contact"
    cooling_setpoint = "coolingSetpoint"
    cooling_setpoint_range = "coolingSetpointRange"
    data = "data"
    di = "di"
    dishwasher_job_state = "dishwasherJobState"
    dishwasher_mode = "dishwasherMode"
    dmv = "dmv"
    door = "door"
    drlc_status = "drlcStatus"
    dryer_job_state = "dryerJobState"
    dryer_mode = "dryerMode"
    dust_level = "dustLevel"
    energy = "energy"
    equivalent_carbon_dioxide_measurement = "equivalentCarbonDioxideMeasurement"
    fan_mode = "fanMode"
    fan_speed = "fanSpeed"
    filter_status = "filterStatus"
    fine_dust_level = "fineDustLevel"
    formaldehyde_level = "formaldehydeLevel"
    gas_meter = "gasMeter"
    gas_meter_calorific = "gasMeterCalorific"
    gas_meter_conversion = "gasMeterConversion"
    gas_meter_precision = "gasMeterPrecision"
    gas_meter_time = "gasMeterTime"
    gas_meter_volume = "gasMeterVolume"
    heating_setpoint = "heatingSetpoint"
    heating_setpoint_range = "heatingSetpointRange"
    hue = "hue"
    humidity = "humidity"
    icv = "icv"
    illuminance = "illuminance"
    infrared_level = "infraredLevel"
    input_source = "inputSource"
    level = "level"
    lighting_mode = "lightingMode"
    lock = "lock"
    lqi = "lqi"
    machine_state = "machineState"
    mndt = "mndt"
    mnfv = "mnfv"
    mnhw = "mnhw"
    mnml = "mnml"
    mnmn = "mnmn"
    mnmo = "mnmo"
    mnos = "mnos"
    mnpv = "mnpv"
    mnsl = "mnsl"
    motion = "motion"
    mute = "mute"
    n = "n"
    number_of_buttons = "numberOfButtons"
    odor_level = "odorLevel"
    operation_time = "operationTime"
    oven_job_state = "ovenJobState"
    oven_mode = "ovenMode"
    oven_setpoint = "ovenSetpoint"
    pi = "pi"
    playback_repeat_mode = "playbackRepeatMode"
    playback_shuffle = "playbackShuffle"
    playback_status = "playbackStatus"
    power = "power"
    power_consumption = "powerConsumption"
    power_source = "powerSource"
    presence = "presence"
    progress = "progress"
    rapid_cooling = "rapidCooling"
    refrigeration_setpoint = "refrigerationSetpoint"
    robot_cleaner_cleaning_mode = "robotCleanerCleaningMode"
    robot_cleaner_movement = "robotCleanerMovement"
    robot_cleaner_turbo_mode = "robotCleanerTurboMode"
    rssi = "rssi"
    saturation = "saturation"
    schedule = "schedule"
    smoke = "smoke"
    sound = "sound"
    st = "st"
    supported_ac_fan_modes = "supportedAcFanModes"
    supported_ac_modes = "supportedAcModes"
    supported_button_values = "supportedButtonValues"
    supported_input_sources = "supportedInputSources"
    supported_machine_states = "supportedMachineStates"
    supported_playback_commands = "supportedPlaybackCommands"
    supported_thermostat_fan_modes = "supportedThermostatFanModes"
    supported_thermostat_modes = "supportedThermostatModes"
    switch = "switch"
    tamper = "tamper"
    temperature = "temperature"
    thermostat_fan_mode = "thermostatFanMode"
    thermostat_mode = "thermostatMode"
    thermostat_operating_state = "thermostatOperatingState"
    thermostat_setpoint = "thermostatSetpoint"
    thermostat_setpoint_range = "thermostatSetpointRange"
    three_axis = "threeAxis"
    tv_channel = "tvChannel"
    tv_channel_name = "tvChannelName"
    tvoc_level = "tvocLevel"
    ultraviolet_index = "ultravioletIndex"
    valve = "valve"
    vid = "vid"
    voltage = "voltage"
    volume = "volume"
    washer_job_state = "washerJobState"
    washer_mode = "washerMode"
    water = "water"
    window_shade = "windowShade"


ATTRIBUTE_ON_VALUES = {
    Attribute.acceleration: "active",
    Attribute.contact: "open",
    Attribute.filter_status: "replace",
    Attribute.motion: "active",
    Attribute.mute: "muted",
    Attribute.playback_shuffle: "enabled",
    Attribute.presence: "present",
    Attribute.sound: "detected",
    Attribute.switch: "on",
    Attribute.tamper: "detected",
    Attribute.valve: "open",
    Attribute.water: "wet",
}

ATTRIBUTE_OFF_VALUES = {
    Attribute.acceleration: "inactive",
    Attribute.contact: "closed",
    Attribute.filter_status: "normal",
    Attribute.motion: "inactive",
    Attribute.mute: "unmuted",
    Attribute.playback_shuffle: "disabled",
    Attribute.presence: "not present",
    Attribute.sound: "not detected",
    Attribute.switch: "off",
    Attribute.tamper: "clear",
    Attribute.valve: "closed",
    Attribute.water: "dry",
}
