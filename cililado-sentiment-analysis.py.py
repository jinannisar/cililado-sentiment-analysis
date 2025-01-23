# -*- coding: utf-8 -*-
"""Copy of DAML_Assn_SA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IRdUkLMExJXhWNEkyO1Wux9AitHCqpXf
"""

import re
import json
import requests
import pandas as pd

url = 'https://shopee.com.my/Cili-Lado-Sambal-Minang-250-Gram-Halal-i.34398605.8433245961'

r = re.search(r'i\.(\d+)\.(\d+)', url)
shop_id, item_id = r[1], r[2]
ratings_url = 'https://shopee.co.id/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit=20&offset={offset}&shopid={shop_id}&type=0'

offset = 0
reviews_data = []

while True:
    data = requests.get(ratings_url.format(shop_id=shop_id, item_id=item_id, offset=offset)).json()

    for rating in data['data']['ratings']:
        author_username = rating['author_username'] # extract username
        comment = rating['comment'] # extract comment if written, otherwise null
        rating_star = rating['rating_star']  # Extract rating
        rating_date = rating['ctime']  # Extract date
        reviews_data.append({'Author Username': author_username, 'Comment': comment, 'Rating': rating_star, 'Date': rating_date})

    if len(data['data']['ratings']) < 20:
        break

    offset += 20

# create a dataframe from the collected data
df = pd.DataFrame(reviews_data)

# save the dataframe as a csv file
df.to_csv('shopee_reviews.csv', index=False)

import pandas as pd
import numpy as np

#import translated data
df2 = pd.read_excel('cililado_reviews.xlsx')
df2.head(5)

# check the shape of the dataframe
df2.shape

# check the summary of the dataframe
df2.info()

# check the columns with object data type
text_columns = df2.select_dtypes(include=['object'])
text_columns.describe()

# checking the properties of numerical data
df2.describe()

# dropping the user and date columns. they are not needed for our purpose
df2 = df2.drop(['user'], axis = 1)
df2.info()

# convert 'date' column to pandas datetime format
df2['date'] = pd.to_datetime(df2['date'], unit='s')
# change the format to 'YYYY-MM-DD HH:MM:SS'
df2['date'] = df2['date'].dt.strftime('%m/%d/%Y %H:%M:%S')
# convert it back to datetime
df2['date'] = pd.to_datetime(df2['date'])

# checking the data type
df2.info()

# find how many null values are there
df2.isna().sum()

# instead of null, it's replaced with an empty string instead
df2['review'].fillna('', inplace=True)

# rechecking the number of null values per column
df2.isna().sum()

# checking if all is correct
print(df2.info())
print(df2.head(5))

import nltk
import glob
import os
import pandas as pd
import seaborn as sns
from textblob import TextBlob
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
from nltk.tokenize import word_tokenize

import matplotlib.pyplot as plt

import re
import string

