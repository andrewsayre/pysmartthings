"""
Defines SmartThings capabilities and attributes.

https://smartthings.developer.samsung.com/docs/api-ref/capabilities.html
"""

CAPABILITIES_TO_ATTRIBUTES = {
    'accelerationSensor': ['acceleration'],
    'activityLightingMode': ['lightingMode'],
    'airConditionerMode': ['airConditionerMode'],
    'airQualitySensor': ['airQuality'],
    'alarm': ['alarm'],
    'audioMute': ['mute'],
    'audioVolume': ['volume'],
    'battery': ['battery'],
    'bodyMassIndexMeasurement': ['bmiMeasurement'],
    'bodyWeightMeasurement': ['bodyWeightMeasurement'],
    'button': ['button', 'numberOfButtons', 'supportedButtonValues'],
    'carbonDioxideMeasurement': ['carbonDioxide'],
    'carbonMonoxideDetector': ['carbonMonoxide'],
    'carbonMonoxideMeasurement': ['carbonMonoxideLevel'],
    'colorControl': ['color', 'hue', 'saturation'],
    'colorTemperature': ['colorTemperature'],
    'contactSensor': ['contact'],
    'dishwasherMode': ['dishwasherMode'],
    'dishwasherOperatingState': ['machineState', 'supportedMachineStates',
                                 'dishwasherJobState', 'completionTime'],
    'doorControl': ['door'],
    'dryerMode': ['dryerMode'],
    'dryerOperatingState': ['machineState', 'supportedMachineStates',
                            'dryerJobState', 'completionTime'],
    'dustSensor': ['fineDustLevel', 'dustLevel'],
    'energyMeter': ['energy'],
    'equivalentCarbonDioxideMeasurement': ['equivalentCarbonDioxideMeasurement'],
    'fanSpeed': ['fanSpeed'],
    'filterStatus': ['filterStatus'],
    'formaldehydeMeasurement': ['formaldehydeLevel'],
    'garageDoorControl': ['door'],
    'illuminanceMeasurement': ['illuminance'],
    'infraredLevel': ['infraredLevel'],
    'lock': ['lock'],
    'mediaInputSource': ['inputSource', 'supportedInputSources'],
    'mediaPlaybackRepeat': ['playbackRepeatMode'],
    'mediaPlaybackShuffle': ['playbackShuffle'],
    'mediaPlayback': ['playbackStatus', 'supportedPlaybackCommands'],
    'motionSensor': ['motion'],
    'odorSensor': ['odorLevel'],
    'ovenMode': ['ovenMode'],
    'ovenOperatingState': ['machineState', 'supportedMachineStates', 'ovenJobState',
                           'completionTime', 'operationTime', 'progress'],
    'ovenSetpoint': ['ovenSetpoint'],
    'powerMeter': ['power'],
    'powerSource': ['powerSource'],
    'presenceSensor': ['presence'],
    'rapidCooling': ['rapidCooling'],
    'refrigerationSetpoint': ['refrigerationSetpoint'],
    'relativeHumidityMeasurement': ['humidity'],
    'robotCleanerCleaningMode': ['robotCleanerCleaningMode'],
    'robotCleanerMovement': ['robotCleanerMovement'],
    'robotCleanerTurboMode': ['robotCleanerTurboMode'],
    'signalStrength': ['lqi', 'rssi'],
    'smokeDetector': ['smoke'],
    'soundSensor': ['sound'],
    'switchLevel': ['level'],
    'switch': ['switch'],
    'tamperAlert': ['tamper'],
    'temperatureMeasurement': ['temperature'],
    'thermostatCoolingSetpoint': ['coolingSetpoint'],
    'thermostatFanMode': ['thermostatFanMode', 'supportedThermostatFanModes'],
    'thermostatHeatingSetpoint': ['heatingSetpoint'],
    'thermostatMode': ['thermostatMode', 'supportedThermostatModes'],
    'thermostatOperatingState': ['thermostatOperatingState'],
    'thermostatSetpoint': ['thermostatSetpoint'],
    'tvChannel': ['tvChannel'],
    'tvocMeasurement': ['tvocLevel'],
    'ultravioletIndex': ['ultravioletIndex'],
    'valve': ['valve'],
    'voltageMeasurement': ['voltage'],
    'washerMode': ['washerMode'],
    'washerOperatingState': ['machineState', 'supportedMachineStates',
                             'washerJobState', 'completionTime'],
    'waterSensor': ['water'],
    'windowShade': ['windowShade']
}
CAPABILITIES = CAPABILITIES_TO_ATTRIBUTES.keys()
ATTRIBUTES = {attrib
              for attributes in CAPABILITIES_TO_ATTRIBUTES.values()
              for attrib in attributes}


