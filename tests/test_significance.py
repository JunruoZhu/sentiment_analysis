import pytest
import pandas as pd
import numpy as np
from sentiment_analysis.significance import calculate_max_percentage_drop_date_test, extract_period_data, perform_t_test

# Create testing data
@pytest.fixture
def price_data():
    np.random.seed(0)
    price_data = {
        'Date': pd.date_range(start='2023-01-01', periods=100),
        'Close': np.random.normal(100, 10, 100).tolist()
    }
    price_df = pd.DataFrame(price_data)
    return price_df

@pytest.fixture
def neg_data():
    neg_data = {
        'Date': pd.date_range(start='2023-01-01', periods=100),
        'neg': np.random.normal(0.1, 0.05, 100).tolist()
    }
    neg_df = pd.DataFrame(neg_data)
    return neg_df

@pytest.fixture
def pos_data():
    pos_data = {
        'Date': pd.date_range(start='2023-01-01', periods=100),
        'pos': np.random.normal(0.2, 0.05, 100).tolist()
    }
    pos_df = pd.DataFrame(pos_data)
    return pos_df

@pytest.fixture
def article_count_data():
    article_count_data = {
        'Date': pd.date_range(start='2023-01-01', periods=100),
        'Article Count': np.random.randint(1, 20, 100).tolist()
    }
    article_count_df = pd.DataFrame(article_count_data)
    return article_count_df

@pytest.fixture
def sample_data(price_data, neg_data, pos_data, article_count_data):
    return price_data, neg_data, pos_data, article_count_data


def test_calculate_max_percentage_drop_date_test(sample_data):
    price_df, _, _, _ = sample_data
    max_drop_date = calculate_max_percentage_drop_date_test(price_df, 'Close')
    
    # Ensure max_drop_date is converted to pd.Timestamp for assertion
    max_drop_date = pd.Timestamp(max_drop_date)
    
    assert isinstance(max_drop_date, pd.Timestamp), "Max percentage drop date should be of type Timestamp"
    
    # Calculate expected max drop date
    price_df['Price Percentage Change'] = price_df['Close'].pct_change()
    df_drops = price_df[price_df['Price Percentage Change'] < 0]
    expected_max_drop_date = df_drops[df_drops['Price Percentage Change'] == df_drops['Price Percentage Change'].min()]['Date'].values[0]
    expected_max_drop_date = pd.Timestamp(expected_max_drop_date)  # Ensure the expected date is of type Timestamp
    
    assert max_drop_date == expected_max_drop_date, "Max percentage drop date should be correctly calculated"

def test_extract_period_data(sample_data):
    price_df, neg_df, _, _ = sample_data
    max_change_date = pd.Timestamp(calculate_max_percentage_drop_date_test(price_df, 'Close'))
    period_data = extract_period_data(neg_df, max_change_date, period_days=30)
    assert not period_data.empty, "Extracted period data should not be empty"
    assert period_data['Date'].min() >= max_change_date - pd.Timedelta(days=30), "Period start date is incorrect"
    assert period_data['Date'].max() <= max_change_date + pd.Timedelta(days=30), "Period end date is incorrect"

def test_perform_t_test(sample_data):
    price_df, neg_df, _, _ = sample_data
    max_change_date = pd.Timestamp(calculate_max_percentage_drop_date_test(price_df, 'Close'))
    df_pre = extract_period_data(neg_df, max_change_date, period_days=30)
    df_pre = df_pre[df_pre['Date'] < max_change_date]
    df_post = extract_period_data(neg_df, max_change_date, period_days=30)
    df_post = df_post[df_post['Date'] > max_change_date]
    t_stat, p_value = perform_t_test(df_pre, df_post, 'neg')
    assert isinstance(t_stat, float), "t_stat should be of type float"
    assert isinstance(p_value, float), "p_value should be of type float"