# a function to clean the comments
def clean_text(sentence):
    # convert sentence to lowercase
    sentence = sentence.lower()

    # remove url from sentence
    pattern = re.compile('https?://\S+')
    sentence = pattern.sub('', sentence)

    # remove social media handles
    sentence = re.sub(r'(^|\s)@(\w+)', '', sentence)

    # Replace colons ':' with spaces
    sentence = sentence.replace(":", " ")

    # remove emojis via Unicode patterns
    emo = re.compile("["
        u"\U0001F600-\U0001FFFF"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    sentence = emo.sub(r'', sentence)

    sentence = sentence.lower()

    # remove special characters and punctution
    sentence = re.sub(r"[,.\"\'!@#$%^&*(){}?/;`~:<>+=-]", "", sentence)
    # replace any inline character with space
    sentence = sentence.replace("\n", " ")

    # tokenize each sentence
    tokens = word_tokenize(sentence)

    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    # keep only alphabetical words
    words = [word for word in stripped if word.isalpha()]

    return " ".join(words)

# applying clean_text function to all reviews from the dataset
df2['cleaned_comments'] = df2['review'].apply(lambda x: clean_text(x))

# applying TextBlob to all cleaned reviews
df2['review_sentiment'] = df2['cleaned_comments'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
df2['review_sentiment']

# checking the top 5 rows
df2.head(5)

import matplotlib.pyplot as plt

# define the sentiment categories based on thresholds
def categorize_sentiment(score):
    if score < 0:
        return "Negative"
    elif score == 0:
      return "Neutral"
    elif score > 0 and score < 0.5:
        return "Positive"
    elif score >= 0.5:
        return "Very Positive"

# apply sentiment categorization from the review sentiment into a new column
df2['sentiment_category'] = df2['review_sentiment'].apply(categorize_sentiment)
df2

# separate reviews into categories based on the sentiment_category column
commented_df = df2[df2['cleaned_comments'] != '']

negative_reviews = commented_df[commented_df['sentiment_category'] == 'Negative']['review_sentiment']
neutral_reviews = commented_df[commented_df['sentiment_category'] == 'Neutral']['review_sentiment']
positive_reviews = commented_df[commented_df['sentiment_category'] == 'Positive']['review_sentiment']
very_positive_reviews = commented_df[commented_df['sentiment_category'] == 'Very Positive']['review_sentiment']

# create histograms for each review
plt.hist(negative_reviews, bins=20, alpha=0.5, color='red', label='Negative Sentiment')
plt.hist(neutral_reviews, bins=20, alpha=0.5, color='yellow', label='Neautral Sentiment')
plt.hist(positive_reviews, bins=20, alpha=0.5, color='green', label='Positive Sentiment')
plt.hist(very_positive_reviews, bins=20, alpha=0.5, color='blue', label='Very Positive Sentiment')

# add labels and legend
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.title('Sentiment Analysis of Reviews (TextBlob)')
plt.legend()
plt.show()

# separate reviews into categories based on the sentiment_category column
commented_df = df2[df2['cleaned_comments'] != '']

negative_reviews = commented_df[commented_df['sentiment_category'] == 'Negative']['review_sentiment']
neutral_reviews = commented_df[commented_df['sentiment_category'] == 'Neutral']['review_sentiment']
positive_reviews = commented_df[commented_df['sentiment_category'] == 'Positive']['review_sentiment']
very_positive_reviews = commented_df[commented_df['sentiment_category'] == 'Very Positive']['review_sentiment']

# count the frequencies of each sentiment category
negative_freq = negative_reviews.value_counts()
neutral_freq = neutral_reviews.value_counts()
positive_freq = positive_reviews.value_counts()
very_positive_freq = very_positive_reviews.value_counts()

# create a new dataframe for easy plotting
data = pd.DataFrame({
    'Sentiment Category': ['Negative', 'Neutral', 'Positive', 'Very Positive'],
    'Frequency': [negative_freq.sum(), neutral_freq.sum(), positive_freq.sum(), very_positive_freq.sum()]
})

# create a gradient from red to green
colors = sns.color_palette("RdYlGn", len(data))

# create a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Sentiment Category', y='Frequency', data=data, palette=colors)

# add labels and title
plt.xlabel('Sentiment Category')
plt.ylabel('Frequency')
plt.title('Sentiment Analysis of Reviews (TextBlob)')
plt.show()

# install vader
!pip install vaderSentiment

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# initialize the vader sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# create an empty list to store sentiment scores
sentiment_scores = []

df3 = df2.copy()

# iterate over each comment in the 'Comment' column
for comment in df3['cleaned_comments']:
    # analyze the sentiment through vader
    sentiment_score = analyzer.polarity_scores(comment)

    # extract the compound sentiment score, which represents overall sentiment
    compound_score = sentiment_score['compound']

    # append the sentiment score to the list
    sentiment_scores.append(compound_score)

# store the sentiment scores back into the dataframe on a new column
df3['review_sentiment'] = sentiment_scores

# check the top 5 rows to check
df3.head(5)

# filter to get only the negative sentiments and print them
negative_sentiments = df3[df3['review_sentiment'] < -0.5]
print(negative_sentiments)

# filter to get only the very positive sentiments and print them
positive_sentiments = df3[df3['review_sentiment'] > 0.5]
print(positive_sentiments)

# apply sentiment categorization to the 'review_sentiment' column
df3['sentiment_category'] = df3['review_sentiment'].apply(categorize_sentiment)

# separate reviews into categories
commented_df2 = df3[df3['cleaned_comments'] != '']

negative_reviews = commented_df2[commented_df2['sentiment_category'] == 'Negative']['review_sentiment']
neutral_reviews = commented_df2[commented_df2['sentiment_category'] == 'Neutral']['review_sentiment']
positive_reviews = commented_df2[commented_df2['sentiment_category'] == 'Positive']['review_sentiment']
very_positive_reviews = commented_df2[commented_df2['sentiment_category'] == 'Very Positive']['review_sentiment']

# create histograms of each reviews category
plt.hist(negative_reviews, bins=20, alpha=0.5, color='red', label='Negative Sentiment')
plt.hist(neutral_reviews, bins=20, alpha=0.5, color='yellow', label='Neautral Sentiment')
plt.hist(positive_reviews, bins=20, alpha=0.5, color='green', label='Positive Sentiment')
plt.hist(very_positive_reviews, bins=20, alpha=0.5, color='blue', label='Very Positive Sentiment')

# add labels and legend
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.title('Sentiment Analysis of Reviews (VADER)')
plt.legend()
plt.show()

# separate reviews into categories
commented_df2 = df3[df3['cleaned_comments'] != '']

negative_reviews = commented_df2[commented_df2['sentiment_category'] == 'Negative']['review_sentiment']
neutral_reviews = commented_df2[commented_df2['sentiment_category'] == 'Neutral']['review_sentiment']
positive_reviews = commented_df2[commented_df2['sentiment_category'] == 'Positive']['review_sentiment']
very_positive_reviews = commented_df2[commented_df2['sentiment_category'] == 'Very Positive']['review_sentiment']

# count the frequencies of each sentiment category
negative_freq = negative_reviews.value_counts()
neutral_freq = neutral_reviews.value_counts()
positive_freq = positive_reviews.value_counts()
very_positive_freq = very_positive_reviews.value_counts()

# create a new dataframe for ease of use
data = pd.DataFrame({
    'Sentiment Category': ['Negative', 'Neutral', 'Positive', 'Very Positive'],
    'Frequency': [negative_freq.sum(), neutral_freq.sum(), positive_freq.sum(), very_positive_freq.sum()]
})

# create a gradient from red to green
colors = sns.color_palette("RdYlGn", len(data))

# create a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Sentiment Category', y='Frequency', data=data, palette=colors)

# add labels and title
plt.xlabel('Sentiment Category')
plt.ylabel('Frequency')
plt.title('Sentiment Analysis of Reviews (VADER)')
plt.show()

# separate reviews into categories for the textblob approach
commented_df1 = df2[df2['cleaned_comments'] != '']
negative_reviews1 = commented_df1[commented_df1['sentiment_category'] == 'Negative']['review_sentiment']
neutral_reviews1 = commented_df1[commented_df1['sentiment_category'] == 'Neutral']['review_sentiment']
positive_reviews1 = commented_df1[commented_df1['sentiment_category'] == 'Positive']['review_sentiment']
very_positive_reviews1 = commented_df1[commented_df1['sentiment_category'] == 'Very Positive']['review_sentiment']

# count the frequencies of each sentiment category
negative_freq1 = negative_reviews1.value_counts()
neutral_freq1 = neutral_reviews1.value_counts()
positive_freq1 = positive_reviews1.value_counts()
very_positive_freq1 = very_positive_reviews1.value_counts()

# Separate reviews into categories for the vader approach
commented_df2 = df3[df3['cleaned_comments'] != '']
negative_reviews2 = commented_df2[commented_df2['sentiment_category'] == 'Negative']['review_sentiment']
neutral_reviews2 = commented_df2[commented_df2['sentiment_category'] == 'Neutral']['review_sentiment']
positive_reviews2 = commented_df2[commented_df2['sentiment_category'] == 'Positive']['review_sentiment']
very_positive_reviews2 = commented_df2[commented_df2['sentiment_category'] == 'Very Positive']['review_sentiment']

# count the frequencies of each sentiment category
negative_freq2 = negative_reviews2.value_counts()
neutral_freq2 = neutral_reviews2.value_counts()
positive_freq2 = positive_reviews2.value_counts()
very_positive_freq2 = very_positive_reviews2.value_counts()

# create new dataframes for each approach for ease of use
data1 = pd.DataFrame({
    'Sentiment Category': ['Negative', 'Neutral', 'Positive', 'Very Positive'],
    'Frequency': [negative_freq1.sum(), neutral_freq1.sum(), positive_freq1.sum(), very_positive_freq1.sum()],
    'Approach': ['TextBlob'] * 4
})

data2 = pd.DataFrame({
    'Sentiment Category': ['Negative', 'Neutral', 'Positive', 'Very Positive'],
    'Frequency': [negative_freq2.sum(), neutral_freq2.sum(), positive_freq2.sum(), very_positive_freq2.sum()],
    'Approach': ['VADER'] * 4
})

# concatenate the two dataframes
combined_data = pd.concat([data1, data2])

# create a custom color palette for the gradient (red to green) FAILED
colors_gradient = sns.color_palette("RdYlGn", n_colors=len(data1['Sentiment Category'])) # failed process. It instead seem to only apply on each grouped bar plot

# create a grouped bar plot
plt.figure(figsize=(12, 6))
sns.barplot(x='Sentiment Category', y='Frequency', hue='Approach', data=combined_data, palette=colors_gradient)

# add labels and title
plt.xlabel('Sentiment Category')
plt.ylabel('Frequency')
plt.title('Comparison of Sentiment Analysis Approaches')
plt.show()

import nltk
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# copy the dataframe into another
df4 = df2[df2['cleaned_comments'] != ''].reset_index(drop=True)

# initialize a counter for positive and negative reviews
positive_word_frequency_counter = Counter()
negative_word_frequency_counter = Counter()

for i in range(len(df4['cleaned_comments'])):
    text = df4['cleaned_comments'][i]
    sentiment = df4['review_sentiment'][i]

    # skip short phrases
    if len(nltk.word_tokenize(text)) < 3:
        continue

    # tokenize the cleaned comment into words
    nltk_tokens = nltk.word_tokenize(text)

    # create bigrams from the words
    bigrams_list = list(nltk.bigrams(nltk_tokens))

    # convert bigrams into a list
    dictionary2 = [' '.join(tup) for tup in bigrams_list]

    # check if dictionary2 is not empty
    if dictionary2:
        try:
            # using CountVectorizer to create a bag-of-words representation for bigrams
            vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words='english')
            bag_of_words = vectorizer.fit_transform(dictionary2)
            words_freq = list(zip(vectorizer.get_feature_names_out(), bag_of_words.sum(axis=0).tolist()[0]))

            # update the word frequency counters based on sentiment labels
            if sentiment > 0:
                positive_word_frequency_counter.update(dict(words_freq))
            elif sentiment < 0:
                negative_word_frequency_counter.update(dict(words_freq))

        except ValueError as e:
            # handle exceptions if something happened
            print(f"Error for sentence: {text}")
            print(e)
    else:
        # print error message if no words are found
        print("No bigrams found for sentence: ", text)

# define unrelated bigrams to exclude from the negative word cloud.
exclude_bigrams = {'sambal minang', 'buy sambal', 'afiq haris', 'arrived safely', 'chicken feet', 'bottle arrived',
                   'bubble wrapglass', 'licking toes', 'quality looks', 'taste licking', 'safely tqsm', 'feet packing',
                   'haris waladofinally', 'looks neat', 'seller afiq', 'neat taste', 'toes chicken', 'tqsm seller',
                   'wrapglass bottle', 'diskqun kot', 'buy tp', 'waladofinally got', 'giler murahbsambal', 'fish giler',
                   'fried luck', 'kot pay', 'murahbsambal diskqun', 'luck plus', 'plus toman', 'toman fish', 'tp live',
                   'younger sister', 'sister going', 'chili pepper', 'minang heard', 'just opened', 'pepper hope',
                   'delivery just'}

# remove specified bigrams from negative_word_frequency_counter
for bigram in exclude_bigrams:
    if bigram in negative_word_frequency_counter:
        del negative_word_frequency_counter[bigram]

# plot the positive word cloud with custom stop words
wordcloud_positive = WordCloud(width=800, height=400, background_color='white', collocation_threshold=5)
wordcloud_positive.generate_from_frequencies(positive_word_frequency_counter)

plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_positive, interpolation='bilinear')
plt.title("Positive Word Cloud (TextBlob)")
plt.axis('off')
plt.show()

