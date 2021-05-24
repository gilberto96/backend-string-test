import datetime

def valid_datetime(datestr):
    try:
        datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def str_to_date(datestr):
    return datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
