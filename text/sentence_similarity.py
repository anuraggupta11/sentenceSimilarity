import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import time

def ss(sentence1, sentence2):
    start = time.time()
    print("Init called -----``````~~~~~~")
    #global embed,g,session,messages,output
    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3" 
    embed = hub.Module(module_url)
    g = tf.get_default_graph()
    session = tf.Session(graph=g)
    session.run([tf.global_variables_initializer(), tf.tables_initializer()])   
    messages = tf.placeholder(dtype=tf.string, shape=[None])
    output = embed(messages)
    message_embeddings = session.run(output, feed_dict={messages:  [sentence1, sentence2]})
    print('Embedding done after: '+str(time.time()-start))
    sentence1Embeddings = np.array(message_embeddings)[0]
    sentence2Embeddings = np.array(message_embeddings)[1]
    print('Inner product done after: '+str(time.time()-start))
    similarity12 = np.inner(sentence1Embeddings, sentence2Embeddings)
    return similarity12