# plot the negative word cloud with custom stop words
wordcloud_negative = WordCloud(width=800, height=400, background_color='white', collocation_threshold=3)
wordcloud_negative.generate_from_frequencies(negative_word_frequency_counter)

plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.title("Negative Word Cloud (TextBlob)")
plt.axis('off')
plt.show()

# print the top 10 words for positive and negative word clouds
print("Top 10 Words for Positive Word Cloud:")
print(positive_word_frequency_counter.most_common(10))

print("\nTop 10 Words for Negative Word Cloud:")
print(negative_word_frequency_counter.most_common(10))

# extract the top bigrams and their frequencies for positive sentiment
top_positive_bigrams = positive_word_frequency_counter.most_common(10)
top_positive_bigram_words, top_positive_frequencies = zip(*top_positive_bigrams)

# extract the top bigrams and their frequencies for negative sentiment
top_negative_bigrams = negative_word_frequency_counter.most_common(10)
top_negative_bigram_words, top_negative_frequencies = zip(*top_negative_bigrams)

# convert frequencies to integers
top_positive_frequencies = [int(freq) for freq in top_positive_frequencies]
top_negative_frequencies = [int(freq) for freq in top_negative_frequencies]

# create a new dataframe for the positive bigrams
positive_df = pd.DataFrame({'Bigrams': top_positive_bigram_words, 'Frequency': top_positive_frequencies})

