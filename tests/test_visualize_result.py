import pytest
import pandas as pd
from datetime import datetime
from pandas.testing import assert_frame_equal
import matplotlib.pyplot as plt
import os

from sentiment_analysis.visualize_result import load_and_process_data, calculate_max_percentage_drop_date, plot_coin, plot_articles_and_price, visualize_results 

@pytest.fixture
def price_data():
    data = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'Close': [100, 110, 105, 115]
    }
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

@pytest.fixture
def results_data():
    data = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'pos': [0.1, 0.2, 0.3, 0.4],
        'neg': [0.1, 0.1, 0.1, 0.1]
    }
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

@pytest.fixture
def article_count_data():
    data = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'Article Count': [5, 3, 4, 2]
    }
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def test_load_and_process_data(price_data, results_data):
    df_merged = load_and_process_data(price_data, results_data)
    expected_data = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'Close': [100, 110, 105, 115],
        'pos': [0.1, 0.2, 0.3, 0.4],
        'neg': [0.1, 0.1, 0.1, 0.1]
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df['Date'] = pd.to_datetime(expected_df['Date'])
    assert_frame_equal(df_merged, expected_df)


def test_calculate_max_percentage_drop_date(price_data, results_data):
    df_merged = load_and_process_data(price_data, results_data)
    max_drop_date = calculate_max_percentage_drop_date(df_merged, 'Close')
    assert pd.to_datetime(max_drop_date) == pd.to_datetime(datetime(2023, 1, 3))
 

def test_plot_coin(price_data, results_data):
    df_merged = load_and_process_data(price_data, results_data)
    df_merged.rename(columns={'pos': 'Positive Sentiment', 'neg': 'Negative Sentiment'}, inplace=True)
    max_change_date = calculate_max_percentage_drop_date(df_merged, 'Close')

    fig, ax = plt.subplots()
    plot_coin(ax, df_merged, 'Positive Sentiment', max_change_date, 'TestCoin', 'TestTitle')

    assert ax.get_title() == 'TESTCOIN Close Prices and TestTitle (Highlight Period)'

def test_plot_articles_and_price(price_data, article_count_data):
    df_merged = load_and_process_data(price_data, article_count_data)
    max_change_date = calculate_max_percentage_drop_date(df_merged, 'Close')

    fig, ax = plt.subplots()
    plot_articles_and_price(ax, df_merged, max_change_date, 'TestCoin')

    assert ax.get_title() == 'TESTCOIN Close Prices and Daily Article Count (Highlight Period)'

def test_visualize_results(price_data, results_data, article_count_data, tmpdir):
    folder = tmpdir.mkdir("test_folder")
    pos_df = results_data
    pos_df.rename(columns={'pos': 'Positive Sentiment'}, inplace=True)
    neg_df = results_data.copy()
    neg_df.rename(columns={'neg': 'Negative Sentiment'}, inplace=True)
    price_df = price_data
    article_count_df = article_count_data

    visualize_results(str(folder), pos_df, neg_df, price_df, article_count_df)

    pos_plot = folder.join(f'test_folder_price_pos.png')
    neg_plot = folder.join(f'test_folder_price_neg.png')
    articles_plot = folder.join(f'test_folder_price_articles.png')

    assert pos_plot.check()
    assert neg_plot.check()
    assert articles_plot.check()

if __name__ == "__main__":
    pytest.main()
