from sense_hat import SenseHat
import math #this isn't really needed...yet
sense = SenseHat()
import time


#Converts the measured temperature to Fahrenehit
def convert_to_f(temperature):
    return (temperature*(9/5)) + 32

#Queries the temperature from the sense hat (in celsius)
def get_temp():
    return convert_to_f(sense.get_temperature())

#Gets the humity (a percent from 0 - 100)
def get_humidity():
    return sense.get_humidity()

#calculates what the body really feels
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

red = (255, 0, 0)
green = (0,255,0)
O = [0,0,0]
X = green
smiley = [
X, X, X, X, X, X, X, X,
X, O, O, O, O, O, O, X,
X, O, X, O, O, X, O, X,
X, O, O, O, O, O, O, X,
X, O, X, O, O, X, O, X,
X, O, O, X, X, O, O, X,
X, O, O, O, O, O, O, X,
X, X, X, X, X, X, X, X

]
Y = red
frown = [
Y, Y, Y, Y, Y, Y, Y, Y,
Y, O, O, O, O, O, O, Y,
Y, O, Y, O, O, Y, O, Y,
Y, O, O, O, O, O, O, Y,
Y, O, O, Y, Y, O, O, Y,
Y, O, Y, O, O, Y, O, Y,
Y, O, O, O, O, O, O, Y,
Y, Y, Y, Y, Y, Y, Y, Y

]
def display_temp(temperature):
	temp2 = round(temperature,1)
	if temp2 > 120:
		#sense.show_message(str(temp2), text_colour=red)
		sense.set_pixels(frown)
	else:
		#sense.show_message(str(temp2), text_colour=green)
		sense.set_pixels(smiley)
while True:
	print('Checking temperature now!')
	print(calc_heat_index(get_temp(),get_humidity()))
	display_temp(calc_heat_index(get_temp(),get_humidity()))
	time.sleep(10)