# create a bar plot for top bigrams in positive sentiment
plt.figure(figsize=(12, 6))
sns.barplot(data=positive_df, x='Bigrams', y='Frequency', palette='viridis')
plt.xlabel('Bigrams')
plt.ylabel('Frequency')
plt.title('Top 10 Bigrams for Positive Sentiment (TextBlob)')
plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for better readability
plt.show()

# create a new dataframe for the negative bigrams
negative_df = pd.DataFrame({'Bigrams': top_negative_bigram_words, 'Frequency': top_negative_frequencies})

# create a bar plot for top bigrams in negative sentiment
plt.figure(figsize=(12, 6))
sns.barplot(data=negative_df, x='Bigrams', y='Frequency', palette='magma')
plt.xlabel('Bigrams')
plt.ylabel('Frequency')
plt.title('Top 10 Bigrams for Negative Sentiment (TextBlob)')
plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for better readability
plt.show()

# copy df3 into another dataframe
df4 = df3[df3['cleaned_comments'] != ''].reset_index(drop=True)

# initialize a Counter for positive and negative reviews
positive_word_frequency_counter = Counter()
negative_word_frequency_counter = Counter()

for i in range(len(df4['cleaned_comments'])):
    text = df4['cleaned_comments'][i]
    sentiment = df4['review_sentiment'][i]

    # skip short phrases
    if len(nltk.word_tokenize(text)) < 3:
        continue

    # tokenize the cleaned comment into words
    nltk_tokens = nltk.word_tokenize(text)

    # create bigrams from the words
    bigrams_list = list(nltk.bigrams(nltk_tokens))

    # convert bigrams into a list
    dictionary2 = [' '.join(tup) for tup in bigrams_list]

    # check if dictionary2 is not empty
    if dictionary2:
        try:
            # using CountVectorizer to create a bag-of-words representation for bigrams
            vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words='english')
            bag_of_words = vectorizer.fit_transform(dictionary2)
            words_freq = list(zip(vectorizer.get_feature_names_out(), bag_of_words.sum(axis=0).tolist()[0]))

            # update the word frequency counters based on sentiment labels
            if sentiment > 0:
                positive_word_frequency_counter.update(dict(words_freq))
            elif sentiment < 0:
                negative_word_frequency_counter.update(dict(words_freq))

        except ValueError as e:
            # handle exceptions if something happened
            print(f"Error for sentence: {text}")
            print(e)
    else:
        # print error message if no words are found
        print("No bigrams found for sentence: ", text)

