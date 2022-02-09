#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 13:01:40 2021

@author: anthonyyang
"""

import math

def clean_text(txt):
        """ takes a string of text 'txt' as a parameter and returns a list containing the words in 'txt' after it has been 'cleaned'
            this function will be used when you need to process each word in a text individually, without having to worry about punctuation or special characters
        """
        s = txt.lower().replace('.', '').replace(',', '').replace('?','').replace('!','').replace(';','').replace(':','').replace('"','').split()
        if s[-1] == '':
            return s[:-1]
        else:
            return s
        
    
def stem(s):
    """ accepts a string as a parameter. The function should return the stem of 's'
        ing, s, es, er, ers, irregular, ed, ly, ies
    """
    irregular = {'said' : 'say', 'made' : 'make', 'went' : 'go', 'gone' : 'go', 'taken' : 'take', 
                 'took' : 'take', 'came' : 'come', 'seen' : 'see', 'saw' : 'see', 'known' : 'know', 
                 'knew' : 'know', 'got' : 'get', 'gotten' : 'get', 'given' : 'give', 'gave' : 'give', 
                 'found' : 'find', 'thought' : 'think', 'told' : 'tell', 'became' : 'become', 
                 'shown' : 'show', 'showed' : 'show', 'left' : 'leave', 'brought' : 'bring', 
                 'begun' : 'begin', 'began' : 'begin', 'kept' : 'keep', 'held' : 'hold', 'written' : 'write', 
                 'wrote' : 'write', 'meant' : 'mean', 'met' : 'meet', 'sat' : 'sit', 'spoke' : 'speak', 'spoken' : 'speak', 
                 'lain' : 'lie', 'lay' : 'lie', 'led' : 'lead', 'lost' : 'lose', 'built' : 'build', 'understood' : 'understand', 
                 'drawn' : 'draw', 'drawn' : 'draw', 'chosen' : 'choose', 'chose' : 'choose'}
    if s in irregular:
        return irregular[s]
    elif s[-3:] == 'ing':
        return s[:-3]
    elif s[-2:] == 'er':
        return s[:-2]
    elif s[-3:] == 'ers':
        return s[:-3]
    elif s[-2:] == 'ed':
        return s[:-2]
    elif s[-2:] == 'ly':
        return s[:-2]
    elif s[-3:] == 'ies':
        return s[:-3] + 'y'
    elif s[-1] == 's':
        return s[:-1]
    elif s[-1] == 'e':
        return s[:-1]
    elif s[-2:] == 'es':
        return s[:-2]
    elif s[-1] == 'y':
        return s[:-1] + 'i'
    else:
        return s 
        
            
            
class TextModel:    
    
    """ serves as a blueprint for objects that model a body of text
        (collection of one or more text documents)
    """
    def __init__(self, model_name):
        """ constructs a new TextModel object by accepting a string 'model_name'
            as a parameter and initializing the following three attributes: name - label for text model
            use the model_name passed in as a parameter, words - dictionary that records the number of times
            each word appears in the text, word_lengths - dictionary that records the number of times each word 'length' appears
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}
        
    def __repr__(self):
        """ returns a string that includes the name of the model as well as the sizes of the dictionaries for 
            each feature of the text
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of punctuation: ' + str(len(self.punctuation))
        return s
    
    def add_string(self, s):
        """ adds a string of text 's' to the model by augmenting the feature dictionaries defined in the constructor.
            It should not explicitly return a value
        """
        punctuation = '!?."*'
        for x in s:
            if x in punctuation:
                if x not in self.punctuation:
                    self.punctuation[x] = 1
                else:
                    self.punctuation[x] += 1
                    
        
        split_str = s.replace('!','.').replace('?','.').split('.')
        
        if split_str[-1] == '':
            split_str = split_str[:-1]
            
        counter = 1
        for i in split_str:
            for r in range(len(i)):
                if i[r] == ' ':
                    counter += 1
                    
            if counter not in self.sentence_lengths:
                self.sentence_lengths[counter] = 1
            else:
                self.sentence_lengths[counter] += 1
                
            counter = 0
                    
        
        word_list = clean_text(s)
        
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
                
            else:
                self.words[w] += 1
                
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
            
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1
            
                
    def add_file(self, filename):
        """ adds all of the text in the file identified by 'filename' to the model
            it should not explicitly return a value
        """
        
        # still not sure if this method works as intended
        
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        
        text = f.read()
        f.close()
        self.add_string(text)
        
        
                
    def save_model(self):
        """ saves the TextModel object 'self' by writing its various feature dictionaries to files
        """
        d1 = self.words #first dictionary
        d2 = self.word_lengths #second dictionary
        
        d3 = self.stems
        d4 = self.sentence_lengths
        d5 = self.punctuation
        
        filename1 = self.name + '_words' #create dictionary name as outlined in assignment
        filename2 = self.name + '_word_lengths'
        
        filename3 = self.name + '_stems'
        filename4 = self.name + '_sentence_lengths'
        filename5 = self.name + '_punctuation'
        
        f1 = open(filename1, 'w')
        f1.write(str(d1)) #write d1 dictionary into new file called filename1
        f1.close()
        #f1 = file of dictionary words
        
        f2 = open(filename2, 'w')
        f2.write(str(d2))
        f2.close()
        #f2 = file of dictionary word_lengths
        
        f3 = open(filename3, 'w')
        f3.write(str(d3))
        f3.close()
        #f3 = file of dictionary stems
        
        f4 = open(filename4, 'w')
        f4.write(str(d4))
        f4.close()
        #f4 = file of dictionary sentence_lengths
        
        f5 = open(filename5, 'w')
        f5.write(str(d5))
        f5.close()
        #d5 = file of dictionary punctuation
                
        
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from their files and 
            assigns them to the attributes of the called TextModel
        """
        filename1 = self.name + '_words' #get name of file
        filename2 = self.name + '_word_lengths'
        filename3 = self.name + '_stems'
        filename4 = self.name + '_sentence_lengths'
        filename5 = self.name + '_punctuation'
        
        f1 = open(filename1, 'r') #open file called filename1
        d1_str = f1.read()
        f1.close()
        self.words = dict(eval(d1_str)) #converts string d1 to a dictionary and assigns self.words variable to the self.dictionary in order to use its values
        
        f2 = open(filename2, 'r')
        d2_str = f2.read()
        f2.close()
        self.word_lengths = dict(eval(d2_str))
        
        f3 = open(filename3, 'r')
        d3_str = f3.read()
        f3.close()
        self.stems = dict(eval(d3_str))
        
        f4 = open(filename4, 'r')
        d4_str = f4.read()
        f4.close()
        self.sentence_lengths = dict(eval(d4_str))
        
        f5 = open(filename5, 'r')
        d5_str = f5.read()
        f5.close()
        self.punctuation = dict(eval(d5_str))
        
    def classify(self, source1, source2):
        """ compares the textmodel object(self) to two other 'source' textmodel objects (source1 and source2)
            and determines which of these other textmodels is the more likely source of the called textmodel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        print('scores for ' + source1.name + ': ' + str(scores1))
        print('scores for ' + source2.name + ': ' + str(scores2))
    
        s1_score = 0
        s2_score = 0
    
        for x in range(len(scores1)):
            if scores1[x] > scores2[x]:
                s1_score += 1
            else:
                s2_score += 1
            
        winner = source1.name
        output = str(self.name) + ' is more likely to have come from ' + winner  
                    
        if s1_score > s2_score: 
            print(output)
        else:
            winner = source2.name
            print(output)
        
    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores mearusing the similarity of self and other
            - one score for each type of feature (words, word lengths, stems sentence lengths, and your additional feature)
            you should make repeated calls to compare_dictionaries, and put the resulting scores in a list that the method returns
        """
        word_score = []
            
        word_score += [compare_dictionaries(other.words, self.words)]
        word_score += [compare_dictionaries(other.word_lengths, self.word_lengths)]
        word_score += [compare_dictionaries(other.stems, self.stems)]
        word_score += [compare_dictionaries(other.sentence_lengths, self.sentence_lengths)]
        word_score += [compare_dictionaries(other.punctuation, self.punctuation)]
        
        return word_score


        
