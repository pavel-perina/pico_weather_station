from saturation_table import saturation_table as sat_table

def interpolate(x, x1, x2, y1, y2):
   return y1 + (x - x1) * (y2 - y1) / (x2 - x1)

def find_pressure(temp):
   for i in range(len(sat_table)-1):
       if sat_table[i][0] <= temp <= sat_table[i+1][0]:
           return interpolate(temp, 
               sat_table[i][0], sat_table[i+1][0],
               sat_table[i][1], sat_table[i+1][1])
   return None

def find_temp(pressure):
   for i in range(len(sat_table)-1):
       if sat_table[i][1] <= pressure <= sat_table[i+1][1]:
           return interpolate(pressure,
               sat_table[i][1], sat_table[i+1][1],
               sat_table[i][0], sat_table[i+1][0])
   return None

# Test
e_s = find_pressure(25)
e = e_s * 0.1
print(find_temp(e))

e_s = find_pressure(50)
e = e_s * 0.9
print(find_temp(e))

# The temperature is 0 °C, with a wind chill of -4 °C.
# The dew point is -4 °C, the relative humidity is 75%. The air pressure at sea level is 1032 hPa (QNH).
e_s = find_pressure(0)
e = e_s * 0.75
print(find_temp(e))