# define unrelated bigrams to exclude from the negative word cloud
exclude_bigrams = {'im sorry', 'dont think', 'parcel today', 'click received', 'just click', 'just opened'}

# remove specified bigrams from negative_word_frequency_counter
for bigram in exclude_bigrams:
    if bigram in negative_word_frequency_counter:
        del negative_word_frequency_counter[bigram]

# plot the positive word cloud with custom stop words
wordcloud_positive = WordCloud(width=800, height=400, background_color='white', collocation_threshold=5)
wordcloud_positive.generate_from_frequencies(positive_word_frequency_counter)

plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_positive, interpolation='bilinear')
plt.title("Positive Word Cloud (VADER)")
plt.axis('off')
plt.show()

# plot the negative word cloud with custom stop words
wordcloud_negative = WordCloud(width=800, height=400, background_color='white', collocation_threshold=5)
wordcloud_negative.generate_from_frequencies(negative_word_frequency_counter)

plt.figure(figsize=(8, 4))
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.title("Negative Word Cloud (VADER)")
plt.axis('off')
plt.show()

# print the top 10 words for positive and negative word clouds
print("Top 10 Words for Positive Word Cloud:")
print(positive_word_frequency_counter.most_common(10))

print("\nTop 10 Words for Negative Word Cloud:")
print(negative_word_frequency_counter.most_common(10))

# extract the top bigrams and their frequencies for positive sentiment
top_positive_bigrams = positive_word_frequency_counter.most_common(10)
top_positive_bigram_words, top_positive_frequencies = zip(*top_positive_bigrams)

# extract the top bigrams and their frequencies for negative sentiment
top_negative_bigrams = negative_word_frequency_counter.most_common(10)
top_negative_bigram_words, top_negative_frequencies = zip(*top_negative_bigrams)

# convert frequencies to integers
top_positive_frequencies = [int(freq) for freq in top_positive_frequencies]
top_negative_frequencies = [int(freq) for freq in top_negative_frequencies]

# create a new dataframe for the positive bigrams
positive_df = pd.DataFrame({'Bigrams': top_positive_bigram_words, 'Frequency': top_positive_frequencies})

# create a bar plot for top bigrams in positive sentiment
plt.figure(figsize=(12, 6))
sns.barplot(data=positive_df, x='Bigrams', y='Frequency', palette='viridis')
plt.xlabel('Bigrams')
plt.ylabel('Frequency')
plt.title('Top 10 Bigrams for Positive Sentiment (TextBlob)')
plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for better readability
plt.show()

# create a new dataframe for the negative bigrams
negative_df = pd.DataFrame({'Bigrams': top_negative_bigram_words, 'Frequency': top_negative_frequencies})

# create a bar plot for top bigrams in negative sentiment
plt.figure(figsize=(12, 6))
sns.barplot(data=negative_df, x='Bigrams', y='Frequency', palette='magma')
plt.xlabel('Bigrams')
plt.ylabel('Frequency')
plt.title('Top 10 Bigrams for Negative Sentiment (TextBlob)')
plt.xticks(rotation=45, ha='right')  # rotate x-axis labels for better readability
plt.show()

# copy the reviews into another variable
reviews = df2['cleaned_comments'].str.cat(sep=' ')

