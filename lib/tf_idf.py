import os
import re
from pathlib import Path

import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from bs4 import BeautifulSoup

class TF_IDF:

    corpus_file_paths = None
    corpus_base_file_path = None

    maximum_features = 10000
    minimum_document_frequency = 1
    maximum_document_frequency = None
    ngram_range = (1,2)
    stop_words = 'english'
    documents_encoding = 'utf-8'
    documents_in_delimeter = ', '
    sentences_in_delimeter = '\n\n'

    documents_df = None
    sentences_df = None
    term_occurrences_df = None
    term_weights_df = None
    term_frequency_inverse_document_frequency_df = None
    dataframe = None

    def __init__(self,
                 corpus_base_file_path,
                 corpus_file_extenions
                 ):

        self.corpus_base_file_path = corpus_base_file_path

        self.corpus_file_extenions = corpus_file_extenions

        self.set_corpus_file_paths_list()

        self.set_maximum_document_frequency()


    def set_corpus_file_paths_list(self):

        files = os.listdir(self.corpus_base_file_path)

        paths = []

        for file in files:

            if Path(file).suffix in self.corpus_file_extenions:

                paths.append(file)

        self.corpus_file_paths = files

        return files

    def set_maximum_document_frequency(self):

        self.maximum_document_frequency = round(len(self.corpus_file_paths) * .99)

        return self.maximum_document_frequency

    def documents(self):

        documents = []

        for filename in self.corpus_file_paths:

            with open(os.path.join(self.corpus_base_file_path, filename), 'r', encoding=self.documents_encoding) as file:

                soup = BeautifulSoup(file.read())

                documents.append({'source': filename, 'text': soup.get_text()})

        dataframe = pd.DataFrame(documents)

        self.documents_df = dataframe

        return self


    def sentences(self):

        sentences = []

        for filename in self.corpus_file_paths:

            with open(os.path.join(self.corpus_base_file_path, filename), 'r', encoding=self.documents_encoding) as file:

                soup = BeautifulSoup(file.read())

                for i in sent_tokenize(soup.get_text()):

                    sentences.append({'text': i})

        dataframe = pd.DataFrame(sentences)

        self.sentences_df = dataframe

        return self

    def term_occurrences(self):

        count_vectorizer = CountVectorizer(
            min_df=self.minimum_document_frequency,
            max_df=self.maximum_document_frequency,
            stop_words=self.stop_words,
            ngram_range=self.ngram_range
        )

        count_vectorizer.fit(self.sentences_df.text)

        count_vectorizer_occurrences = count_vectorizer.transform(self.sentences_df.text)

        dataframe = pd.DataFrame({'term': count_vectorizer.get_feature_names(), 'occurrences': np.asarray(count_vectorizer_occurrences.sum(axis=0)).ravel().tolist()})
        
        self.term_occurrences_df = dataframe

        return self

    def term_weights(self):

        tfidf_vectorizer = TfidfVectorizer(
            min_df=self.minimum_document_frequency,
            max_df=self.maximum_document_frequency,
            stop_words=self.stop_words,
            ngram_range=self.ngram_range,
            max_features=self.maximum_features
        )

        tfidf_vectorizer_weights = tfidf_vectorizer.fit_transform(self.sentences_df.text.dropna())

        dataframe = pd.DataFrame({'term': tfidf_vectorizer.get_feature_names(), 'weight': np.asarray(tfidf_vectorizer_weights.mean(axis=0)).ravel().tolist()})

        self.term_weights_df = dataframe

        return self

    def term_frequency_inverse_document_frequency(self):

        dataframe = pd.merge(self.term_weights_df, self.term_occurrences_df, how='left', left_on='term', right_on='term')

        self.term_frequency_inverse_document_frequency_df = dataframe

        return self

    def documents_in(self):

        dataframe = self.term_frequency_inverse_document_frequency_df

        dataframe['documents_in'] = dataframe.term.map(lambda x: self.documents_in_delimeter.join(list(self.documents_df.loc[self.documents_df['text'].str.contains(fr'\b{x}\b', flags=re.IGNORECASE, regex=True)]['source'])))

        self.dataframe = dataframe

        return self

    def sentences_in(self):

        dataframe = self.dataframe

        dataframe['sentences_in'] = dataframe.term.map(lambda x: self.sentences_in_delimeter.join(list(self.sentences_df.loc[self.sentences_df['text'].str.contains(fr'\b{x}\b', flags=re.IGNORECASE, regex=True)]['text'])[:4]))

        self.dataframe = dataframe

        return self

    def run(self):

        self.documents()\
            .sentences()\
            .term_occurrences()\
            .term_weights()\
            .term_frequency_inverse_document_frequency()\
            .documents_in()\
            .sentences_in()

        return self
