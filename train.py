"""
Trains and pickles a Positive/Negative text classifier.
"""
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer as wnl
from nltk.corpus import stopwords, wordnet
from nltk.tag import pos_tag
from nltk import classify, NaiveBayesClassifier

from nltk.corpus import twitter_samples

import re, random, pickle

"""
Returns a generator to get all tokens in a list of sentences
"""
def get_all_tokens(sentences):
    for sent in sentences:
        for token in sent:
            yield token

"""
Returns the corresponding wordnet tag for a parts of speach (pos) tag
"""
def get_wordnet_tag(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    
"""
Returns cleaned up sentence (lemmatized, stopwords, special characters, urls, and tweet handles removed)
"""
def cleanup_sentence(tokens, lang='english'):
    lemmatizer = wnl()
    stop_words = stopwords.words(lang)

    result = []
    
    for token, tag in pos_tag(tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        
        
        if token.lower() in stop_words:
            continue
        
        wordnet_pos = get_wordnet_tag(tag)
        result.append(lemmatizer.lemmatize(token, wordnet_pos))
        
    return result

"""
Return dictionary for existing dataset to for model
"""
def sentence_to_dict(dataset):
    for tokens in dataset:
        yield dict([token, True] for token in tokens)


if __name__ == '__main__':
  positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
  negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

  p_cleaned_up_tokens = []
  n_cleaned_up_tokens = []
  for sentence in positive_tweet_tokens:
    p_cleaned_up_tokens.append(cleanup_sentence(sentence))

  for sentence in negative_tweet_tokens:
    n_cleaned_up_tokens.append(cleanup_sentence(sentence))

  p_dataset = []
  n_dataset = []
  for d in sentence_to_dict(p_cleaned_up_tokens):
      p_dataset.append(([d, 1]))
      
  for d in sentence_to_dict(n_cleaned_up_tokens):
      n_dataset.append(([d, 0]))

  dataset = p_dataset + n_dataset
  random.shuffle(dataset)

  train = dataset[:8000] # 80%
  test = dataset[8000:] # 20%

  classifier = NaiveBayesClassifier.train(train)

  print(classify.accuracy(classifier, test))

  pickle.dump(classifier, open('classifier.o', 'wb'))