# excluded words from the wordcloud. Doesn't work that well
excluded_words = {'sambal', 'a', 'it', 'a little', 'it can', 'want', 'the green', 'in the', 'to buy'}

# create a word cloud for the postive reviews
wordcloud_reviews = WordCloud(width=1000, height=500,
background_color='white', collocation_threshold=3, stopwords=excluded_words).generate(reviews)
plt.imshow(wordcloud_reviews, interpolation='bilinear')
plt.title("Postive Word Cloud Reviews (TextBlob)")
plt.axis('off')
plt.show()

# create a word cloud for the negative reviews
negative_reviews = df2[df2['review_sentiment'] < 0]['cleaned_comments'].str.cat(sep=' ')
wordcloud_negative = WordCloud(width=1000, height=500, background_color='white', collocation_threshold=3, stopwords=excluded_words).generate(negative_reviews)
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.title("Negative Word Cloud Reviews (TextBlob)")
plt.axis('off')
plt.show()

#maybe separate word clouds on the basis of positive and negative reviews
#the words are not clear compared to bigrams

# extracting word frequencies from the word cloud
positve_word_frequencies = wordcloud_reviews.words_
negative_word_frequencies = wordcloud_negative.words_

# get the top 10 words for positive and negative
top_10_positive_words = list(positve_word_frequencies.keys())[:10]
top_10_negative_words = list(negative_word_frequencies.keys())[:10]

# print the top 10 words for positive and negative
print("Top 10 Words for Postive:")
print(top_10_positive_words)
print("\nTop 10 Words for Negative:")
print(top_10_negative_words)

# copy the reviews into another variable
reviews = df3['cleaned_comments'].str.cat(sep=' ')

# exclude words from the wordcloud. Doesn't work that well
excluded_phrases = {'sambal', 'a', 'it', 'a little', 'it can', 'want', 'the green', 'in the', 'to buy','i didnt', 'didnt have', 'have time', 'time to', 'i dont', 'because i'}

# Remove excluded phrases from the reviews
for phrase in excluded_phrases:
    reviews = reviews.replace(phrase, '')

# create a positive word cloud review
wordcloud_reviews = WordCloud(width=800, height=400,
background_color='white', collocation_threshold=3, stopwords=excluded_words).generate(reviews)
plt.imshow(wordcloud_reviews, interpolation='bilinear')
plt.title("Postive Word Cloud Reviews (VADER)")
plt.axis('off')
plt.show()


# create a negative word cloud review
negative_reviews = df3[df3['review_sentiment'] < 0]['cleaned_comments'].str.cat(sep=' ')
# for phrase in excluded_phrases:
#     negative_reviews = reviews.replace(phrase, '')
wordcloud_negative = WordCloud(width=800, height=400, background_color='white', collocation_threshold=3, stopwords=excluded_words).generate(negative_reviews)
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.title("Negative Word Cloud Reviews (VADER)")
plt.axis('off')
plt.show()

#maybe separate word clouds on the basis of positive and negative reviews
#the negative seems to be mixing with some positive words

# extracting word frequencies from the word cloud
positve_word_frequencies = wordcloud_reviews.words_
negative_word_frequencies = wordcloud_negative.words_

# get the top 10 words for positive and negative
top_10_positive_words = list(positve_word_frequencies.keys())[:10]
top_10_negative_words = list(negative_word_frequencies.keys())[:10]

# print the top 10 words for positive and negative
print("Top 10 Words for Postive:")
print(top_10_positive_words)
print("\nTop 10 Words for Negative:")
print(top_10_negative_words)

import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import string
from nltk import word_tokenize, pos_tag
import scipy
from gensim import matutils
from gensim import models
import pickle
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer

from nltk import word_tokenize, pos_tag
def nouns_adj(text):
    # only extract the nouns and adjectives by tokenizing a string of text
    is_noun_adj = lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ'
    tokenized = word_tokenize(text)
    nouns_adj = [word for (word, pos) in pos_tag(tokenized) if   is_noun_adj(pos)]
    return ' '.join(nouns_adj)

# get the nouns and adjectives from the cleaned dataframe
data_nouns_adj = pd.DataFrame(df2['cleaned_comments'].apply(nouns_adj))
print(data_nouns_adj)

from sklearn.feature_extraction.text import CountVectorizer

# re-add the additional stop words since we are recreating the document-term matrix
add_stop_words = ['like', 'im', 'know', 'just', 'dont', 'thats', 'right', 'people', 'youre', 'got', 'gonna', 'time', 'think', 'yeah', 'said']
stop_words = list(text.ENGLISH_STOP_WORDS.union(add_stop_words))

# recreate a document-term matrix with only nouns
cvn = CountVectorizer(stop_words=stop_words)
data_cvn = cvn.fit_transform(data_nouns_adj['cleaned_comments'])
data_dtmn = pd.DataFrame(data_cvn.toarray(), columns=cvn.get_feature_names_out())
data_dtmn.index = data_nouns_adj.index
data_dtmn

