# sentiment-analysis-homework

This project complements a set of provided files to create different models for sentiment analysis. The models are able to predict, based on a text (reviews from [TripAdvisor](https://www.tripadvisor.com/)), whether it has a positive or negative sentiment. In turn, these models are compared and the different variations in the hyper parameters are discussed.

Our team members are:
- Sebastián Galindo 15452
- Jose Antonio Ramirez 15441
- Diego Castañeda 15151


## Installation

It is recommended to use a virtual environment before installing the libraries used in the project. The necessary libraries are found in the requirements.txt file in pip format. To install the libraries, use the following command:

```bash
pip install -r requirements.txt
```


## Usage and Process

prepare_data.ipynb -> tokenize.ipynb ->  train.ipynb 

To get started, we first use the prepare_data.ipynb notebook. The notebook will generate a dictionary containing a list of positive reviews and a list of negative reviews. Reviews contain a rating between 10 - 50 (10, 20, 30, 40, 50), with 10 being terrible and 50 being excellent. A review is assigned to one of the lists based on a rating threshold (first hyperparameter). If the review rating is greater than or equal to the threshold, then it is assigned to the positive sentiment list.

After having divided our reviews into positive and negative, we are going to carry out a pre-processing where we remove stopwords from each of the reviews, add bigrams and lemmatization. This preprocessing is located inside the file tokenize.ipynb

We changed en_core_web_trf pipeline to en_core_web_md, because it is better optimized for CPU.

Most of the changes happened in the train.ipynb file. We start by adding another split function, where we split the reviews into 2, train and test. Next, we perform the predict function that takes the model and evaluates the test data. Finally we evaluate our model with the test data in terms of precision and recall (we also perform a small confusion matrix).


### Models

The main hyperparameters that we use to create different models and be able to compare them are the following:

1. Rating threshold for reviews (hyper_sen_trshld): This parameter tells us the threshold at which we will count a review as positive. It is important to remember that each review is evaluated between the following values (10, 20, 30, 40, 50), with 10 being terrible and 50 being excellent.
2. As a second hyperparameter we use the amount of preprocessing that exists within the reviews. This is if the model has the removal of stopwords, creation of bigrams and/or lemmatization.
3. The third hyperparameter is the min_count in bigram creation. min_count ignore all words and bigrams with total collected count lower than this value.

- #### Model 1

Parameters: 
    hyper_sen_trshld : 50
    stopwords, creation of bigrams and lemmatization
    min_count = 8

Results:

- precision:  0.54
- recall: 0.33
- accuracy:  0.38


- #### Model 2


- #### Model 3



## Team contributions

Our team contributions are divided as follow:

- Diego Castañeda: Responsible for creating the prediction function according to a model.
- Jose Antonio Ramirez: Responsible for the evaluation of the models, creation of metrics and documentation.
- Sebastián Galindo: Responsible for the creation of different models according to different hyper parameters discussed in the group.