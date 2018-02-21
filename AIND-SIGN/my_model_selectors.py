import math
import statistics
import warnings
import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant
    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components
        

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        bestbic = np.float("inf")
        best_model = None

        for num_states in range(self.min_n_components, self.max_n_components+1):
            try:
                #model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                        #random_state=self.random_state, verbose=False).fit(self.X, self.lengths)

                #model = GaussianHMM(n_components=num_states, n_iter=1000).fit(self.X, self.lengths)
                model = self.base_model(num_states)
                logL = model.score(self.X, self.lengths)
                initialStateProbs = num_states
                transitionProbs = num_states * (num_states - 1)
                emissionProbs = len(np.diagonal(model.means_)) + len(np.diagonal(model.covars_))
                p = initialStateProbs + transitionProbs + emissionProbs
                logN = np.log(len(self.X))
                bic = -2 * logL + p * logN

                if bic < bestbic:
                    bestbic = bic
                    best_num_components = num_states
                    best_model = model
                    #print(best_model)
            except:

                continue

        return best_model



class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        best_n = self.random_state
        best_dic = np.float("-inf")
        best_model = None
        for num_states in range(self.min_n_components, self.max_n_components + 1):
            try:
                #model = GaussianHMM(n_components=num_states, n_iter=1000).fit(self.X, self.lengths)
                model = self.base_model(num_states)
                #model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                       #random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
                current_word_Score = model.score(self.X, self.lengths) # likelihood function or the current word score (logL)

                logL_left_words = 0
                number_of_words = 0
                for word in self.words:
                    if word == self.this_word:
                        number_of_words += 1
                        continue
                    left_x, left_length = self.hwords[word]
                    logl_left = model.score(left_x, left_length)
                    logL_left_words += logl_left

                average_score = logL_left_words/number_of_words - 1
                dic = current_word_Score - average_score

                if dic > best_dic:
                    best_dic = dic
                    best_n = num_states
            except:
                continue
        #best_model = GaussianHMM(best_n, n_iter=1000).fit(self.X, self.lengths)
        best_model = self.base_model(best_n)
        #best_model = GaussianHMM(n_components=best_n, covariance_type="diag", n_iter=1000, random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
        return best_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        folds = 0
        best_cv = np.float("-inf")
        best_model = None
        best_n = self.random_state
        b_model = self.base_model(self.n_constant)
        if len(self.sequences) == 1:
            return b_model
        else:
            split_method = KFold(n_splits=min(len(self.sequences), 3))

        for num_states in range(self.min_n_components, self.max_n_components + 1):
            total_logL = 0
            try:
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                    folds +=1
                    train_X, train_lengths = combine_sequences(cv_train_idx, self.sequences)
                    test_X, test_lengths = combine_sequences(cv_test_idx, self.sequences)
                    model = GaussianHMM(n_components=num_states, n_iter=1000).fit(train_X, train_lengths)
                    #model = self.base_model(num_states)
                    logL = model.score(test_X, test_lengths)
                    total_logL += logL

                average_logL = total_logL / folds

                if average_logL >= best_cv:

                    #print(average_logL)
                    best_cv = average_logL
                    #best_model = model
                    best_n = num_states
                    #print(best_n)

            except:
                continue

            best_model = GaussianHMM(n_components=best_n, n_iter=1000).fit(self.X, self.lengths)
            #best_model = self.base_model(best_n)

        return best_model




