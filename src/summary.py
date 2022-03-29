import nltk
import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
# Tokenizing Words
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')
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


def app(text):
    st.title('Generating Summary')
    summary_text = summary(text)
    st.write("\nModel Summary: ")
    summary_list = summary_text.split(". ")
    for sentence in summary_list:
        st.write(sentence)
    st.download_button("Download summary", "\n".join(summary_list))
