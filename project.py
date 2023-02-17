# import the streamlit library
import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo

st.write("# Twitter Data Scraper")

keyword = st.text_input("Enter the keyword or hashtag to be searched:")
start_date = st.date_input("Enter the start date:")
end_date = st.date_input("Enter the end date:")
tweet_count = st.number_input("Enter the number of tweets to be scraped:", min_value=1, max_value=1000)

# Create a list to store the scraped data
tweets_list = []

# Iterate through the search results and extract the data
tweets_df = pd.DataFrame()
# copy_df=pd.DataFrame()

# Convert the list of dictionaries to a pandas dataframe
def Scraping():
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} since:{start_date} until:{end_date}').get_items()):
        if i >= tweet_count:
            break
        tweet_dict = {
            "date": tweet.date,
            "id": tweet.id,
            "url": tweet.url,
            "content": tweet.content,
            "user": tweet.user.username,
            "reply_count": tweet.replyCount,
            "retweet_count": tweet.retweetCount,
            "language": tweet.lang,
            "source": tweet.sourceLabel,
            "like_count": tweet.likeCount
        }
        global tweets_df
#         global copy_df
        tweets_list.append(tweet_dict)
    tweets_df = tweets_df.append(tweets_list, ignore_index=True)

if st.button("Scrape"):
    Scraping()
    if not tweets_df.empty:
        st.write(tweets_df)

if st.button("Upload to Database"):
    client = pymongo.MongoClient("mongodb+srv://gascitech:gascitech@cluster0.mdoeudq.mongodb.net/?retryWrites=true&w=majority")
    db = client.DB
    collection = db["Web Scraping"]
    Scraping()
    collection.insert_many(tweets_df.to_dict("records"))
    st.write("Data uploaded to database!")

if st.button("Download CSV"):
#     global tweets_df
    print(copy_df)
    Scraping()
    if not tweets_list.empty:
        csv = tweets_list.to_csv(index=False)
        st.download_button("Download CSV", csv, "tweets.csv", "text/csv")

if st.button("Download JSON"):
#     global tweets_df
    print(copy_df)
    Scraping()
    if not tweets_list.empty:
        json = tweets_list.to_json(orient="records")
        st.download_button("Download JSON", json, "tweets.json", "application/json")
