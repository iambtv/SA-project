#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import gensim
from gensim import corpora, models, similarities
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = gensim.models.KeyedVectors.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True) 
words = [["dog", "pet", "retriever", "grass", "cute"], ["example", "can", "success","hello","dog"], ["test", "sentence", "apple", "orange", "puppy"]]
#words = [['happy','excited','enjoy','unbelieveable'],['sad', 'too','bad'],['i','have','glad']]


target = "dog" #target is hint
#compute the sum
sentence_sum = []

for sentence in words:
	sum = 0
	for sentence_word in sentence:
		#for target_word in target:
		sim = model.similarity(sentence_word, target)
		sum = sum+sim
	#print (sum/5)
	sentence_sum.append(sum/5)
print (sentence_sum)



if sentence_sum > 0.5:
	print("This picture is accepted")

else:
	print("This picture is invalid")



