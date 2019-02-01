from twython import Twython
import json

# credentials = {}
# credentials['CONSUMER_KEY'] = "GscLLZJLQzVlBBKKTJaM1FoXN"
# credentials['CONSUMER_SECRET'] = "nO7zaYoiWHROlaKqZGnnPKzncmJjWtm32lrjgmwSMPJwN1sN33"
# credentials['ACCESS_TOKEN'] = "241300826-CMtXmTmZLXTa0b3gVlJzPpi71bdtUKnrkkD2icve"
# credentials['ACCESS_SECRET'] = "fxWXY3aEDBqOwrTwDRlAoBUBAVoOdDi3w0FoqWN1uaMfO"

# with open("twitter_credentials.json", "w") as file:
# 	json.dump(credentials, file)

with open("twitter_credentials.json", "r") as file:
	creds = json.load(file)

tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

# print(creds)

query - { 'q': 'crohn', 'result_type': 'mixed', 'count': 10, 'lang': 'en'}



