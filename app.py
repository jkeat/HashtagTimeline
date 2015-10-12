import os, datetime
from flask import Flask, render_template
from TwitterAPI import TwitterAPI


app = Flask(__name__)

@app.route('/')
def search():
	return render_template("search.html")

@app.route('/<username>/<hashtag>')
def timeline(username, hashtag):
	
	twitter = TwitterAPI(os.environ['CONSUMER_KEY'],
						 os.environ['CONSUMER_SECRET'],
						 os.environ['ACCESS_TOKEN'],
						 os.environ['ACCESS_TOKEN_SECRET'])

	tweet_query_results = twitter.request('statuses/user_timeline',
										  {'screen_name': username,
										   'count': 200,
										   'include_rts': 'false',
										   'exclude_replies': 'true'})
	tweet_matches = []
	for tweet in tweet_query_results:
		if "#{0}".format(hashtag).lower() in tweet['text'].lower():
			tweet['created_at_datetime'] = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
			tweet_matches = [tweet] + tweet_matches
	if not tweet_matches:
		return render_template("no-results.html", hashtag=hashtag)
	return render_template("timeline.html", tweets=tweet_matches, hashtag=hashtag)


@app.template_filter()
def relativedate(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
    	if day_diff == 1:
    		return "1 day ago"
        return str(day_diff) + " days ago"
    if day_diff < 31:
    	week_diff = day_diff / 7
    	if week_diff == 1:
    		return "1 week ago"
        return str(week_diff) + " weeks ago"
    if day_diff < 365:
    	month_diff = day_diff / 30
    	if month_diff == 1:
    		return "1 month ago"
        return str(month_diff) + " months ago"
    return str(day_diff / 365) + " years ago"

app.jinja_env.filters['relativedate'] = relativedate

@app.template_filter()
def prettydate(d):
	return d.strftime("%b %-d, %Y")

app.jinja_env.filters['prettydate'] = prettydate


if __name__ == "__main__":
    app.run(debug=os.environ['DEBUG'])


"""
TODO
> link to twitter profile
    > link to each tweet?
> back to home button / logo
> 'Android' matches #Android and #AndroidWear
> split up CSS
> lots of bottom messages
	> is that all, folks?
	> to be continued
	> this is the end
	> that's all, folks!
	> now what?
	> you are here
	> ?
> get correct capitalization by looking @ first tweet
> 404 page
> start/end dates
> get ALL tweets, not just 200 
	> loop, get id of last one, start there if there are more
"""