def compare_dictionaries(d1, d2):
    """ takes two feature dictionaries 'd1' and 'd2' as inputs, and it should compute and return
        their log similarity score using the outlined procedure
    """
    score = 0
    total = 0
    for x in d1:
        total += d1[x]
    
        
    for i in d2:
        if i in d1:
            score += d2[i]*math.log(d1[i]/total)
           
        else:
            score += d2[i]*math.log(0.5/total)
            
        
    return score
def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


def run_tests():
    """ your docstring goes here """
    source1 = TextModel('rowling')
    source1.add_file('JKRowling_text.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare_2.txt')

    new1 = TextModel('WR102')
    new1.add_file('WR_text.txt')
    new1.classify(source1, source2)

    #2
    source1 = TextModel('CNN')
    source1.add_file('cnn_article.txt')

    source2 = TextModel('NYTimes')
    source2.add_file('times_article.txt')

    new1 = TextModel('WR102')
    new1.add_file('WR_text.txt')
    new1.classify(source1, source2)

    #3
    source1 = TextModel('rowling')
    source1.add_file('JKRowling_text.txt')

    source2 = TextModel('CNN')
    source2.add_file('cnn_article.txt')

    new1 = TextModel('WR102')
    new1.add_file('WR_text.txt')
    new1.classify(source1, source2)
    
    #4
    source1 = TextModel('NYTimes')
    source1.add_file('times_article.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare_1.txt')

    new1 = TextModel('WR102')
    new1.add_file('WR_text.txt')
    new1.classify(source1, source2)






                
                
                
                
                
   