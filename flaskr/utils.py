import datetime
import json

def valid_datetime(datestr):
    try:
        datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def str_to_date(datestr):
    return datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')

def compare(obj1, obj2):
    return json.dumps(obj1) == json.dumps(obj2)