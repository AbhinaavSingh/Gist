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
    # st.write('You selected:', sentenceValue)
     
    for sentence in sentenceValue:
        sum += sentenceValue[sentence]
    avg = int(sum / len(sentenceValue))
    summary = ""
    sentences = Stokenize(text)
    
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * avg)):
            summary += " " + sentence
    return summary


def create_summary_table(summary_list, summary_size):
    threshold = 5
    if summary_size == "Small":
        threshold = 5
    elif summary_size == "Medium":
        threshold = len(summary_list)/2
    else:
        threshold = len(summary_list)  
    
    display_table = """<table>
        <caption>Minutes of the Meeting</caption>
        <tr bgcolor="#EC5A53" style="color:white">
            <th>Time</th>
            <th>Speaker</th>
            <th>Salient Points</th>
        </tr>"""
        
    sentence_count = 0
    for sentence in summary_list:
        sentence_count += 1
        display_table += "<tr>"
        pre_point = (sentence[:sentence.rindex(':')]).split()
        time = str((pre_point[1]).split(":")[1]) + " minutes"
        name = pre_point[4]
        point = sentence[sentence.rindex(':')+1:]
        display_table += "<td>" + time + "</td><td>" + name + " </td><td>" + point+ "</td>"
        display_table += "</tr>"
        if sentence_count > threshold:
            break
    display_table += """</table>"""
    return display_table


def app(text):
    # st.markdown( """ <style> .sidebar { background-color:#33475b }</style>""")
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

    local_css("style.css")

    with st.container():
        st.title('Minutes of the Meeting')
        size_option = "Medium"
        size_option = st.selectbox('Select Summary Size',('Small', 'Medium', 'Large'))
        summary_text = summary(text)
        summary_list = summary_text.split(". ")
        st.markdown(
            create_summary_table(summary_list, size_option),
            unsafe_allow_html=True
        )
        st.download_button("Download summary", "\n".join(summary_list))
