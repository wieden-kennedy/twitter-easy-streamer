"""
You can use these values to kick a listener off for jgttest1
@todo, put in settings module

CONSUMERKEY = "Itih20yY6e3Pno9zAWn4aA"
CONSUMERSECRET = "2hsTMOBuO0eL6arelLeztLYp2buNzJ75Hq33bYyxuYY"
ACCESSTOKEN = "463307634-CXSnhOVJfn4ZG3Mufuk4fsDe9Pl02CFOOtkwCYtM"
ACCESSTOKENSECRET = "FHbIAU0yHg2MJGjonnH2CaXF1McKfZAWpw02QSo2Q"
"""
import signal
import json
import requests
from operator import attrgetter
from tweepy import Stream, API, BasicAuthHandler, StreamListener, OAuthHandler
from tweepy.error import TweepError

DEFAULT_CALLBACK_URL = "http://www.google.com"

class RuleListener(StreamListener):
    """
    A twitter stream listener. Given credentials and a ruleset will listen to twitter indefinitely
    and get a set of filtered tweets.
    """
    def listen(self, rules, consumer_key, consumer_secret, access_token, access_token_secret):
        self._ruleset = rules

        auth_handler = OAuthHandler(consumer_key, consumer_secret)
        auth_handler.set_access_token(access_token, access_token_secret)
        self.stream = Stream(auth_handler, self, timeout=None)

        follow_list = []
        track_list = []
        location_list = []

        self.api = API(auth_handler)

        for rule in self.ruleset:
            if rule.follow:
                for user in rule.follow:
                    follow_list.append(self.api.get_user(user).id)
            if rule.track:
                track_list += rule.track
            if rule.location:
                location_list += rule.location
            if rule.historical:
                for phrase in track_list:
                    for i in range(1, 100):
                        try:
                            results = self.api.search(phrase, rpp=100, page=i)
                            rule.send_tweets_to_callback(results)
                        except TweepError:
                            break
        try:
            signal.signal(signal.SIGTERM, self.disconnect)
            self.stream.filter(follow=follow_list, track=track_list, locations=location_list)
        except KeyboardInterrupt:
            self.stream.disconnect()

    def disconnect(self):
        self.stream.disconnect()

    @property
    def ruleset(self):
        """
        Return the set of rules for this listener, sorted by priority
        """
        return sorted(self._ruleset, key=attrgetter('priority'))

    def on_status(self, status):
        """
        Callback triggered when we receive a matching tweet.
        Print the text and post the tweet's id to the endpoint specified by the given rule.y
        """
        for rule in self.ruleset:
            if rule.match(status):
                requests.post(rule.callback_url, data={"tweet_id": status.id})
                rule.send_tweets_to_callback([status])

        return

    def on_error(self, status_code):
        """
        Error callback. Returns True so the stream doesn't get closed.
        """
        return True;

class Rule:
    """
    A simple class defining a rule for filtering twitter's streaming API
    """
    def __init__(self, priority=0, follow=None, track=None, location=None, callback_url=None, operator=None, on_status=[], historical=False):
        self.priority = priority
        self.follow = follow
        self.track = track
        self.location = location
        self.callback_url = callback_url or DEFAULT_CALLBACK_URL
        self.on_status_callbacks = on_status
        self.operator = operator or "AND"
        self.historical = historical

    def search(self):
        pass

    def match(self, status):
        """
        Determine if the rule matches the given status
        """
        is_match = False
        if self.operator == "OR":
            is_match = True
        else:
            is_match = self.follow_match(status) or self.track_match(status)
        return is_match

    def follow_match(self, status):
        """
        Return True if the given status contains all of the follow usernames
        in our filter.
        """
        if self.follow is not None:
            if self.operator == "AND":
                return all([username in status.user.screen_name for username in self.follow if username])
            else:
                return any([username in status.user.screen_name for username in self.follow if username])

    def track_match(self, status):
        """
        Return True if the given status contains all of the tracked phrases
        in our filter.
        """
        if self.track is not None:
            if self.operator == "AND":
                return all([phrase.lower() in status.text.lower() for phrase in self.track if phrase])
            else:
                return any([phrase.lower() in status.text.lower() for phrase in self.track if phrase])
        

    def send_tweets_to_callback(self, tweets):
        for callback in self.on_status_callbacks:
            callback(tweets)

    @classmethod
    def from_json(cls, json):
        """
        Build a Rule from the given JSON string
        """
        return from_dict(json.loads(json))

    @classmethod
    def from_dict(cls, dict):
        """
        Build a Rule from the given dictionary.
        Expected keys:
        -priority: a number indicating the rule's priority
        -follow: a list of usernames
        -track: a list of strings to search for
        -location: a list of GPS bounding boxes
        -callback_url: the url to post to when a matching tweet is found
        """
        return Rule(**dict)
