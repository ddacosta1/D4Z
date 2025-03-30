"""Tuya Power Meter."""

from collections.abc import ByteString

from zigpy.quirks.v2 import SensorDeviceClass, SensorStateClass
from zigpy.quirks.v2.homeassistant import (
    UnitOfElectricCurrent,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfElectricPotential,
    UnitOfFrequency,
    UnitOfConductivity,
)
import zigpy.types as t
from zigpy.zcl.clusters.general import LevelControl, OnOff
from zigpy.zcl.clusters.homeautomation import ElectricalMeasurement

from zhaquirks.tuya import DPToAttributeMapping, TuyaLocalCluster
from zhaquirks.tuya.builder import TuyaQuirkBuilder


def dp_to_power(data: ByteString) -> int:
    """Convert DP data to power value."""
    # From https://github.com/Koenkk/zigbee2mqtt/issues/18603#issuecomment-2277697295
    power = int(data)
    if power > 0x0FFFFFFF:
        power = (0x1999999C - power) * -1
    return power


def multi_dp_to_power(data: ByteString) -> int:
    """Convert DP data to power value."""
    # Support negative power readings
    # From https://github.com/Koenkk/zigbee2mqtt/issues/18603#issuecomment-2277697295
    power = data[7] | (data[6] << 8)
    if power > 0x7FFF:
        power = (0x999A - power) * -1
    return power


def multi_dp_to_current(data: ByteString) -> int:
    """Convert DP data to current value."""
    return data[4] | (data[3] << 8)


def multi_dp_to_voltage(data: ByteString) -> int:
    """Convert DP data to voltage value."""
    return data[1] | (data[0] << 8)


class Tuya3PhaseElectricalMeasurement(ElectricalMeasurement, TuyaLocalCluster):
    """Tuya Electrical Measurement cluster."""

    _CONSTANT_ATTRIBUTES = {
        ElectricalMeasurement.AttributeDefs.ac_current_multiplier.id: 1,
        ElectricalMeasurement.AttributeDefs.ac_current_divisor.id: 1000,
        ElectricalMeasurement.AttributeDefs.ac_voltage_multiplier: 1,
        ElectricalMeasurement.AttributeDefs.ac_voltage_divisor.id: 10,
    }
