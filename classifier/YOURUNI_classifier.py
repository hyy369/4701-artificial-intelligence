import sys
import string
import math

"""
Prior to tuning:
train: 99.126%
test: 98.205%
dev: 97.666%

After tuning: (m=2, k=0.01)
train: 99.305%
test: 98.384%
dev: 98.025%
"""

class NbClassifier(object):

    """
    A Naive Bayes classifier object has three parameters, all of which are populated during initialization:
    - a set of all possible attribute types
    - a dictionary of the probabilities P(Y), labels as keys and probabilities as values
    - a dictionary of the probabilities P(F|Y), with (feature, label) pairs as keys and probabilities as values
    """
    def __init__(self, training_filename, stopword_file):
        self.attribute_types = set()
        self.label_prior = {}    
        self.word_given_label = {}   

        self.collect_attribute_types(training_filename)
        if stopword_file is not None:
            self.remove_stopwords(stopword_file)
        self.train(training_filename)


    """
    A helper function to transform a string into a list of word strings.
    You should not need to modify this unless you want to improve your classifier in the extra credit portion.
    """
    def extract_words(self, text):
        no_punct_text = "".join([x for x in text.lower() if not x in string.punctuation])

        result = []
        for word in no_punct_text.split():
            # Replace numbers with "123"
            if self.is_number(word):
                word = "123"
            result.append(word)
        return result
    
    # test if a string is all digits
    def is_number(self, string):
        num = {0,1,2,3,4,5,6,7,8,9}
        for char in string:
            if not char in num:
                return False
        return True


    """
    Given a stopword_file, read in all stop words and remove them from self.attribute_types
    Implement this for extra credit.
    """
    def remove_stopwords(self, stopword_file):
        s_file = open(stopword_file)
        all_lines = s_file.readlines()
        s_file.close()
        stop_words = set()
        for line in all_lines:
            stop_words.add(line.strip())
        self.attribute_types.difference(stop_words)

    """
    Given a training datafile, add all features that appear at least m times to self.attribute_types
    """
    def collect_attribute_types(self, training_filename, m=2):
        self.attribute_types = set()
        t_file = open(training_filename)
        all_lines = t_file.readlines()
        t_file.close()

        # Store occurance of words
        tmp_dict = dict()

        for line in all_lines:
            words = self.extract_words(line)
            for word in words[1:]:
                if word in tmp_dict:
                    tmp_dict[word] += 1
                else:
                    tmp_dict[word] = 1
        for word in tmp_dict:
            if tmp_dict[word] >= m:
                self.attribute_types.add(word)


    """
    Given a training datafile, estimate the model probability parameters P(Y) and P(F|Y).
    Estimates should be smoothed using the smoothing parameter k.
    """
    def train(self, training_filename, k=0.01):
        self.label_prior = {}
        self.word_given_label = {}
        t_file = open(training_filename)
        all_lines = t_file.readlines()
        t_file.close()

        total = 0
        label_count = {"spam": 0, "ham": 0}
        word_count = dict()
        for line in all_lines:
            words = self.extract_words(line)
            label = words[0]
                
            for word in words:
                if word in self.attribute_types:
                    total += 1
                    if label == "spam":
                        label_count["spam"] += 1
                    else:
                        label_count["ham"] += 1
                    if (word, label) in word_count:
                        word_count[(word, label)] += 1
                    else:
                        word_count[(word, label)] = 1
        
        self.label_prior["spam"] = label_count["spam"] / total
        self.label_prior["ham"] = label_count["ham"] / total

        for word in self.attribute_types:
            word_ham = word_count[(word,"ham")] if (word,"ham") in word_count else 0
            word_spam = word_count[(word,"spam")] if (word,"spam") in word_count else 0
            self.word_given_label[(word, "ham")] = (word_ham + k) / (label_count["ham"] + k*len(self.attribute_types))
            self.word_given_label[(word, "spam")] = (word_spam + k) / (label_count["spam"] + k*len(self.attribute_types))


    """
    Given a piece of text, return a relative belief distribution over all possible labels.
    The return value should be a dictionary with labels as keys and relative beliefs as values.
    The probabilities need not be normalized and may be expressed as log probabilities. 
    """
    def predict(self, text):
        words = self.extract_words(text)[1:]
        ham = math.log(self.label_prior["ham"])
        spam = math.log(self.label_prior["spam"])
        for word in words:
            if word in self.attribute_types:
                ham += math.log(self.word_given_label[(word,"ham")])
                spam += math.log(self.word_given_label[(word,"spam")])
        return {"ham": ham, "spam": spam}


    """
    Given a datafile, classify all lines using predict() and return the accuracy as the fraction classified correctly.
    """
    def evaluate(self, test_filename):
        t_file = open(test_filename)
        all_lines = t_file.readlines()
        t_file.close()

        correct = 0
        for line in all_lines:
            words = self.extract_words(line)
            label = words[0]
            result = self.predict(line)
            if result["ham"] > result["spam"] and label == "ham":
                correct += 1
            if result["ham"] <= result["spam"] and label == "spam":
                correct += 1
            
        return correct/len(all_lines)


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("\nusage: ./hmm.py [training data file] [test or dev data file] [(optional) stopword file]")
        exit(0)
    elif len(sys.argv) == 3:
        classifier = NbClassifier(sys.argv[1], None)
    else:
        classifier = NbClassifier(sys.argv[1], sys.argv[3])
    print(classifier.evaluate(sys.argv[2]))