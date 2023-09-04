import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class TwitterTrendAnalyzer:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def get_trending_topics(self):
        trends = self.api.trends_place(1)
        trending_topics = []

        for trend in trends[0]["trends"]:
            if trend["name"].startswith("#"):
                trending_topics.append(trend["name"])

        return trending_topics

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0:
            return "positive"
        elif polarity < 0:
            return "negative"
        else:
            return "neutral"

    def generate_word_cloud(self, text):
        wordcloud = WordCloud().generate(text)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

    def track_hashtag(self, hashtag):
        tweets = tweepy.Cursor(self.api.search, q=hashtag).items(100)
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        user_demographics = {}

        for tweet in tweets:
            sentiment = self.analyze_sentiment(tweet.text)

            if sentiment == "positive":
                positive_count += 1
            elif sentiment == "negative":
                negative_count += 1
            else:
                neutral_count += 1

            user_demographics[tweet.user.id] = {
                "username": tweet.user.screen_name,
                "followers": tweet.user.followers_count,
                "location": tweet.user.location
            }

        total_engagement = positive_count + negative_count + neutral_count

        positive_percent = (positive_count / total_engagement) * 100
        negative_percent = (negative_count / total_engagement) * 100
        neutral_percent = (neutral_count / total_engagement) * 100

        self.generate_user_demographics_report(user_demographics)

        print("Sentiment Analysis Results:")
        print("Positive: {:.2f}%".format(positive_percent))
        print("Negative: {:.2f}%".format(negative_percent))
        print("Neutral: {:.2f}%".format(neutral_percent))

    def generate_user_demographics_report(self, user_demographics):
        report = "User Demographics:\n"

        for user_id, user_info in user_demographics.items():
            report += "Username: {}\n".format(user_info["username"])
            report += "Followers: {}\n".format(user_info["followers"])
            report += "Location: {}\n".format(user_info["location"])
            report += "\n"

        print(report)

if __name__ == "__main__":
    # Twitter API credentials
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

    twitter_analyzer = TwitterTrendAnalyzer(consumer_key, consumer_secret, access_token, access_token_secret)
    trending_topics = twitter_analyzer.get_trending_topics()

    print("Trending Topics:")
    for i, topic in enumerate(trending_topics):
        print("{}. {}".format(i + 1, topic))

    trend_index = int(input("Enter the index of the trend you want to analyze: "))
    trend = trending_topics[trend_index - 1]

    tweets = tweepy.Cursor(twitter_analyzer.api.search, q=trend).items(100)
    tweet_texts = [tweet.text for tweet in tweets]

    sentiment_scores = [twitter_analyzer.analyze_sentiment(text) for text in tweet_texts]

    all_text = " ".join(tweet_texts)
    twitter_analyzer.generate_word_cloud(all_text)