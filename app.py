
from functions.text import *
from functions.timeseries import *
from functions.multi_numeric import *

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
        st.subheader("Project Description")
        st.write("This project supports basic analysis.")

        st.markdown("---")

        with st.expander("Usage", expanded=True):
            st.markdown("**1. Text**")
            st.write("`Word frequency`, `Word clouds`, `network graph of topics`")
            st.markdown("**2. Time Series**")
            st.write("`ADF(Augmented Dickey-Fuller test)`, `ARIMA`, `Prophet`")
            st.markdown("**3. Multiple Numerical**")
            st.write("`Correlation`, `Distribution`, `ML Prediction`")
            # st.markdown("**4. Classification Analysis**")
        st.markdown("---")
        st.write(
            """     
            Written by TJ.Kim ☕
            """
        )
        st.markdown("---")

    # Insert containers separated into tabs:
    tab1, tab2, tab3 = st.tabs(["Text", "Time Series", "Multiple Numerical"])
    # tab1, tab2, tab3, tab4 = st.tabs(["Text Analysis", "Time Series Analysis", "Multiple Numerical Analysis", "Classification Analysis"])
    # Text Analysis
    with tab1:
        col1_tab1, col2_tab1 = st.columns([1, 2])
        with col1_tab1:
            st.subheader("1. Data Preparation")
            col1_col1_tab2, col2_col1_tab2 = st.columns([2, 1])
            with col1_col1_tab2:
                df_example_comments = call_example_comments()

                text_data_uploaded = st.file_uploader("Upload Text data", key="time_text_data")
            with col2_col1_tab2:
                # st.markdown("---")
                download_df_as_csv(df_example_comments, file_name="sample_text_data", key="download_text_sample_csv", label="Sample download")
                st.dataframe(df_example_comments.head(2))
                # download_df_as_csv(df_example_comments, file_name="sample_text_data", key="download_text_sample_csv", label="Sample")
                st.markdown("---")
            if text_data_uploaded is not None:
                try:
                    comments = read_comments_from(text_data_uploaded, column_name="comments")
                    comments_as_string = ' '.join(comments.astype(str))
                    nouns = prepare_nouns(comments)
                    df_word_freq = prepare_word_freq(nouns)
                    corpus, dictionary = prepare_networkg(comments_as_string)

                    st.session_state["tab1"] = {"plot_df_word_freq": df_word_freq,
                                                "wordcloud_nouns": nouns,
                                                "network_corpus":corpus,
                                                "network_dictionary":dictionary}
                    st.subheader("2. Analysis results")
                    # download btn
                    download_df_as_csv(df_word_freq, file_name="word_freq_analysis", key="download_csv_text_analysis", label="Result download")
                    st.dataframe(df_word_freq.head(3))
                except:
                    st.error('Please verify the file format', icon="🚨")
        with col2_tab1:
            if st.session_state["tab1"] is not None:
                st.subheader("3. Visualization")
                tab1_col2_tab1, tab2_col2_tab1, tab3_col2_tab1 = st.tabs(["Plot", "Word Cloud", "Network Graph"])
                with tab1_col2_tab1:
                    df_word_freq = st.session_state["tab1"]["plot_df_word_freq"]
                    plot_freq(df_word_freq)
                with tab2_col2_tab1:
                    nouns = st.session_state["tab1"]["wordcloud_nouns"]
                    plot_wordcloud(nouns)
                with tab3_col2_tab1:
                    corpus = st.session_state["tab1"]["network_corpus"]
                    dictionary = st.session_state["tab1"]["network_dictionary"]
                    plot_networkg(corpus, dictionary)
    # Time Series Analysis
    with tab2:
        col1_tab2, col2_tab2 = st.columns([1, 2])
        with col1_tab2:

            st.subheader("1. Data Preparation")
            col1_col1_tab2, col2_col1_tab2 = st.columns([2, 1])
            with col1_col1_tab2:
                df_example_timeseries = call_example_timeseries()
                time_data_uploaded = st.file_uploader("Upload Time Series", key="time_series_uploader")
            with col2_col1_tab2:
                download_df_as_csv(df_example_timeseries, "sample_timeseries_data", key="download_timeseries_sample_csv", label="Sample download")
                st.dataframe(df_example_comments.head(2))
                st.markdown("---")
            if time_data_uploaded is not None:
                try:
                    timeseries = read_timeseries_from(time_data_uploaded)

                    st.session_state["tab2"] = {"timeseries": timeseries}
                    plot_time_series(timeseries)
                except:
                    st.error('Please verify the file format', icon="🚨")
        with col2_tab2:
            if st.session_state["tab2"] is not None:
                st.subheader("2. Visualization")
                tab1_col2_tab3, tab2_col2_tab3  = st.tabs(["Prophet Plot", "TimeSeries"])
                timeseries = st.session_state["tab2"]["timeseries"]
                with tab1_col2_tab3:
                    plot_prophet(timeseries)
                with tab2_col2_tab3: 
                    plot_timesseries_arima(timeseries)
    with tab3:
        col1_tab3, col2_tab3 = st.columns([1, 2])
        with col1_tab3:

            st.subheader("1. Data Preparation")
            col1_col1_tab3, col2_col1_tab3 = st.columns([2, 1])
            with col1_col1_tab3:
                df_example_multi_numeric = call_example_multi_numeric()
                multi_data_uploaded = st.file_uploader("Upload numeric data", key="multi_numeric_uploader")
            with col2_col1_tab3:
                download_df_as_csv(df_example_multi_numeric, "sample_multi_numeric_data", key="download_multi_numeric_sample_csv",
                                   label="Sample download")
                st.dataframe(df_example_comments.head(2))
                st.markdown("---")
            if multi_data_uploaded is not None:
                try:
                    st.subheader("2. Build Model")
                    df_multi = read_numeric_from(multi_data_uploaded)
                    y_column = df_multi.columns[0]

                    numerical_columns, categorical_columns =  split_data_columns(df_multi.drop([y_column], axis=1))

                    tab1_col1_tab3, tab2_col1_tab3, tab3_col1_tab3, tab4_col1_tab3, tab5_col1_tab3= st.tabs(
                        ["Missing value", "Numeric Features", "Categorical Features", "Pre-process", "Machine learning"])
                    with tab1_col1_tab3:
                        if is_na(df_multi):
                            col1_col1_tab3, col2_col1_tab3 = st.columns(2)
                            with col1_col1_tab3:
                                plot_missing_value(df_multi)
                            with col2_col1_tab3:
                                df_multi = df_multi.interpolate(method='linear', inplace=True)
                                plot_missing_value(df_multi)
                        else:
                            plot_missing_value(df_multi)
                    with tab2_col1_tab3:
                        tab1_tab2_col1_tab3, tab2_tab2_col1_tab3, tab3_tab2_col1_tab3  = st.tabs(["Distribution", "Correlation", "Normality"])
                        with tab1_tab2_col1_tab3:
                            plot_distribution(df_multi.drop(categorical_columns, axis=1))
                        with tab2_tab2_col1_tab3:
                            plot_correlation(df_multi.drop(categorical_columns, axis=1))
                        with tab3_tab2_col1_tab3:
                            plot_normality(df_multi.drop(categorical_columns, axis=1))
                    with tab3_col1_tab3:
                        plot_stacked_bar(df_multi[categorical_columns])
                    with tab4_col1_tab3:
                        y = df_multi[y_column]
                        X = preprocess_data(df_multi)
                    with tab5_col1_tab3:
                        best_model_name, best_model, best_mse = select_best_model(X, y)
                        visualize_best_model_performance(X, y, best_model_name, best_model)
                        st.session_state["tab3"] = {"ml_model": best_model}
                except:
                    st.error('Please verify the file format', icon="🚨")
        with col2_tab3:
            if st.session_state["tab3"] is not None:
                st.subheader("3. Actual prediction")
                actual_multi_data_uploaded = st.file_uploader("Upload actual data", key="actual_multi_data_uploaded")
                if actual_multi_data_uploaded is not None:
                    try:
                        st.markdown("---")
                        df_X = read_numeric_from(actual_multi_data_uploaded)
                        X_new = preprocess_data(df_X, show=False)
                        best_model = st.session_state["tab3"].get("ml_model")
                        results = model_predictions_and_visual(X_new, best_model)
                        download_df_as_csv(results, file_name="numerical_results",
                                           key="download_csv_numeric_analysis", label="Result download")

                    except:
                        st.error('Please verify the file format', icon="🚨")



if __name__ == "__main__":
    main()
