from sense_hat import SenseHat
sense = SenseHat()
import time

# Conversts the given temperature to farhaneit 
def convert_temp_to_f(temperature):
	return (temperature*(5/9)+32))

# Returns the temperature, converted to F
def get_temp():
	return convert_temp_to_f(sense.get_temp())

def get_humidity():
	return sense.get_humidity()

# Calculates the real feel temperature from the outside temp and humidtty
def calc_heat_index(temperature, humidity):
    t = temperature
    h = humidity

    #constants for the heat index calculation
    c1 = -42.379
    c2 = 2.04901523
    c3 = 10.14333127
    c4 = -0.22475541
    c5 = -6.83783*10**(-3)
    c6 = -5.481717*10**(-2)
    c7 = 1.22874*10**(-3)
    c8 = 8.5282*10**(-4)
    c9 = -1.99*10**(-6)

    #calculation for heat index
    # https://en.wikipedia.org/wiki/Heat_index
    hi = c1 + (c2*t) + (c3*h) + (c4*t*h) + (c5*(t**2)) + (c6*(h**2)) + (c7*(t**2)*h) + (c8*t*(h**2)) + (c9*(t**2)*(h**2))

# returns the original temperature if the calculated HI is lower
    if hi < t:
        return t
    else:
        return hi


