from flask import Flask, escape, request, jsonify, render_template
import twitter
from flask_caching import Cache
import datetime
from dateutil import tz

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
api = twitter.Api(consumer_key="QUHCT9gGwXPl0GBRNv9TVK8el",
                  consumer_secret="6lkDB4xuuyFsT1GWkcT5YNjdMHjvto5KWWEYHXjZ2DWvpg2doL",
                  access_token_key="173551089-fGOKF1uEDZPolaZLtmPl1xEzpGJyiZivc404wVUL",
                  access_token_secret="UqUTcHJmuNQ3A5XpOF12mGO46CpFsBuR56WfIOih4SNU2")

from_zone = tz.tzutc()
to_zone = tz.tzlocal()


def timeconvert(time):
    newtime = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")
    newtime = newtime.replace(tzinfo=from_zone)
    newtime = newtime.astimezone(to_zone)
    return newtime.strftime("%B %d, %Y - %H:%M:%S")


@cache.memoize(50)
def get_trends(place=None):
    if place==None:
        return api.GetTrendsCurrent()
    else:
        return api.GetTrendsWoeid(place)


def trendlist(trend_obj):
    trends = []
    for trend in trend_obj:
        trtime = timeconvert(trend.timestamp)
        # print(trtime,trend)
        trends.append({"name":trend.name,\
                                 "volume":trend.tweet_volume,\
                                 "time":trtime,\
                                 "url":trend.url})
    return trends


@app.route('/')
def hello():

    trends = {}
    trends["global"] = trendlist(get_trends())
    trends["pakistan"] = trendlist(get_trends(23424922))
    trends["lahore"] = trendlist(get_trends(2211177))
    trends["karachi"] = trendlist(get_trends(2211096))
    trends["india"] = trendlist(get_trends(23424848))

    return render_template("main.html", trends=trends)