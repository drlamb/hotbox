![Alt text](/hotbox_logo.png?raw=true "Logo")

# Hotbox
A program that utilizes a variety of technologies and a raspberry pi to detect the presence of a human in a stopped hot car and and alert the car owner to the potential dangers of prolonged heat exposure. 

## Purpose
So far in 2016, 37 children in the United States alone have died due to being left alone in a hot car. Unfortunatly, this number has averaged around 40 deaths per year since 1998 with 54% of deaths blaimed to the child being forgotten. Hotbox was created during MHacks 8 in Detroit, Michigan in an effort to show that a solution to this problem could be inexpensive (the entire setup costs less than $100) and effective in preventing another innocent child from dying.

![Alt text](/deaths.png?raw=true "Deaths")

Source: http://noheatstroke.org/

## Vision
Hotbox has the potential the detect not only children but adults and pets as well. The Twilio API can be expanded to contact the authorities with the geolocation of the vehicle if the SMS messages to the owner go unanswered with support depending on a particular region's police department. As cars become more and more open, it's not unreasonable to imagine solutions like this could be adapted to control the vehicles climate systems. 


## Hardware Used
* Raspberry Pi 3 
* PiCamera Module v2
* Sense-Hat Module
* USB GPS Module (BU-353 S4)

## Software Used
* Rasbian 
* Python 2.7
* OpenCV
* Twilio
* GPS3
* SenseHat and PiCamera Libraries 
 
## License 
WTFPL Because we don't know any better. Logos Used sourced from and Designed by Freepik (freepik.com)
