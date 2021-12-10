import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier


from nltk.tag import pos_tag
from pymystem3 import Mystem
from nltk.corpus import stopwords


import re, string, random

def lemmatize_sentence(tokens):
    mystem = Mystem()
    lemmatized_sentence = []
    cleaned_tokens=[]
    for word, tag in pos_tag(tokens, lang='rus'):
       lemmatized_sentence.append(mystem.lemmatize(word))
       if word.lower() not in stop_words:
            cleaned_tokens.append(word.lower())
    return cleaned_tokens


def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

if __name__ == "__main__":
    # nltk.download('twitter_samples')
    # nltk.download('punkt')
    # nltk.download('wordnet')
    # nltk.download('averaged_perceptron_tagger')
    # nltk.download('averaged_perceptron_tagger_ru')
    # nltk.download('stopwords')

    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    # stop_words = stopwords.words("russian")
    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))
        # positive_cleaned_tokens_list.append(lemmatize_sentence(tokens))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))
        # negative_cleaned_tokens_list.append(lemmatize_sentence(tokens))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))

    custom_tweets = ["Micelle did her homework this afternoon",
"My uncle was born in 1988",
"The teachers were preparing for the exam next week at the office.",
"My sister had a headache this morning, I hope she will get better soon.",
"Roy would like to go to the store earlier before it starts to rain.",
"Amy is not going to school today.",
"Tom doesn’t like to eat spicy food.",
"They were not playing basketball.",
"Roy would not like to go to the store earlier before it starts to rain.",
"I could not make you some fresh juice."]

    for custom_tweet in custom_tweets:
        custom_tokens = remove_noise(word_tokenize(custom_tweet))

        print(custom_tweet, classifier.classify(dict([token, True] for token in custom_tokens)))