(
    TuyaQuirkBuilder("_TZE204_loejka0i", "TS0601")
    # Energy
    .tuya_sensor(
        dp_id=1,
        attribute_name="energy",
        type=t.int32s,
        divisor=1000,
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        fallback_name="Total energy",
    )
    .tuya_sensor(
        dp_id=2,
        attribute_name="produced_energy",
        type=t.int32s,
        divisor=100,
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        fallback_name="Total energy",
    )
    .tuya_sensor(
        dp_id=15,
        attribute_name="power_factor",
        type=t.int32s,
        divisor=1000,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER_FACTOR,
        fallback_name="Power Factor",
    )
    .tuya_sensor(
        dp_id=101,
        attribute_name="ac_frequency",
        type=t.int32s,
        divisor=100,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.FREQUENCY,
        unit=UnitOfFrequency.HERTZ,
        fallback_name="Power Factor",
    )
    .tuya_sensor(
        dp_id=102,
        attribute_name="voltage_a",
        type=t.int32s,
        divisor=10,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.VOLTAGE,
        unit=UnitOfElectricPotential.VOLT,
        fallback_name="Voltage phase a",
    )    
    .tuya_sensor(
        dp_id=103,
        attribute_name="current_a",
        type=t.int32s,
        divisor=1000,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.CURRENT,
        unit=UnitOfElectricCurrent.AMPERE,
        fallback_name="Current phase a",
    )
    .tuya_sensor(
        dp_id=104,
        attribute_name="power_a",
        type=t.int32s,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.APPARENT_POWER,
        unit=UnitOfPower.WATT,
        translation_key="power_a",
        fallback_name="Energy phase A",
    )
    .tuya_sensor(
        dp_id=105,
        attribute_name="voltage_b",
        type=t.int32s,
        divisor=10,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.VOLTAGE,
        unit=UnitOfElectricPotential.VOLT,
        fallback_name="Voltage phase b",
    )    
    .tuya_sensor(
        dp_id=106,
        attribute_name="current_b",
        type=t.int32s,
        divisor=1000,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.CURRENT,
        unit=UnitOfElectricCurrent.AMPERE,
        fallback_name="Current phase b",
    )
    .tuya_sensor(
        dp_id=107,
        attribute_name="power_b",
        type=t.int32s,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.APPARENT_POWER,
        unit=UnitOfPower.WATT,
        translation_key="power_b",
        fallback_name="Energy phase b",
    )
    .tuya_sensor(
        dp_id=108,
        attribute_name="voltage_c",
        type=t.int32s,
        divisor=10,        
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.VOLTAGE,
        unit=UnitOfElectricPotential.VOLT,
        fallback_name="Voltage phase c",
    )    
    .tuya_sensor(
        dp_id=109,
        attribute_name="current_c",
        type=t.int32s,
        divisor=1000,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.CURRENT,
        unit=UnitOfElectricCurrent.AMPERE,
        fallback_name="Current phase c",
    )
    .tuya_sensor(
        dp_id=110,
        attribute_name="power_c",
        type=t.int32s,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.APPARENT_POWER,
        unit=UnitOfPower.WATT,
        translation_key="power_c",
        fallback_name="Energy phase c",
    )
    .tuya_sensor(
        dp_id=111,
        attribute_name="power",
        type=t.int32s,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.APPARENT_POWER,
        unit=UnitOfPower.WATT,
        translation_key="power",
        fallback_name="Energy",
    )    
    .tuya_sensor(
        dp_id=112,
        attribute_name="energy_ph_a",
        type=t.int32s,
        divisor=1000,
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        translation_key="energy_ph_a",
        fallback_name="Energy phase A",
    )
    .tuya_sensor(
        dp_id=113,
        attribute_name="energy_produced_a",
        type=t.int32s,
        divisor=100,
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        translation_key="energy_produced_a",
        fallback_name="Energy produced phase A",
    )
    .tuya_sensor(
        dp_id=114,
        attribute_name="energy_ph_b",
        type=t.int32s,
        divisor=100,
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        translation_key="energy_ph_b",
        fallback_name="Energy phase B",
    )
    .tuya_sensor(
        dp_id=115,
        attribute_name="energy_produced_b",
        type=t.int32s,
        divisor=100,
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        translation_key="energy_produced_b",
        fallback_name="Energy produced phase B",
    )
    .tuya_sensor(
        dp_id=116,
        attribute_name="energy_ph_c",
        type=t.int32s,
        divisor=100,
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        translation_key="energy_ph_c",
        fallback_name="Energy phase C",
    )
    .tuya_sensor(
        dp_id=117,
        attribute_name="energy_produced_c",
        type=t.int32s,
        divisor=100,
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.ENERGY,
        unit=UnitOfEnergy.KILO_WATT_HOUR,
        translation_key="energy_produced_c",
        fallback_name="Energy produced phase C",
    )    
    .tuya_sensor(
        dp_id=118,
        attribute_name="power_factor_ph_a",
        type=t.int32s,
        divisor=1000,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER_FACTOR,
        translation_key="energy_produced_a",
        fallback_name="Energy produced phase A",
    )    
    .tuya_sensor(
        dp_id=119,
        attribute_name="power_factor_ph_b",
        type=t.int32s,
        divisor=1000,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER_FACTOR,
        translation_key="energy_produced_b",
        fallback_name="Energy produced phase B",
    )    
    .tuya_sensor(
        dp_id=120,
        attribute_name="power_factor_ph_c",
        type=t.int32s,
        divisor=1000,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER_FACTOR,
        translation_key="energy_produced_c",
        fallback_name="Energy produced phase C",
    )    
    .removes(LevelControl.cluster_id)
    .removes(OnOff.cluster_id)
    .skip_configuration()
    .add_to_registry()
)
