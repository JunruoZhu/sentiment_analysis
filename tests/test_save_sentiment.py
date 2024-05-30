import pytest
import pandas as pd
from pandas import DataFrame
from sentiment_analysis.save_sentiment import save_results_to_a_dataframe, get_mean_of_sentiment_and_article_counts, save_sentiment


@pytest.fixture
def sample_data():
    results = {
        '1': {'pos': 0.9, 'neg': 0.1},
        '2': {'pos': 0.1, 'neg': 0.9},
        '3': {'pos': 0.5, 'neg': 0.5}
    }
    corpus_data = {
        'id': ['1', '2', '3'],
        'Date': ['2022-01-01', '2022-01-02', '2022-01-03'],
        'Text': ['Good news', 'Bad news', 'Neutral news']
    }
    corpus = pd.DataFrame(corpus_data)
    output_file_path = 'test_output.csv'
    return results, corpus, output_file_path

def test_save_results_to_a_dataframe(sample_data):
    results, corpus, output_file_path = sample_data
    results_df = save_results_to_a_dataframe(results, corpus, output_file_path)

    # 读取生成的CSV文件
    results_df_saved = pd.read_csv(output_file_path)

    # 检查DataFrame的内容是否正确
    assert 'id' in results_df.columns
    assert 'pos' in results_df.columns
    assert 'neg' in results_df.columns
    assert 'Date' in results_df.columns
    assert 'Text' in results_df.columns
    assert 'URL' not in results_df.columns
    assert len(results_df) == len(corpus)

def test_get_mean_of_sentiment_and_article_counts(sample_data):
    results, corpus, output_file_path = sample_data
    results_df = save_results_to_a_dataframe(results, corpus, output_file_path)

    pos_df, neg_df, daily_articles_df = get_mean_of_sentiment_and_article_counts(results_df)

    assert 'Positive Sentiment' in pos_df.columns
    assert 'Negative Sentiment' in neg_df.columns
    assert 'Article Count' in daily_articles_df.columns
    assert pos_df['Positive Sentiment'].iloc[0] == 0.9
    assert neg_df['Negative Sentiment'].iloc[0] == 0.1
    assert daily_articles_df['Article Count'].iloc[0] == 1

def test_save_sentiment(sample_data):
    results, corpus, output_file_path = sample_data
    pos_df, neg_df, daily_articles_df = save_sentiment(results, corpus, output_file_path)

    assert 'Positive Sentiment' in pos_df.columns
    assert 'Negative Sentiment' in neg_df.columns
    assert 'Article Count' in daily_articles_df.columns
    assert pos_df['Positive Sentiment'].iloc[0] == 0.9
    assert daily_articles_df['Article Count'].iloc[0] == 1
