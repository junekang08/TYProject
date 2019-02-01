from pymongo import MongoClient
import json
import tweepy

creds = None 
MONGO_HOST= 'mongodb://junekang08:Rf860704!@cluster0-shard-00-00-cnddh.mongodb.net:27017,cluster0-shard-00-01-cnddh.mongodb.net:27017,cluster0-shard-00-02-cnddh.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
WORDS = ['Crohn','crohn\'s', 'crohns', 'cron\'s', 'crons', 'ulcerative','colitis',
		 'ibd', 'inflammatory bowel','inflamatory bowel', 'bowel disease']

with open("twitter_credentials.json", "r") as file:
	creds = json.load(file)

# print(creds)

class StreamListener(tweepy.StreamListener):
	def on_connect(self):
		print("You are now connected to the streaming API")

	def on_error(self, status_code):
		print('An Error has occured: ' + repr(status_code))
		return False

	def on_data(self, data):
		try:
			myDict	    	= {}
			client 	    	= MongoClient(MONGO_HOST)
			db 		    	= client.IBDTweets
			datajson    	= json.loads(data)
			created_at  	= datajson['created_at']
			lang 	    	= datajson['lang']
			user	        = datajson['user']
			isCopyOfRetweet = datajson['text'][:3] == 'RT '
			retweetedStatus = datajson.get('retweeted_status')
			retweeted 		= isCopyOfRetweet and retweetedStatus
			if (not retweeted):
				tweet = filterTweet(datajson)
				print("Text: " + tweet['text'])
				print("Language is: " + lang)
				if lang=='en' and user['lang']=='en':	
					print("Tweet collected at " + str(created_at))	
					db.tweet.insert(tweet)
		except Exception as e:
			print(e)

def filterTweet(rawTweet):
	myDict = {}
	user   = rawTweet['user']
	# Dealing with truncated texts.
	if (rawTweet['truncated']):
		text = rawTweet['extended_tweet']['full_text']
	else:
		text = rawTweet['text']
	# Removing mentions.
	text = " ".join(filter(lambda x:x[0]!='@', text.split()))
	myDict.update(id=rawTweet['id'],createdAt=rawTweet['created_at'],text=text, userID=user['id'], userLocation=user['location'])
	return myDict

print(creds["CONSUMER_KEY"])
auth = tweepy.OAuthHandler(creds["CONSUMER_KEY"], creds["CONSUMER_SECRET"])
auth.set_access_token(creds["ACCESS_TOKEN"], creds["ACCESS_SECRET"])
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(languages=["en"], track=WORDS)
