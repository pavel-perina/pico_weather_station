#!/usr/bin/env python3

# Pavel Perina, 2024-12-31
# based on https://github.com/pavel-perina/pico_weather_station/tree/main/snippets/saturation_vapor_pressure

import numpy as np

def arden_buck_func(T,a=611.21,b=18.678,c=257.14,d=234.5):
    return a * np.exp((b-(T/d))*(T/(c+T)))

def arden_buck(T):
    if (T<0):
        return arden_buck_func(T, 611.15, 23.036, 279.82, 333.7)
    else:
        return arden_buck_func(T, 611.21, 18.564, 255.57, 254.4)

class TemperatureSaturationLUT:
    def __init__(self):
        self.temp_begin = -50.0
        self.temp_end = 100.0
        self.temp_step = 0.5
        self.temperatures = np.linspace(self.temp_begin, self.temp_end, int(self.temp_end-self.temp_begin)*2+1)
        self.pressures    = np.array([arden_buck(T) for T in self.temperatures])

    def lerp(x, x1, x2, y1, y2):
        return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

    def temperature_to_index(self, temp:float):
        index = (temp - self.temp_begin) / self.temp_step
        index = int(index)
        if (index < 0):
            return None
        if (index > len(self.temperatures)):
            return None
        return index

    def index_to_temperature(self, index:int):
        if (index < 0):
            return None
        if (index > len(self.temperatures)):
            return None
        temperature = self.temp_begin + index * self.temp_step
        return temperature

    def lookup_pressure(self, temp:float) -> float:
        index = self.temperature_to_index(temp)
        t0 = self.index_to_temperature(index)
        t1 = t0 + self.temp_step
        p0 = self.pressures[index]
        p1 = self.pressures[index+1]
        return TemperatureSaturationLUT.lerp(temp, t0, t1, p0, p1)

    def lookup_temperature(self, pressure:float) -> float:
        index = np.searchsorted(self.pressures, pressure)
        t0 = self.index_to_temperature(index-1)
        t1 = t0 + self.temp_step
        p0 = self.pressures[index-1]
        p1 = self.pressures[index]
        return TemperatureSaturationLUT.lerp(pressure, p0, p1, t0, t1)

lut_ts = TemperatureSaturationLUT()

def get_sea_level_pressure(pressure, altitude, temperature_celsius = None, vapor_pressure = None, temperature_lapse = 0.0065):
    # Compensate for temperature lapse, this has minimal effect
    temperature = temperature_celsius
    if temperature is None:
        # Use international standard athmosphere - adjust 15C at sea level by altitude (gets colder upwards)
        temperature = 15.0 - temperature_lapse * altitude * 0.5
    else:
        # Adjust temperature at station level by altitude (gets warmer downwards)
        temperature = temperature + temperature_lapse * altitude * 0.5

    # Convert to kelvins
    temperature = temperature + 273.15

    # Compensate for humidity
    if (vapor_pressure is not None):
        # Get virtual temperature (dry air has the same density as moist air at current temperature)
        #print(f"TEMP: {temperature}")
        temperature = temperature / (1.0 - vapor_pressure / pressure * (1 - 0.622))
        #print(f"Virtual temp {temperature}")
    pressure = pressure * np.exp(9.80665 * 0.02896968 * altitude / (8.314462618 * temperature))
    return pressure

def mixing_ratio(total_pressure_pa, vapor_pressure_pa):
    """Calculate mixing ratio (dimensionless)"""
    epsilon = 0.62197
    dry_air_pressure = (total_pressure_pa - vapor_pressure_pa)
    return epsilon * vapor_pressure_pa / dry_air_pressure

def specific_humidity(total_pressure_pa, vapor_pressure_pa):
    """Calculate specific humidity in g/g"""
    r = mixing_ratio(total_pressure_pa, vapor_pressure_pa)
    return r/(1.0 + r)


