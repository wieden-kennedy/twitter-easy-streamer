"""
You can use these values to kick a listener off for jgttest1
@todo, put in settings module

CONSUMERKEY = "Itih20yY6e3Pno9zAWn4aA"
CONSUMERSECRET = "2hsTMOBuO0eL6arelLeztLYp2buNzJ75Hq33bYyxuYY"
ACCESSTOKEN = "463307634-CXSnhOVJfn4ZG3Mufuk4fsDe9Pl02CFOOtkwCYtM"
ACCESSTOKENSECRET = "FHbIAU0yHg2MJGjonnH2CaXF1McKfZAWpw02QSo2Q"
"""
import json
import requests
from operator import attrgetter
from tweepy import Stream, API, BasicAuthHandler, StreamListener, OAuthHandler

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
        
        for rule in self.ruleset:
            if rule.follow:
                for user in rule.follow:                                       
                    follow_list.append(API(auth_handler).get_user(user).id)
            if rule.track:
                track_list += rule.track
            if rule.location:
                location_list += rule.location
        self.stream.filter(follow=follow_list, track=track_list, locations=location_list)
            
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
                for callback in rule.on_status_callbacks:
                    callback(status)

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
    def __init__(self, priority=0, follow=None, track=None, location=None, callback_url=None, operator=None, on_status=[]):
        self.priority = priority
        self.follow = follow
        self.track = track
        self.location = location       
        self.callback_url = callback_url or DEFAULT_CALLBACK_URL
        self.on_status_callbacks = on_status
        self.operator = operator or "AND"

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
            return all(["@"+username in status.text for username in self.follow])

    def track_match(self, status):
        """
        Return True if the given status contains all of the tracked phrases
        in our filter.
        """
        return all([phrase in status.text for phrase in self.track])

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
        
        
def main(consumerkey, consumersecret, accesstoken, accesstokensecret):
    listener = RuleListener()
    listener.listen(consumerkey, consumersecret, accesstoken, accesstokensecret, [Rule(follow=["realgrantthomas",], track=["salami",])])
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('consumerkey', action="store")
    parser.add_argument('consumersecret', action="store")
    parser.add_argument('accesstoken', action="store")
    parser.add_argument('accesstokensecret', action="store")
    values = parser.parse_args()

    try:
        main(values.consumerkey, values.consumersecret, values.accesstoken, values.accesstokensecret)
    except KeyboardInterrupt:
        print "\nAll Done!"