class Capability:
    """Define common capabilities."""

    acceleration_sensor = 'accelerationSensor'
    activity_lighting_mode = 'activityLightingMode'
    air_conditioner_mode = 'airConditionerMode'
    air_quality_sensor = 'airQualitySensor'
    alarm = 'alarm'
    audio_mute = 'audioMute'
    audio_volume = 'audioVolume'
    battery = 'battery'
    body_mass_index_measurement = 'bodyMassIndexMeasurement'
    body_weight_measurement = 'bodyWeightMeasurement'
    button = 'button'
    carbon_dioxide_measurement = 'carbonDioxideMeasurement'
    carbon_monoxide_detector = 'carbonMonoxideDetector'
    carbon_monoxide_measurement = 'carbonMonoxideMeasurement'
    color_control = 'colorControl'
    color_temperature = 'colorTemperature'
    contact_sensor = 'contactSensor'
    dishwasher_mode = 'dishwasherMode'
    dishwasher_operating_state = 'dishwasherOperatingState'
    door_control = 'doorControl'
    dryer_mode = 'dryerMode'
    dryer_operating_state = 'dryerOperatingState'
    dust_sensor = 'dustSensor'
    energy_meter = 'energyMeter'
    equivalent_carbon_dioxide_measurement = 'equivalentCarbonDioxideMeasurement'
    fan_speed = 'fanSpeed'
    filter_status = 'filterStatus'
    formaldehyde_measurement = 'formaldehydeMeasurement'
    garage_door_control = 'garageDoorControl'
    illuminance_measurement = 'illuminanceMeasurement'
    infrared_level = 'infraredLevel'
    lock = 'lock'
    media_input_source = 'mediaInputSource'
    media_playback = 'mediaPlayback'
    media_playback_repeat = 'mediaPlaybackRepeat'
    media_playback_shuffle = 'mediaPlaybackShuffle'
    motion_sensor = 'motionSensor'
    odor_sensor = 'odorSensor'
    oven_mode = 'ovenMode'
    oven_operating_state = 'ovenOperatingState'
    oven_setpoint = 'ovenSetpoint'
    power_meter = 'powerMeter'
    power_source = 'powerSource'
    presence_sensor = 'presenceSensor'
    rapid_cooling = 'rapidCooling'
    refrigeration_setpoint = 'refrigerationSetpoint'
    relative_humidity_measurement = 'relativeHumidityMeasurement'
    robot_cleaner_cleaning_mode = 'robotCleanerCleaningMode'
    robot_cleaner_movement = 'robotCleanerMovement'
    robot_cleaner_turbo_mode = 'robotCleanerTurboMode'
    signal_strength = 'signalStrength'
    smoke_detector = 'smokeDetector'
    sound_sensor = 'soundSensor'
    switch = 'switch'
    switch_level = 'switchLevel'
    tamper_alert = 'tamperAlert'
    temperature_measurement = 'temperatureMeasurement'
    thermostat_cooling_setpoint = 'thermostatCoolingSetpoint'
    thermostat_fan_mode = 'thermostatFanMode'
    thermostat_heating_setpoint = 'thermostatHeatingSetpoint'
    thermostat_mode = 'thermostatMode'
    thermostat_operating_state = 'thermostatOperatingState'
    thermostat_setpoint = 'thermostatSetpoint'
    tv_channel = 'tvChannel'
    tvoc_measurement = 'tvocMeasurement'
    ultraviolet_index = 'ultravioletIndex'
    valve = 'valve'
    voltage_measurement = 'voltageMeasurement'
    washer_mode = 'washerMode'
    washer_operating_state = 'washerOperatingState'
    water_sensor = 'waterSensor'
    window_shade = 'windowShade'