from gensim import corpora

# converts a sparse matrix into a gensim corpus
corpusn = matutils.Sparse2Corpus(scipy.sparse.csr_matrix(data_dtmn.transpose()))
# create the vocabulary dictionary
id2wordn = corpora.Dictionary.from_corpus(corpusn, id2word = dict((v, k) for k, v in cvn.vocabulary_.items()))

from gensim import corpora
from gensim.matutils import Sparse2Corpus

# Convert sparse matrix to a list of tokenized documents
tokenized_docs = data_nouns_adj['cleaned_comments'].apply(lambda x: x.split())

# Create Dictionary
id2word = corpora.Dictionary(tokenized_docs)

# Create Corpus: Term Document Frequency
corpus = [id2word.doc2bow(text) for text in tokenized_docs]

from gensim.models import LdaModel

# specify the number of topics
num_topics = 4

# build the LDA model
lda_model = LdaModel(corpus, num_topics=4, id2word=id2word, passes=10, random_state=42)

# print the topics and their top words
topics = lda_model.print_topics(num_words=5)
for topic in topics:
    print(topic)

# installing pyLDAvis since it's not natively installed to google collab
!pip install pyLDAvis

# downgrading pandas is required for it to work with pyLDAvis
!pip install pandas==1.5.3

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import pandas as pd

# visualize the topics
pyLDAvis.enable_notebook()
vis = gensimvis.prepare(lda_model, corpus, dictionary=lda_model.id2word)
pyLDAvis.save_html(vis, 'lda_visualization.html') # save the model as a HTML file
vis

topics_list = []

# iterate to find the topics and their top words
for i, topic in enumerate(lda_model.print_topics()):
    topic_words = [word.split('*')[1].strip().strip('"') for word in topic[1].split('+')]
    topics_list.append(topic_words)

# print the topic list and their top words
print(topics_list)

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# generate and display a word cloud for a given topic
def generate_word_cloud(ax, topic_words, topic_number):
    wordcloud = WordCloud(width=400, height=200, background_color='white').generate(' '.join(topic_words))

    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_title(f'Topic {topic_number}')
    ax.axis('off')

# create a 2x2 subplot grid
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# generate word clouds for the top 4 topics
for i, ax in enumerate(axs.flat):
    if i < len(topics_list):
        generate_word_cloud(ax, topics_list[i], i+1)

plt.tight_layout()
plt.show()

# map sentiment scores to a rating
def map_to_rating(sentiment_score, actual_rating, comment):
    if comment == '' or comment is None:
        return actual_rating
    elif sentiment_score < 0:
        return 1
    elif sentiment_score == 0:
        return 2
    elif 0 < sentiment_score < 0.3:
        return 3
    elif 0.3 <= sentiment_score < 0.5:
        return 4
    elif sentiment_score >= 0.5:
        return 5

# apply the mapping function to create a new column 'Mapped_Rating'
df2['Mapped_Rating'] = df2.apply(lambda row: map_to_rating(row['review_sentiment'], row['rating'], row['cleaned_comments']), axis=1)

# comparing the rating between the actual and mapped rating
print('Actual Rating:')
print(df2['rating'].value_counts())
print('Mapped Rating:')
print(df2['Mapped_Rating'].value_counts())

# create a new dataframe for easy plotting. Manually created from the .value_counts() method.
data = pd.DataFrame({
    'Rating': [1, 2, 3, 4, 5],
    'Sentiment Frequency': [23, 25, 133, 103, 579],
    'Actual Frequency': [4, 7, 24, 30, 798]
})

# set up the matplotlib figure
fig, ax = plt.subplots(figsize=(12, 8))

# define the bar width
bar_width = 0.35

# create the bar positions
bar_positions_sentiment = np.arange(len(data['Rating']))
bar_positions_actual = bar_positions_sentiment + bar_width + 0.04

# define the colors and edgecolors
color_sentiment = '#6dbefc'
color_actual = '#6cc47c'
edgecolor_sentiment = '#3a7ca6'  # Darker version of color_sentiment
edgecolor_actual = '#367a52'  # Darker version of color_actual

# create grouped bar plot using matplotlib
ax.bar(bar_positions_sentiment, data['Sentiment Frequency'], color=color_sentiment, edgecolor=edgecolor_sentiment, label='Sentiment Analysis Mapped Ratings', width=bar_width)
ax.bar(bar_positions_actual, data['Actual Frequency'], color=color_actual, edgecolor=edgecolor_actual, label='Actual Ratings', width=bar_width)

