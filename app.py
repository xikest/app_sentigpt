import streamlit as st
from datetime import datetime
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import pos_tag
from wordcloud import WordCloud
import plotly.express as px
import pyLDAvis.gensim
import gensim
import gensim.corpora as corpora


def make_dataframe_ex() -> pd.DataFrame:
    # creating exmaple data
    comments = {
        'comments': [
            "This is a sample comment about data analysis. Data analysis is a crucial step in any research or business decision-making process. It involves collecting, cleaning, and interpreting data to gain valuable insights. Data analysts use various tools and techniques to uncover patterns and trends in data. In today's data-driven world, data analysis skills are in high demand.",
            "Natural language processing (NLP) is a fascinating field of study. NLP focuses on the interaction between computers and human language. NLP applications include sentiment analysis, machine translation, chatbots, and more. NLP researchers develop algorithms to understand and generate human language. The possibilities in NLP seem endless, and it's an exciting area to explore.",
            "Machine learning is revolutionizing industries across the globe. It's the science of getting computers to learn and act like humans do. Machine learning algorithms are used in recommendation systems, image recognition, autonomous vehicles, and many other areas. As machine learning advances, it continues to shape the future of technology and innovation.",
            "Python is a versatile programming language commonly used in data science and machine learning. Its readability and extensive libraries make it a popular choice among data scientists. Python's simplicity and flexibility make it an excellent language for analyzing and visualizing data. It's no wonder that Python is a go-to language for data professionals.",
            "Artificial intelligence (AI) is a transformative technology with applications in healthcare, finance, and more. AI systems can perform tasks that typically require human intelligence. These systems learn from data, recognize patterns, and make decisions. The growth of AI is expected to drive significant changes in various industries."
        ]
    }
    # dataframe
    df = pd.DataFrame(comments)
    return df
