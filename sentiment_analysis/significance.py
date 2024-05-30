#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This scripts does the two sample t-test to check if sentiment scores and 
article numbers are significant different before and after the price change 
max date.
"""

import pandas as pd
from scipy import stats

def calculate_max_percentage_drop_date_test(df_merged, column):
    df_merged['Price Percentage Change'] = df_merged[column].pct_change()
    # Only consider negative percentage changes (drops)
    df_drops = df_merged[df_merged['Price Percentage Change'] < 0]
    max_percentage_drop_date = df_drops[df_drops['Price Percentage Change'] == df_drops['Price Percentage Change'].min()]['Date'].values[0]
    return max_percentage_drop_date

def extract_period_data(df, max_change_date, period_days=30): 
    # Ensure max_change_date is of type pd.Timestamp
    max_change_date = pd.Timestamp(max_change_date)
    
    start_date = max_change_date - pd.Timedelta(days=30)
    end_date = max_change_date + pd.Timedelta(days=30)
    
    # Ensure the Date column is of type pd.Timestamp
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

def perform_t_test(df_pre, df_post, column):
    t_stat, p_value = stats.ttest_ind(df_pre[column], df_post[column], equal_var=False)
    return t_stat, p_value

def statistical_significance(price_df, neg_df, pos_df, article_count_df): 
    results = {}

    # Rename columns for consistency
    neg_df = neg_df.rename(columns={'neg': 'Negative Sentiment'})
    pos_df = pos_df.rename(columns={'pos': 'Positive Sentiment'})

    max_change_date = pd.Timestamp(calculate_max_percentage_drop_date_test(price_df, 'Close'))

    df_pre_neg = extract_period_data(neg_df, max_change_date, period_days=30)
    df_pre_neg = df_pre_neg[df_pre_neg['Date'] < max_change_date]
    df_post_neg = extract_period_data(neg_df, max_change_date, period_days=30)
    df_post_neg = df_post_neg[df_post_neg['Date'] > max_change_date]

    df_pre_pos = extract_period_data(pos_df, max_change_date, period_days=30)
    df_pre_pos = df_pre_pos[df_pre_pos['Date'] < max_change_date]
    df_post_pos = extract_period_data(pos_df, max_change_date, period_days=30)
    df_post_pos = df_post_pos[df_post_pos['Date'] > max_change_date]

    df_pre_article = extract_period_data(article_count_df, max_change_date, period_days=30)
    df_pre_article = df_pre_article[df_pre_article['Date'] < max_change_date]
    df_post_article = extract_period_data(article_count_df, max_change_date, period_days=30)
    df_post_article = df_post_article[df_post_article['Date'] > max_change_date]

    neg_t_stat, neg_p_value = perform_t_test(df_pre_neg, df_post_neg, 'Negative Sentiment')
    pos_t_stat, pos_p_value = perform_t_test(df_pre_pos, df_post_pos, 'Positive Sentiment')
    article_t_stat, article_p_value = perform_t_test(df_pre_article, df_post_article, 'Article Count')

    results['neg_t_stat'] = neg_t_stat
    results['neg_p_value'] = neg_p_value
    results['pos_t_stat'] = pos_t_stat
    results['pos_p_value'] = pos_p_value
    results['article_t_stat'] = article_t_stat
    results['article_p_value'] = article_p_value

    return results

