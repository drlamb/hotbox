from datetime import timedelta, datetime
from time import sleep
import temperature
from sense_hat import SenseHat
import sms
import facerec

MIN_BACKOFF = timedelta(minutes=1)
MAX_BACKOFF = timedelta(minutes=10)

TEMP_THRESHOLD = 60 # Fahrenheit
HOT_THRESHOLD = 75 # or 80

def main():
    """
    Main loop that runs to check on the car's temperature, speed, and location
    (if authorities are needed).
    """
    backoff = timedelta(minutes=1)
    
    start_time = None
    start_temp = 0

    sensehat = SenseHat()

    while True:
        # Wait until checking again
        sleep(backoff.total_seconds())

        # Before checking temperature, check that car is moving.
        speed = sensehat.get_accelerometer_raw()
        if speed[0] > 1 or speed[1] > 1 or speed[2] > 1:
            print("Car still moving, increasing backoff")
            start_temp = 0
            start_time = None
            backoff.minutes = backoff.minutes + 2 if backoff.minutes <= 8 else MAX_BACKOFF
            continue

        # If car is still, detect if there's a face in there.
        if not facerec.detected_person():
            print("No face detected, increasing backoff")
            start_temp = 0
            start_time = None
            backoff.minutes = backoff.minutes + 2 if backoff.minutes <= 0 else MAX_BACKOFF
            continue
            
        # Check the temperature
        current_temp = 60 #temperature.get_temp()
        
        if current_temp < TEMP_THRESHOLD:
            # Resets timer and start temp, and increases backoff
            print("Too cold, delaying backoff")
            start_temp = 0
            start_time = None
            backoff.minutes = backoff.minutes + 2 if backoff.minutes <= 8 else MAX_BACKOFF
            continue
    
        elif current_temp >= TEMP_THRESHOLD:
            # Decreases backoff
            print("Getting warmer...")
            if start_temp == 0:
                # Sets the new start temperature and time.
                backoff = backoff.minutes - 2 if backoff.minutes >= 2 else MIN_BACKOFF
                start_time = datetime.today()
                start_temp = current_temp
            delta = timedelta(datetime.today() - start_time).total_seconds() / 60
            sms.send_text("Check on your car!",
                          current_temp - start_temp,
                          delta)

if __name__ == "__main__":
    main()
    