def main():
    # basic setting
    st.set_page_config(
        page_title="plot stream",
        layout="wide")

    # session state initialize
    st.session_state.setdefault("tab1", None)
    st.session_state.setdefault("tab2", None)
    st.session_state.setdefault("tab3", None)
    
    # Title
    st.header("Plot Visualization")

    # Side bar
    with st.sidebar:
        # Basic description
        with st.expander("Project Description", expanded=True):
            st.write(
                """     
                - This project supports basic text analysis.
                """
            )
        st.markdown("---")
        st.write("This project has been helpful, a cup of coffee would be a great encouragement. ☕️")
        st.markdown("---")
        st.write(
            """     
            Written by TJ.Kim
            """
        )

    # Insert containers separated into tabs:
    tab1, tab2, tab3 = st.tabs(["Text Analysis", "Correlation", "LDA"])
    # tab1 = st.tabs(["Word Frequency"])
    # tab1.write("EDA")
    # tab2.write("plot2")
    # tab3.write("plot3")


    with tab1:
        # function
        col1_tab1, col2_tab1, col3_tab1 = st.columns(3)
        with col1_tab1:
            flag_word_freq_df = False
            # Right seg
            st.subheader("1. Data Preparation")
            df_example = make_dataframe_ex()
            st.write("▶ Example: Input Data Form")
            st.write("'comments' column is the subject of analysis. Use the column name 'comments.'")
            st.write("If no column name is specified, the first column will be the subject of analysis.")
            st.dataframe(df_example.head(2))            
            data_uploaded = st.file_uploader("▶ Upload CSV or Excel files only.")
            if data_uploaded is not None:
                if data_uploaded.name.endswith('.csv'):
                    df = pd.read_csv(data_uploaded)
                elif data_uploaded.name.endswith('.xlsx'):
                    df = pd.read_excel(data_uploaded, engine='openpyxl')
                else:
                    st.error("This file format is not supported. Please upload a CSV or Excel file.")
                    st.stop()

                st.subheader("2. Data Preview")
                st.dataframe(df.head(3))

                # extract data
                try:
                    try:
                        comments = df['comments']
                    except KeyError:
                        comments = df.iloc[:, 0]

                    all_words = []

                    #nltk data download
                    nltk.download('punkt')
                    nltk.download('stopwords')
                    nltk.download('averaged_perceptron_tagger')
            
                    for comment in comments:
                        tokens = word_tokenize(comment)  # tokenize
                        all_words.extend(tokens)
                    # stopward
                    stop_words = set(stopwords.words('english'))
                    filtered_words = [word.lower() for word in all_words if word.isalnum() and word.lower() not in stop_words]
                    # nouns
                    nouns = [word for (word, tag) in pos_tag(filtered_words) if tag.startswith('N')]
                    # nouns frequncy
                    noun_counts = FreqDist(nouns)
                    df_word_freq = pd.DataFrame(list(noun_counts.items()), columns=['Nouns', 'Frequency'])
                    # sorted
                    df_word_freq = df_word_freq.sort_values(by='Frequency', ascending=False)
                    st.subheader("3. Analysis results")

                    # download btn
                    csv_word_freq = df_word_freq.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download",
                        csv_word_freq,
                        "word_freq_analysis.csv",
                        "text/csv",
                        key='download-csv'
                    )
                    
                    st.write("▶ Preview")
                    st.dataframe(df_word_freq.head(3))
                    st.session_state["tab1"] = {"df_word_freq": df_word_freq, "nouns": nouns}
                except:
                    st.error('Please verify the file format', icon="🚨")
    
        with col2_tab1:
            if st.session_state["tab1"] is not None:
                st.subheader("4. Visualization")
                tab1_col2_tab1, tab2_col2_tab1 = st.tabs(["Plot", "Word Cloud"])   
                with tab1_col2_tab1:
                    df = st.session_state["tab1"]["df_word_freq"]
                    top_words = df.head(10)
                    fig = px.bar(top_words, x='Nouns', y='Frequency', title="Top 10 Words Frequency")
                    fig.update_xaxes(tickangle=45)
                    # fig.update_layout(width=330, height=330)
                    st.plotly_chart(fig)
                with tab2_col2_tab1:
                    nouns = st.session_state["tab1"]["nouns"]
                     # Word Cloud: 800*400
                    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(nouns))
                    fig = px.imshow(wordcloud, binary_string=True)
                    fig.update_xaxes(visible=False)
                    fig.update_yaxes(visible=False)
                    # fig.update_layout(width=330, height=330)
                    st.plotly_chart(fig)


        with col3_tab1:

            # 토픽 모델링에 사용할 샘플 데이터 생성 (실제로는 여러 문서로 구성된 말뭉치를 사용해야 합니다)
            data = [
                "텍스트 데이터 분석을 위한 토픽 모델링은 중요한 작업입니다.",
                "LDA (Latent Dirichlet Allocation)는 토픽 모델링의 일종입니다.",
                "텍스트 데이터에서 토픽을 추출하려면 LDA 모델을 사용할 수 있습니다.",
                "pyLDAvis는 토픽 모델링 결과를 시각화하는 도구 중 하나입니다.",
            ]

            # 데이터 전처리: 텍스트 데이터를 토큰화하고 딕셔너리를 생성합니다.
            data_words = [gensim.utils.simple_preprocess(text, deacc=True) for text in data]
            dictionary = corpora.Dictionary(data_words)
            corpus = [dictionary.doc2bow(text) for text in data_words]

            # LDA 모델 학습
            lda_model = gensim.models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=2)

            # Streamlit 앱 시작
            st.title("토픽 모델링 시각화")

            # pyLDAvis 시각화
            pyLDAvis.enable_notebook()
            vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
            st.pydeck_chart(vis)

    # second tab: Correlation Plot
    with tab2:
        st.subheader("Correlation Plot Content")
    # third tab: LDA
    with tab3:
        st.subheader("LDA Content")

if __name__ == "__main__":
    main()