def get_derived_data(temperature_celsius:float, humidity:float, pressure:float, altitude:float, is_outdoor_station:bool):
    # Dew point
    e_s = lut_ts.lookup_pressure(temperature_celsius) # Saturated vapor pressure
    e   = e_s * humidity * 0.01                       # Actual vapor pressure
    dp = lut_ts.lookup_temperature(e)                 # Dew point
    data = []
    data.append(("dew_point", float(dp)))

    if is_outdoor_station:
        p0 = get_sea_level_pressure(pressure, altitude, temperature_celsius, e)
        data.append(("sea_level_pressure", float(p0)))
    else:
        p0 = get_sea_level_pressure(pressure, altitude)
        data.append(("sea_level_pressure", float(p0)))

    sh = specific_humidity(pressure, e)
    data.append( ("specific_humidity", float(sh)) )

    return data

# Tests
if __name__ == '__main__':
    # Test relative humidity look up
    t  = 25.0
    rh = 60.0

    e_s = lut_ts.lookup_pressure(t)
    print("LOOKUP: Saturated vapor pressure for {:.2f} °C is {:.2f} Pa".format(t, e_s))
    e = e_s * rh * .01
    dp = lut_ts.lookup_temperature(e)
    print(f"Considering {rh:.1f}% RH, actual vapor pressure is {e:.2f} Pa, dew point is {dp:.2f} °C")
    e2 = lut_ts.lookup_pressure(dp)
    print("LOOKUP: Saturated vapor pressure for {:.2f} °C is {:.2f} Pa".format(dp, e2))
    print("EVAL:   Saturated vapor pressure for {:.2f} °C is {:.2f} Pa".format(dp, arden_buck(dp)))

    # Test on real data
    # https://www.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/stanice/profesionalni-stanice/prehled-stanic/brno-turany
    # 2025-01-01 11:00
    # -3.5C, 94% RH, 997.9hPa, 241m
    # out: dew point: -4.3C, 1029.3hPa
    t = -3.5
    rh = 94.0
    e_s = lut_ts.lookup_pressure(t)
    print("LOOKUP: Saturated vapor pressure for {:.2f} °C is {:.2f} Pa".format(t, e_s))
    e = e_s * rh * .01
    dp = lut_ts.lookup_temperature(e)
    print(f"Considering {rh:.1f}% RH, actual vapor pressure is {e:.2f} Pa, dew point is {dp:.2f} °C")

    print("Expected result is 1029.3 hPA")
    p = 99790
    alt = 241.0
    p0 = get_sea_level_pressure(p, alt)
    print(f"Sea level pressure for 15C@0m, 0%RH: {p0} Pa")
    p0 = get_sea_level_pressure(p, alt, t)
    print(f"Compensated for temperature: {p0} Pa")
    p0 = get_sea_level_pressure(p, alt, t, e)
    print(f"... and humidity: {p0} Pa")
    p0 = get_sea_level_pressure(p, alt, t, e, 0.0)
    print(f"... and no lapse: {p0} Pa")

# https://www.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/stanice/profesionalni-stanice/prehled-stanic/namest-nad-oslavou

    # 2025-01-01 11:00
    # -4.6C, 94% RH, 968.9hPa, 474m
    # out: dew point: -5.5C, 1028.8hPa
    t = -4.6
    rh = 94.0
    e_s = lut_ts.lookup_pressure(t)
    print("Expected result is 1028.8 hPA")
    print("LOOKUP: Saturated vapor pressure for {:.2f} °C is {:.2f} Pa".format(t, e_s))
    e = e_s * rh * .01
    dp = lut_ts.lookup_temperature(e)
    print(f"Considering {rh:.1f}% RH, actual vapor pressure is {e:.2f} Pa, dew point is {dp:.2f} °C")

    p = 96890
    alt = 474.0
    p0 = get_sea_level_pressure(p, alt)
    print(f"Sea level pressure for 15C@0m, 0%RH: {p0} Pa")
    p0 = get_sea_level_pressure(p, alt, t)
    print(f"Compensated for temperature: {p0} Pa")
    p0 = get_sea_level_pressure(p, alt, t, e)
    print(f"... and humidity: {p0} Pa")
    p0 = get_sea_level_pressure(p, alt, t, e, 0.0)
    print(f"... and no lapse: {p0} Pa")
