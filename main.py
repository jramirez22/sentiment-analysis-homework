import enum
from typing import Generator, List
import pickle
import json

from gensim.models import Phrases
from gensim.models.phrases import Phraser
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
import spacy
from spacy.lang.en import English

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

nlp = spacy.load('en_core_web_trf')

class Sentiments(enum.Enum):
    POS = 'POS'
    NEG = 'NEG'
    NEU = 'NEU'


def sentences_to_words(sentences: List[str]) -> List[List[str]]:
    words = []
    for sentence in sentences:
        # https://radimrehurek.com/gensim/utils.html#gensim.utils.simple_preprocess
        words.append(simple_preprocess(str(sentence), deacc=True))  # deacc=True elimina la puntuación
    return words

def remove_stopwords(documents: List[List[str]]) -> List[List[str]]:
    return [[word for word in simple_preprocess(str(doc)) if word not in stopwords.words('english')]
            for doc in documents]

def learn_bigrams(documents: List[List[str]], mincount) -> List[List[str]]:
    # We learn bigrams
    #  https://radimrehurek.com/gensim/models/phrases.html#gensim.models.phrases.Phrases
    bigram = Phrases(documents, min_count=mincount, threshold=10)

    # we reduce the bigram model to its minimal functionality
    bigram_mod = Phraser(bigram)

    # we apply the bigram model to our documents
    return bigram_mod

def create_bigrams(bigram_model, documents: List[List[str]]):
    return [bigram_model[doc] for doc in documents]

def lemmatization(nlp: English, texts: List[List[str]], allowed_postags: List = None) -> List[List[str]]:
    if allowed_postags is None:
        allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']

    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


def tokenize(documents: List[str], bigram_model) -> List[List[str]]:

    document_words = sentences_to_words(documents)
    document_words = remove_stopwords(document_words)
    document_words = create_bigrams(bigram_model, document_words)
    document_words = lemmatization(nlp, document_words)
    return document_words

def predict(model, bigram_model, phrase):
    #Limpiar oracion
    doc = [phrase]
    tokenize_phrase = tokenize(doc, bigram_model)
    #prob_neg = model["NEG_PROB"]
    #prob_pos = model["POS_PROB"]
    prob_neg = prob_pos = 0

    positive_words_prob = model["COND_POS_PROBS"]
    positive_words_prob = json.dumps(positive_words_prob)
    positive_words_prob = json.loads(positive_words_prob)

    negative_words_prob = model["COND_NEG_PROBS"]
    negative_words_prob = json.dumps(negative_words_prob)
    negative_words_prob = json.loads(negative_words_prob)

    tokenjuan = 0
    print(tokenize_phrase[0])
    for token in tokenize_phrase[0]:
        print("\nTokenNo: ",tokenjuan)
        tokenjuan+=1
        print("Token", token)
        if token in negative_words_prob:
            prob_neg += negative_words_prob[token]["logprob"]
            print("Negative prod = ", negative_words_prob[token]["logprob"])
        if token in positive_words_prob:
            prob_pos += positive_words_prob[token]["logprob"]
            print("Positive prod = ", positive_words_prob[token]["logprob"])

        print("Positivo", prob_pos)
        print("Negativo", prob_neg)

    if prob_pos > prob_neg:
        return "POS"
    elif prob_neg > prob_pos:
        return "NEG"
    else:
        return "NEU"

# Modelo 1  : Threshold de positivo >40
#            mincount = 5 veces
print("Leyendo Bigram Model 1")
with open(r"./model_1.pkl", "rb") as input_file:
    model1 = pickle.load(input_file)

with open(r"./bigram_model_1.pkl", "rb") as input_file:
    bigram_model_1 = pickle.load(input_file)

sentiment_1 = predict(model1, bigram_model_1, "The hostal is dirty. They don't offer you a towel (oh yeah), the sheets are nasty, the bathroom is gross, there's no hot water and the owner doesn't take dollars and couldn't give me receipt. Terrible")
print(sentiment_1)

#LA FRASE PROHIBIDA
#The hostal is dirty. They don't offer you a towel (oh yeah), the sheets are nasty, the bathroom is gross, there's no hot water and the owner doesn't take dollars and couldn't give me receipt. Terrible

# Modelo 2  : Threshold de Positivo > 30
#           min_count = 10 veces

# Modelo 3  : Threshold de positivo >50
#            no bigramas.
