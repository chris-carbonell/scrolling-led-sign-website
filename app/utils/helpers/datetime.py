from datetime import datetime, date
from dateutil import tz

def get_now_text():
    '''
    get string of now time in UTC
    '''
    return datetime.now().strftime("%Y-%m-%d %H:%M:%SZ")  # UTC

def convert_UTC(dt_utc: str | datetime, to_zone="America/Chicago"):
    '''
    convert UTC to to_zone
    https://stackoverflow.com/questions/61831304/utc-to-cst-time-conversion-using-pytz-python-package
    '''

    # check if None
    if dt_utc is None:
        return None

    # parse time
    if isinstance(dt_utc, str):
        dt_utc = datetime.strptime(dt_utc, "%Y-%m-%d %H:%M:%SZ")

    # get zones
    from_zone = tz.gettz("UTC")
    to_zone = tz.gettz(to_zone)

    # get to_zone dt
    dt_to_zone = dt_utc.replace(tzinfo=from_zone).astimezone(to_zone)

    return dt_to_zone