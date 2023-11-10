import pandas as pd
import re
import streamlit as st
from functions.aimanager import AIManager





class SentimentManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.aim = AIManager(self.api_key)
        self.messages_prompt = []

    def add_message(self, role, content):
        self.messages_prompt.append({"role": role, "content": content})

    def reset_message(self):
        self.messages_prompt =[]
    def analyze_sentiment(self, keyword:str, sentence:str) -> float:
        try:
            # print(f"keyword {keyword}, sentence {sentence}")
            self.add_message("assistant", "You excel as a Picture quality expert and demonstrate exceptional skills in sentiment analysis.")
            # "You are a highly skilled sentiment analyst"
            self.add_message("user", f"Analyze the sentiment of the following text: "
                                     f"Rate the '{keyword}' in the sentence '{sentence}' on a scale from 0 (strongly negative) to 10 (strongly positive)."
                                     f"only respond as only number")
            bot_response = self.aim.get_text_from_gpt(self.messages_prompt)
            # print(f"bot_response: {bot_response}")
            bot_response = float(bot_response)
        except Exception as e:
            bot_response = 5.0

        self.reset_message()  # 리셋
        return bot_response

    def analyze_sentences(self, input_sentences:list, keywords: list):
        # print(keywords)
        # print(input_sentences)
        dict_analyzed_scores = dict()
        df_scores_list = []
        # df_scores = pd.DataFrame(columns=keywords)
        progress_bar = st.progress(0)
        for i, sentence in enumerate(input_sentences):
            dict_scores = {keyword: self.analyze_sentiment(keyword, sentence) for keyword in keywords}
            dict_analyzed_scores[f"{i}_{sentence}"]= dict_scores
            # print(f"{i}_{sentence}: {keyword} - {score}" for keyword, score in dict_scores.items())
            # print(f"{i}_{sentence}: {dict_scores}")  # Corrected print statement
            df = pd.DataFrame.from_dict(dict_scores, orient='index')
            df_scores_list.append(df)  # Append each DataFrame to the list
            progress_bar.progress(i)
        df_scores = pd.concat(df_scores_list, axis=1).T  # Concatenate all DataFrames in the list
        df_scores.reset_index(drop=True, inplace=True)  # Reset row index

        # print(df_scores)
        return df_scores


    def download_df_as_csv(self, df: pd.DataFrame, file_name: str, key:str, label:str="Download") -> None:

        csv_file = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label,
            csv_file,
            f"{file_name}.csv",
            "text/csv",
            key=key
        )
        # if preview:
        #     st.dataframe(df.head(3))
        return None

    def read_df_from(self, data_uploaded, column_name="sentences") -> pd.Series:
        df = pd.DataFrame()
        supported_formats = ['.csv', '.xlsx', '.txt']
        if data_uploaded.name.endswith(tuple(supported_formats)):
            if data_uploaded.name.endswith('.csv'):
                df = pd.read_csv(data_uploaded)
            elif data_uploaded.name.endswith('.xlsx'):
                df = pd.read_excel(data_uploaded, engine='openpyxl')
            elif data_uploaded.name.endswith('.txt'):
                df = pd.read_csv(data_uploaded, delimiter='\t')  # Assuming tab-separated text file
        else:
            st.error("This file format is not supported. Please upload a CSV, Excel, or text file.")
            st.stop()
        return df

    # 전처리 함수 정의

    def preprocess_text(self, text):
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = ' '.join(text.split())
        text = text.lower()
        return text

    def sample_sentences(self):
        sentences = [
            "I see the calibration settings page on each TV’s review. Are those the calibration settings that you’re saying should be used for actual viewing, or are they specifically designed for consistency during the testing process? I probably won’t pay a professional to calibrate my screen, but if there are some 'no brainer' settings to tweak, I want to be sure I’m doing it.",
            "The chart in your video has the S90C brightness numbers a lot higher compared to Rtings as well.So when looking at the comparison between S90C and A95L the chart on HDTVTest and if you would make one of the Rtings numbers both tell pretty much the same story. A95L has the upper hand in window sizes <10%, then at 10% things get more equal and at 25% and higher the peak brightness is basically identical. So the source you posted doesn’t contradict the Rtings measurements, rather it backs them up. HDTVTest for some reason just has higher numbers for all TVs, maybe a difference in how he measures things.",
            "So we did double check the brightness measurements and got very similar results. I can manage to get flashes closer to 1500 nits but they don’t stay that bright once the tv has warmed up. For what it’s worth, based on Vincent’s charts, it looks like his unit was around 1550 nits and our unit was around 1450. At high brightness levels, 100 nits won’t be super noticeable so it’s also quite possible that both units are within the expected tolerance. All in all, it remains one of the overall brightest OLED’s we’ve tested with great EOTF tracking. Hope that helps!",
            "Sony claims a 200% increase in peak brightness from the K to the L. and some reviewers noted  a difference. in unspecified brightness.rtings.com:  peak brightness readings  between the two from 10% window to 100% window do not come close to a 200% increase. Little difference. Difficult to explain reviewers comments. However, the HDR brightness went from 82 to 86.Two reviewers said the L came  very close to a $30,000 Sony broadcast monitor. Well, if that’s the case, the K, the LG G3 and Samsung 95C are also close to the monitor. Both the LG and Samsung are brighter than the K or L. Lg by a little. Samsung quite a bit.The only area on which those three were way  worse than the L was pre-calibration.Sure, it’s nice to have it close out of the box, but what rtings.com reader doesn’t calibrate his or her set to rtings.com calibrations? (Only very lazy ones.) Making this pretty meaningless.",
            "note Insider-exclusive early access results were used when comparing the A95L to other models – the text below may be revised when the final review is out (presumably sometime next week).wow, Sony. well done. compared to the A95K, the newer model has a couple of advantages.Sony got rid of the weird and wacky stand from last year, presumably because many users complained that placing a soundbar in front of the TV would block some of the bottom portion of the TV.the overall scores have increased a bit; see below A95K is left score, A95L is right score.mixed usage – 9.0 ➜ 9.2; this is the  highest score for mixed usage on TB 1.11, as of Nov 3, 2023 TV shows – 8.8 ➜ 8.9 sports – 8.9 ➜ 9.1 video games – 9.2 ➜ 9.3 movies in HDR – 9.1 ➜ 9.3 gaming in HDR – 9.0 ➜ 9.1 use as a PC monitor – 9.2 ➜ 9.4 below are the notable differences between the A95K and A95L. HDR – the A95L gets a bit brighter (score went from 8.2 to 8.6) in every realistic scene and window size, although ABL is ever so slightly worse.SDR – A95L is reasonably brighter; score went from 7.2 to 8.1.accuracy – A95L has much accuracy before calibration going from a score of 7.7 to 9.3.stutter – slightly worse on the newer model; was already bad due to the OLED panel’s nearly instantaneous response time.Xbox Series X/S compatibility – A95L now supports full 4K/ 120Hz in Dolby Vision; A95K didn’t support Dolby Vision at all on either console.that is everything that isn’t exactly the same or very close."
        ]

        df = pd.DataFrame({"sentences": sentences})
        df['sentences'] = df['sentences'].apply(self.preprocess_text)
        st.markdown("**Supported Formats: CSV, Excel, Text**")
        st.markdown("Excel (or CSV) Considerations: `sentences` column is the subject of analysis.")
        return df


