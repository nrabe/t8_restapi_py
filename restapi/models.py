import datetime
import time
from google.appengine.ext import db

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)


def to_dict(intance):
    output = {}
    for key, prop in intance.properties().iteritems():
        value = getattr(intance, key)
        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            # Convert date/datetime to MILLISECONDS-since-epoch (JS "new Date()").
            ms = time.mktime(value.utctimetuple()) * 1000
            ms += getattr(value, 'microseconds', 0) / 1000
            output[key] = int(ms)
        elif isinstance(value, db.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, db.Model):
            output[key] = to_dict(value)
        else:
            raise ValueError('cannot encode ' + repr(prop))

    return output


class Region(db.Model):
    Uid = db.StringProperty(required=True, indexed=True)
    CreatedAt = db.DateTimeProperty(auto_now_add=True)
    UpdatedAt = db.DateTimeProperty(auto_now=True)
    Title = db.StringProperty(required=True)


class RestaurantTag(db.Model):
    Uid = db.StringProperty(required=True, indexed=True)
    CreatedAt = db.DateTimeProperty(auto_now_add=True)
    UpdatedAt = db.DateTimeProperty(auto_now=True)
    Title = db.StringProperty(required=True)


class Restaurant(db.Model):
    Uid = db.StringProperty(required=True, indexed=True)
    CreatedAt = db.DateTimeProperty(auto_now_add=True)
    UpdatedAt = db.DateTimeProperty(auto_now=True)
    Title = db.StringProperty(required=True)
    Details = db.StringProperty(required=False)
    Regions = db.StringListProperty(db.StringProperty, indexed=True)
    Tags = db.StringListProperty(db.StringProperty, indexed=True)
