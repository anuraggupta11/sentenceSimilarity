import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
import re

class SentenceSimilarity:
  __instance = None
  @staticmethod 
  def getInstance():
    """ Static access method. """
    if SentenceSimilarity.__instance == None:
        SentenceSimilarity()
    return SentenceSimilarity.__instance
  def __init__(self):
    """ Virtually private constructor. """
    if SentenceSimilarity.__instance != None:
      raise Exception("This class is a singleton!")
    else:
      self.module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3" 
      self.embed = hub.Module(self.module_url)
      SentenceSimilarity.__instance = self
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  #def __init__ (self):
  #  self.module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3" 
  #  self.embed = hub.Module(self.module_url)
  
  def giveSentenceMatchScore(self, sentence1, sentence2):
    tf.logging.set_verbosity(tf.logging.ERROR)
    messages = [sentence1, sentence2]
    with tf.Session() as session:
      session.run([tf.global_variables_initializer(), tf.tables_initializer()])
      message_embeddings = session.run(self.embed(messages))
      sentence1Embeddings = np.array(message_embeddings)[0]
      sentence2Embeddings = np.array(message_embeddings)[1]
      similarity12 = np.inner(sentence1Embeddings, sentence2Embeddings)
      return similarity12


#@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
# Import the Universal Sentence Encoder's TF Hub module
#embed = hub.Module(module_url)
# Reduce logging output.




