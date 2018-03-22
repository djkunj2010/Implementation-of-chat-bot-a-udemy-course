# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 16:51:49 2018

@author: Kunal
"""

#Data preprocessing for chat bot
# Step 1 importing library 
import numpy as np
import tensorflow as tf
import re
import time

#importing datasets

lines = open("movie_lines.txt", encoding = "utf-8", errors = "ignore" ).read().split("\n")
conversations = open("movie_conversations.txt", encoding = "utf-8", errors = "ignore" ).read().split("\n")


#Creating a dictionary that maps each line and its ID

id2line = {}
for line in lines:
    _line = line.split(" +++$+++" )
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]
    
#creating list of all the conversations

conversations_id =[]

for conversation in conversations[:-1]:
    
    _conversation = conversation.split( " +++$+++ ")[-1][1:-1].replace("'","").replace(" ","")
    #We have used this technique to remove the square bracket,space and quotes in conversation variable last index, because we don't need the brackets
    conversations_id.append(_conversation.split(','))
    
# Getting seperately the question and answer

questions = []    
answers = []    

for conversation in conversations_id:
    for i in range(len(conversation) - 1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])
# Doing cleaning of text

def clean_text(text):
    text = text.lower() #making all text in lower so that we have all text in same cases
    text = re.sub(r"i'm", "i am", text) # Cleaning of apostopes by using "re LIB"
    text = re.sub(r"he 's " , " he is",text)
    text = re.sub(r"she 's ", "she is", text)
    text = re.sub(r"that's", " that is", text)
    text = re.sub(r"what's", " what is", text)
    text = re.sub(r"where's", " where is", text)    
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", " will not", text)
    text = re.sub(r"can't", " cannot", text)
    text = re.sub(r"[-()\"#@/;:<>{}+=~|.?,]", "", text)
    return text

# cleaning the question
clean_questions = []

for question in questions:
    clean_questions.append(clean_text(question))
    
# cleaning the ansswer
clean_answers = []

for answer in answers:
    clean_answers.append(clean_text(answer))
    
#creating a dictionary that maps each word to its number of occurence

word2count = {}

for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] +=1
            
for answer in clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] +=1
                        
# creating the dictionary that map the question words and the answer words to a unique integer

threshold = 20

questionsword2int = {}
word_number = 0 #initialize the for loop

#it counts the most frequent word and counted
for word,count in word2count.items():
    if count >= threshold:
        questionsword2int[word] = word_number 
        word_number +=1

answersword2int = {}
word_number = 0 #initialize the for loop

#it counts the most frequent word
for word,count in word2count.items():
    if count >= threshold:
        answersword2int[word] = word_number 
        word_number +=1        

#Adding the last tokens to these two dictionaries

tokens = ['<PAD>' , '<EOS>' , '<OUT>' , '<SOS>' ]
for token in tokens:
    questionsword2int[token] = len(questionsword2int) + 1
    
for token in tokens:
    answersword2int[token] = len(answersword2int) + 1    
    
#creating inverse dictionary of the answersword2int dictionary

answersint2word = {w_i: w for w, w_i in answersword2int.items() }

#Adding the End of string token to the end of every answer

for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>' #space is given to differneitate the last word and EOS
    
#Translating all the questions and the answers into integers
#and replacing all the words by <out>

questions_to_int = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in questionsword2int:
            ints.append(questionsword2int['<OUT>'])
        else:
            ints.append(questionsword2int[word])
            
    questions_to_int.append(ints)
 
answers_to_int = []
for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word not in answersword2int:
            ints.append(answersword2int['<OUT>'])
        else:
            ints.append(answersword2int[word])
            
    answers_to_int.append(ints)   
    
        
# sorting questions and answers by the length of questions

sorted_clean_question = []
sorted_clean_answer = []

for length in range(1, 25+1):
    for i in enumerate(questions_to_int):
        if len(i[1]) == length:
            sorted_clean_question.append(questions_to_int[i[0]])
            sorted_clean_answer.append(answers_to_int[i[0]])
            
            
    
    
    



