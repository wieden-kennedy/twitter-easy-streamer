# Twitter Easy Streamer

Streaming from Twitter using tweepy is pretty easy, but you still need to write a lot of the glue code you'd inevitably need to use the status messages you find in your app.

This is a rule-based listener that Grant and I knocked together for a quick Nike thing.

It lives here now, as it's own library - with some additions to make it even easier to use.

### Step 1: Install

    pip install -e "git+git@github.com:wieden-kennedy/twitter-easy-streamer.git#egg=twitter_easy_streamer"

### Step 2: Start with this example

Put this in stream.py

    from twitter_easy_streamer.streamer import Rule, RuleListener

    def print_message(tweet):
        print tweet

    def start():
        listener = RuleListener()
        
        AUTH = {
            'consumer_key': '9ejfkiCu8dTMNDzF29cg',
            'consumer_secret': 'SicnRgAMXu31xvJnpJtqtGOZEZazhDynb7sXLPTnNo',
            'access_token': '14112449-ZDgvgw5Hgj1hf1sZFWP0VSBnJBMOiVhbhgpNDWd5n',
            'access_token_secret': 'ZMtTEXGZ5aNnGrMF03l0lSkqCaouo0CjJbEiN41QlO4'
        }

        rules = [Rule(track=["football"], on_status=[print_message])]
        listener.listen(rules=rules, **AUTH)

    start()

### Step 3: Run

    python stream.py