# add labels and title
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Comparison of Sentiment Analysis Mapped Ratings with Actual Ratings (TextBlob)')
plt.legend() # add legend
ax.set_xticks((bar_positions_sentiment + bar_positions_actual) / 2) # set x-axis ticks and labels
ax.set_xticklabels(data['Rating'])
plt.show()

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# define the ratings and their corresponding frequencies based on .value_counts().
ratings = ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']
mapped_rating_freq = [23, 25, 133, 103, 579]
actual_rating_freq = [4, 7, 24, 30, 798]

# set up the matplotlib figure for Mapped Ratings
fig1, ax1 = plt.subplots(figsize=(6, 6))
wedges1, texts1 = ax1.pie(mapped_rating_freq, labels=ratings, startangle=90, colors=plt.cm.Paired.colors)
legend1 = ax1.legend(wedges1, ratings, title='Mapped Ratings (TextBlob)', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
ax1.set_title('Mapped Ratings')

# show the plot for Mapped Ratings
plt.show()

# set up the matplotlib figure for Actual Ratings
fig2, ax2 = plt.subplots(figsize=(6, 6))
wedges2, texts2 = ax2.pie(actual_rating_freq, labels=ratings, startangle=90, colors=plt.cm.Paired.colors)
legend2 = ax2.legend(wedges2, ratings, title='Actual Ratings', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
ax2.set_title('Actual Ratings')

# show the plot for Actual Ratings
plt.show()

# apply the mapping function to create a new column 'Mapped_Rating'
df3['Mapped_Rating'] = df3.apply(lambda row: map_to_rating(row['review_sentiment'], row['rating'], row['cleaned_comments']), axis=1)

# comparing between the actual and mapped rating
print('Actual Rating:')
print(df3['rating'].value_counts())
print('Mapped Rating')
print(df3['Mapped_Rating'].value_counts())

# define the ratings and their corresponding frequencies manually
ratings = np.array([1, 2, 3, 4, 5])
mapped_rating_freq = np.array([17, 36, 30, 58, 722])
actual_rating_freq = np.array([4, 7, 24, 30, 798])

# set up the matplotlib figure
fig, ax = plt.subplots(figsize=(12, 8))

# define the bar width
bar_width = 0.35

# create the bar positions
bar_positions_mapped = np.arange(len(ratings))
bar_positions_actual = bar_positions_mapped + bar_width + 0.04

# define the colors and edgecolors
color_mapped = '#6dbefc'
color_actual = '#6cc47c'
edgecolor_mapped = '#3a7ca6'  # Darker version of color_mapped
edgecolor_actual = '#367a52'  # Darker version of color_actual

# create grouped bar plot using matplotlib
ax.bar(bar_positions_mapped, mapped_rating_freq, color=color_mapped, edgecolor=edgecolor_mapped, label='Mapped Ratings (VADER)', width=bar_width)
ax.bar(bar_positions_actual, actual_rating_freq, color=color_actual, edgecolor=edgecolor_actual, label='Actual Ratings', width=bar_width)

# add labels and title
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Comparison of Mapped Ratings with Actual Ratings (VADER)')
plt.legend() # add legend
ax.set_xticks((bar_positions_mapped + bar_positions_actual) / 2) # set x-axis ticks and labels
ax.set_xticklabels(ratings)
plt.show()

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# define the ratings and their corresponding frequencies manually
ratings = ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']
mapped_rating_freq = [17, 36, 30, 58, 722]
actual_rating_freq = [4, 7, 24, 30, 798]

# set up the matplotlib figure for Mapped Ratings
fig1, ax1 = plt.subplots(figsize=(6, 6))
wedges1, texts1 = ax1.pie(mapped_rating_freq, labels=ratings, startangle=90, colors=plt.cm.Paired.colors)
legend1 = ax1.legend(wedges1, ratings, title='Mapped Ratings (VADER)', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
ax1.set_title('Mapped Ratings')

# show the plot for Mapped Ratings
plt.show()

# set up the matplotlib figure for Actual Ratings
fig2, ax2 = plt.subplots(figsize=(6, 6))
wedges2, texts2 = ax2.pie(actual_rating_freq, labels=ratings, startangle=90, colors=plt.cm.Paired.colors)
legend2 = ax2.legend(wedges2, ratings, title='Actual Ratings', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
ax2.set_title('Actual Ratings')

# show the plot for Actual Ratings
plt.show()

df2.info()

import pandas as pd
import matplotlib.pyplot as plt

df5 = df2.copy()

# Set the date column as the index
df5.set_index('date', inplace=True)

# Resample the data to a specific frequency (for eg monthly) and count the number of reviews
resampled_data = df5.resample('M').count()

# Plot the time series data
plt.figure(figsize=(12, 6))
plt.plot(resampled_data.index, resampled_data['review'], marker='o')
plt.title('Number of Reviews Over Time')
plt.xlabel('Time')
plt.ylabel('Number of Reviews')
plt.grid(True)
plt.show()