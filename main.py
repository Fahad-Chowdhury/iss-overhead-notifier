import requests
from datetime import datetime, timezone
import time
import smtplib
import config


def get_iss_location():
    """ It returns the current latitude and longitude of ISS (International Space Station)
    which is orbiting the earth's surface. """
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return iss_latitude, iss_longitude


def is_iss_close():
    """ It returns True if the ISS (International Space Station) is close to current
    location. ISS is considered close if it is within 5 degrees of current location's
    longitude and latide. """
    iss_latitude, iss_longitude = get_iss_location()
    lat_diff = abs(config.MY_LAT - iss_latitude)
    lng_diff = abs(config.MY_LONG - iss_longitude)
    return lat_diff <= 5 and lng_diff <= 5


def get_local_time_from_utc(utc_dt):
    """ It takes datetime object in UTC format and returns the local time. """
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None).time()


def is_night():
    """ It returns True if it is night at the current location by comparing the current
    time with sunrise and sunset times of the current location. """
    parameters = {
        "lat": config.MY_LAT,
        "lng": config.MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise_dt = datetime.fromisoformat(data["results"]["sunrise"])
    sunrise = get_local_time_from_utc(sunrise_dt)
    sunset_dt = datetime.fromisoformat(data["results"]["sunset"])
    sunset = get_local_time_from_utc(sunset_dt)
    time_now = datetime.now().time()
    return  (time_now > sunset) or (time_now < sunrise)


def send_email_notification():
    """ Send an e-mail notification to look up the sky for ISS. """
    with smtplib.SMTP(config.SMTP_SERVER, port=config.SMTP_PORT) as connection:
        connection.starttls()
        connection.login(user=config.MY_EMAIL, password=config.PASSWORD)
        email_msg = f"Subject:Look Up!\n\nISS is above you in the sky."
        connection.sendmail(from_addr=config.MY_EMAIL, to_addrs=config.MY_EMAIL,
                            msg=email_msg)


def iss_overhead_notifier():
    """ Main method to execute ISS-overhead-notifier app. It checks every minute
    if ISS is close to current location (set in config moule), and if is night time.
    It sends email notification if ISS can be seen in the sky. """
    while True:
        if is_iss_close() and is_night():
            send_email_notification()
        time.sleep(60)


if __name__ == "__main__":
    iss_overhead_notifier()