class Attribute:
    """Define common attributes."""

    acceleration = 'acceleration'
    air_conditioner_mode = 'airConditionerMode'
    air_quality = 'airQuality'
    alarm = 'alarm'
    battery = 'battery'
    bmi_measurement = 'bmiMeasurement'
    body_weight_measurement = 'bodyWeightMeasurement'
    button = 'button'
    carbon_dioxide = 'carbonDioxide'
    carbon_monoxide = 'carbonMonoxide'
    carbon_monoxide_level = 'carbonMonoxideLevel'
    color = 'color'
    color_temperature = 'colorTemperature'
    completion_time = 'completionTime'
    contact = 'contact'
    cooling_setpoint = 'coolingSetpoint'
    dishwasher_job_state = 'dishwasherJobState'
    dishwasher_mode = 'dishwasherMode'
    door = 'door'
    dryer_job_state = 'dryerJobState'
    dryer_mode = 'dryerMode'
    dust_level = 'dustLevel'
    energy = 'energy'
    equivalent_carbon_dioxide_measurement = 'equivalentCarbonDioxideMeasurement'
    fan_speed = 'fanSpeed'
    filter_status = 'filterStatus'
    fine_dust_level = 'fineDustLevel'
    formaldehyde_level = 'formaldehydeLevel'
    heating_setpoint = 'heatingSetpoint'
    hue = 'hue'
    humidity = 'humidity'
    illuminance = 'illuminance'
    infrared_level = 'infraredLevel'
    input_source = 'inputSource'
    level = 'level'
    lighting_mode = 'lightingMode'
    lock = 'lock'
    lqi = 'lqi'
    machine_state = 'machineState'
    motion = 'motion'
    mute = 'mute'
    number_of_buttons = 'numberOfButtons'
    odor_level = 'odorLevel'
    operation_time = 'operationTime'
    oven_job_state = 'ovenJobState'
    oven_mode = 'ovenMode'
    oven_setpoint = 'ovenSetpoint'
    playback_repeat_mode = 'playbackRepeatMode'
    playback_shuffle = 'playbackShuffle'
    playback_status = 'playbackStatus'
    power = 'power'
    power_source = 'powerSource'
    presence = 'presence'
    progress = 'progress'
    rapid_cooling = 'rapidCooling'
    refrigeration_setpoint = 'refrigerationSetpoint'
    robot_cleaner_cleaning_mode = 'robotCleanerCleaningMode'
    robot_cleaner_movement = 'robotCleanerMovement'
    robot_cleaner_turbo_mode = 'robotCleanerTurboMode'
    rssi = 'rssi'
    saturation = 'saturation'
    smoke = 'smoke'
    sound = 'sound'
    supported_button_values = 'supportedButtonValues'
    supported_input_sources = 'supportedInputSources'
    supported_machine_states = 'supportedMachineStates'
    supported_playback_commands = 'supportedPlaybackCommands'
    supported_thermostat_fan_modes = 'supportedThermostatFanModes'
    supported_thermostat_modes = 'supportedThermostatModes'
    switch = 'switch'
    tamper = 'tamper'
    temperature = 'temperature'
    thermostat_fan_mode = 'thermostatFanMode'
    thermostat_mode = 'thermostatMode'
    thermostat_operating_state = 'thermostatOperatingState'
    thermostat_setpoint = 'thermostatSetpoint'
    tv_channel = 'tvChannel'
    tvoc_level = 'tvocLevel'
    ultraviolet_index = 'ultravioletIndex'
    valve = 'valve'
    voltage = 'voltage'
    volume = 'volume'
    washer_job_state = 'washerJobState'
    washer_mode = 'washerMode'
    water = 'water'
    window_shade = 'windowShade'


ATTRIBUTE_ON_VALUES = {
    Attribute.acceleration: 'active',
    Attribute.contact: 'open',
    Attribute.filter_status: 'replace',
    Attribute.motion: 'active',
    Attribute.mute: 'muted',
    Attribute.presence: 'present',
    Attribute.sound: 'detected',
    Attribute.switch: 'on',
    Attribute.tamper: 'detected',
    Attribute.valve: 'open',
    Attribute.water: 'wet'
}
