
# Tokenizing Sentences
from io import StringIO
from nltk.tokenize import sent_tokenize 
 
# Tokenizing Words
from nltk.tokenize import word_tokenize 
import nltk
from string import punctuation
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
import pandas as pd
import sys

import streamlit as st
from PIL import Image



def clean(text):
    sample = text.split('**')
    sample.pop(0)
    clean_text = ""
    i = 0
    for t in sample:
        if i % 2 != 0:
            clean_text += str(t)
        i += 1
        # print ("Clean Text: ", clean_text)
    return clean_text
 
 
# Stopwords
stop_words = set(stopwords.words("english"))
 
# Tokenize
def Wtokenize(text):
    words = word_tokenize(text)
    return words
 
 
# Frequency of each word
def gen_freq_table(text):
    freqTable = dict()
    words = Wtokenize(text)
     
    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    return freqTable
 
# Sentence Tokenize
def Stokenize(text):
    sentences = sent_tokenize(text)
    return sentences
 
# Storing Sentence Scores
def gen_rank_sentences_table(text):
   
    sentenceValue = dict()

    freqTable = gen_freq_table(text)
     
    sentences = Stokenize(text)
 
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    return sentenceValue
 
 
def summary(text):
    sum = 0
    sentenceValue = gen_rank_sentences_table(text)
    for sentence in sentenceValue:
        sum += sentenceValue[sentence]
    avg = int(sum / len(sentenceValue))
    summary = ""
    sentences = Stokenize(text)
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * avg)):
            summary += " " + sentence
    return summary
 

def setup_streamlit():
    image = Image.open('resources/gist_logo.png')

    st.image(image, width =250, caption='More than just minutes of the meeting!')
    # st.title("Gist")
    # st.write("More than just minutes of the meeting!")
    uploaded_file = st.sidebar.file_uploader("Choose a transcript file")
    return uploaded_file
    

def get_transcript_data(uploaded_file):
    if uploaded_file is not None:
        # To read file as bytes:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        #  st.write(stringio)
        string_data = stringio.read()
        # st.write(string_data)
        return string_data


def main():
    uploaded_file = setup_streamlit()
    if st.sidebar.button('Generate Insights'):
        inp_text = get_transcript_data(uploaded_file)
        if("**" not in inp_text):
            text = inp_text
        else:
            cleaned_text = clean(inp_text)
            text = cleaned_text
        summary_text = summary(text)
        st.write("\nModel Summary: ")
        summary_list = summary_text.split(". ")
        for sentence in summary_list:
            st.write(sentence)
        text_file = open("summary.txt", "w")
        n = text_file.write(summary_text)
        text_file.close()

if __name__ == "__main__":
    main()