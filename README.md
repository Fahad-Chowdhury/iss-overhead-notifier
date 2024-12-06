# ** ISS Overhead Notifier **


## About
An `ISS Overhead Notifier` application is developed in Python using the `requests` package for handling API interactions and the `smtplib` package for sending email notifications.

It fetches the location (latitude and longitude) of the ISS (International Space Station) from the `http://api.open-notify.org` API server, which revolves around the Earth. It checks if the ISS is close to the current location and if it is nighttime in the current location, meaning the ISS can be observed in the sky from that location. In that case, an email notification is sent to look up at the sky to observe the ISS.


## Developed Using:
[Python](https://www.python.org/)

## Dependencies:
- Python v3.6+
- requests
- smtplib


## Contact Information:
Fahad Chowdhury\
[LinkedIn](https://www.linkedin.com/in/fahad-chowdhury-fi)\
[GitHub](https://github.com/Fahad-Chowdhury)
