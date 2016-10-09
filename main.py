from datetime import timedelta, datetime
from time import sleep
import temperature
from sense_hat import SenseHat
import sms
import facerec

MIN_BACKOFF = timedelta(seconds=5) #Sets the minimum temperature refesh time
MAX_BACKOFF = timedelta(minutes=10) #Sets the maximum time before the system will check for a temperature change

TEMP_THRESHOLD = 60 # Fahrenheit
HOT_THRESHOLD = 75 # or 80
DANGER_THRESHOLD = 90

# Creates the pretty pictures to display on the Sense-Hat LED Array
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

# A function to call to set the light to the above images depending on the temperature
def set_lights(sensehat, temperature):
    if temperature > HOT_THRESHOLD:
        sensehat.set_pixels(frown)
    elif temperature >= TEMP_THRESHOLD:
        sensehat.set_pixels(meh)
    else:
        sensehat.set_pixels(smiley)

# The main function of Hotbox
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

        clear_data = False
        current_speed = sensehat.get_accelerometer_raw()
        current_temp = temperature.get_temp()

        # Before checking temperature, check that car is moving.
        if abs(speed['x']) > 1 or abs(speed['y']) > 1 or abs(speed['z']) > 1:
            print("Car still moving, increasing backoff")
            clear_data = True

        # If car is still, detect if there's a face in there.
        elif not facerec.detected_person():
            print("No face detected, increasing backoff")
            clear_data = True
            
        # Check the temperature
        elif current_temp < TEMP_THRESHOLD:
            # Resets timer and start temp, and increases backoff
            print("Too cold, delaying backoff")
            set_lights(sensehat, current_temp)
            clear_data = True
    
        elif current_temp >= TEMP_THRESHOLD:
            # Decreases backoff
            print("Getting warmer...")
            set_lights(sensehat, current_temp)
            message = "Don't forget about your car's passenger!"
            
            n_sec = max(backoff.total_seconds() - 120,
                        MIN_BACKOFF.total_seconds())
            backoff = timedelta(n_sec)
            
            if start_temp == 0:
                # Sets the new start temperature and time.
                start_time = datetime.today()
                start_temp = current_temp
                message = "Your car is starting to heat up!"

            if current_temp >= DANGER_THRESHOLD:
                message = "Check your car's passenger NOW."
                backoff = timedelta(MIN_BACKOFF.total_seconds())
                temp_delta = current_temp - start_temp
                time_delta = (datetime.today() - start_time).total_seconds() / 60
                slope = temp_delta / time_delta
                if slope > 1.25:
                    print("Extremely dangerous! Calling parents/authorities.")
                    # sms.voice_call_driver()
                    sms.contact_911()
                    continue

            elif current_temp >= HOT_THRESHOLD:
                # Edging into the danger zone! Minimum backoff possible
                message = "Please check on your car's passenger(s) soon!"
                backoff = timedelta(seconds=MIN_BACKOFF.total_seconds())

            timediff = (datetime.today() - start_time).total_seconds() / 60
            sms.send_text(message,
                          current_temp,
                          current_temp - start_temp,
                          timediff)
            
        if clear_data:
            # Clear previously kept data
            sensehat.clear()
            start_temp = 0
            start_time = None
            n_sec = min(backoff.total_seconds() - 120, MAX_BACKOFF)
            backoff = timedelta(seconds=n_sec)

if __name__ == "__main__":
    main()
    
