import warnings
from asl_data import SinglesData
import numpy as np


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer

    for item in test_set.get_all_sequences():
        X, length = test_set.get_item_Xlengths(item)

        words_probability = {}
        best_score = np.float("-inf")
        guess_word = None

        for word, model in models.items():

            try:
                words_probability[word] = model.score(X, length)
                if words_probability[word] > best_score:
                    guess_word = word
                    # print(guess_word)
                    best_score = words_probability[word]
            except:
                words_probability[word] = None
                continue

        probabilities.append(words_probability)
        guesses.append(guess_word)

    return (probabilities, guesses)