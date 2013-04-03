from twitter_easy_streamer.streamer import Rule, RuleListener

def print_message(tweets, *args, **kwargs):
    print args
    print tweets[0].text

def start():
    listener = RuleListener()

    AUTH = {
        'consumer_key': '9ejfkiCu8dTMNDzF29cg',
        'consumer_secret': 'SicnRgAMXu31xvJnpJtqtGOZEZazhDynb7sXLPTnNo',
        'access_token': '14112449-ZDgvgw5Hgj1hf1sZFWP0VSBnJBMOiVhbhgpNDWd5n',
        'access_token_secret': 'ZMtTEXGZ5aNnGrMF03l0lSkqCaouo0CjJbEiN41QlO4'
    }

    rules = [Rule(track=["slim"], historical=True, on_status=[print_message])]
    listener.listen(rules=rules, **AUTH)

start()
