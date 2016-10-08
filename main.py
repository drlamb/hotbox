from datetime import timedelta, datetime
from time import sleep
import temperature
from sense_hat import SenseHat
import sms
import facerec

MIN_BACKOFF = timedelta(seconds=5)
MAX_BACKOFF = timedelta(minutes=10)

TEMP_THRESHOLD = 60 # Fahrenheit
HOT_THRESHOLD = 75 # or 80

# Creates the pretty pictures to display on the Sense-Hat
X = (0, 255, 0)
Y = (255, 0, 0)
Z = (255, 255, 0)
O = (0, 0, 0)

smiley = [
X, X, X, X, X, X, X, X,
X, O, O, O, O, O, O, X,
X, O, X, O, O, X, O, X,
X, O, O, O, O, O, O, X,
X, O, X, O, O, X, O, X,
X, O, O, X, X, O, O, X,
X, O, O, O, O, O, O, X,
X, X, X, X, X, X, X, X]

meh = [
Z, Z, Z, Z, Z, Z, Z, Z,
Z, O, O, O, O, O, O, Z,
Z, O, Z, O, O, Z, O, Z,
Z, O, O, O, O, O, O, Z,
Z, O, O, O, O, O, O, Z,
Z, O, Z, Z, Z, Z, O, Z,
Z, O, O, O, O, O, O, Z,
Z, Z, Z, Z, Z, Z, Z, Z]

frown = [
Y, Y, Y, Y, Y, Y, Y, Y,
Y, O, O, O, O, O, O, Y,
Y, O, Y, O, O, Y, O, Y,
Y, O, O, O, O, O, O, Y,
Y, O, O, Y, Y, O, O, Y,
Y, O, Y, O, O, Y, O, Y,
Y, O, O, O, O, O, O, Y,
Y, Y, Y, Y, Y, Y, Y, Y]

def set_lights(sensehat, temperature):
    if temperature > 75:
        sensehat.set_pixels(frown)
    elif temperature >= 60:
        sensehat.set_pixels(meh)
    else:
        sensehat.set_pixels(smiley)

def main():
    """
    Main loop that runs to check on the car's temperature, speed, and location
    (if authorities are needed).
    """
    backoff = timedelta(seconds=5)
    
    start_time = None
    start_temp = 0

    sensehat = SenseHat()

    while True:
        # Wait until checking again
        sleep(backoff.total_seconds())

        # Before checking temperature, check that car is moving.
        speed = sensehat.get_accelerometer_raw()
        if speed['x'] > 1 or speed['y'] > 1 or speed['z'] > 1:
            print("Car still moving, increasing backoff")
            sensehat.clear()
            start_temp = 0
            start_time = None
            n_sec = backoff.total_seconds() + 120 if backoff.total_seconds() <= 60 * 8 else 10 * 60
            backoff = timedelta(seconds=n_sec)
            continue

        # If car is still, detect if there's a face in there.
        if not facerec.detected_person():
            print("No face detected, increasing backoff")
            sensehat.clear()
            start_temp = 0
            start_time = None
            n_sec = backoff.total_seconds() + 120 if backoff.total_seconds() <= 60 * 8 else 10 * 60
            backoff = timedelta(seconds=n_sec)
            continue
            
        # Check the temperature
        current_temp = temperature.get_temp()
        set_lights(sensehat, current_temp)
        if current_temp < TEMP_THRESHOLD:
            # Resets timer and start temp, and increases backoff
            print("Too cold, delaying backoff")
            start_temp = 0
            start_time = None
            n_sec = backoff.total_seconds() + 120 if backoff.total_seconds() <= 60 * 8 else 10 * 60
            backoff = timedelta(seconds=n_sec)
            continue
    
        elif current_temp >= TEMP_THRESHOLD:
            # Decreases backoff
            print("Getting warmer...")
            if start_temp == 0:
                # Sets the new start temperature and time.
                n_sec = backoff.total_seconds() - 120 if backoff.total_seconds() > 60 * 3 else 60 * 1
                backoff = timedelta(seconds=n_sec)
                start_time = datetime.today()
                start_temp = current_temp
            delta = (datetime.today() - start_time).total_seconds() / 60
            sms.send_text("Please Check on your car's passenger(s)!",
                          current_temp,
                          current_temp - start_temp,
                          delta)

if __name__ == "__main__":
    main()
    
