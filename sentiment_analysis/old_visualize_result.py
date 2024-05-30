#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This script aims to plot the result"""
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import regex as re
import os


def load_and_process_data(df_price, df_results):
    # df_price = pd.read_csv(price_path)
    # df_results = pd.read_csv(results_path)
    df_price['Date'] = pd.to_datetime(df_price['Date'])
    df_results['Date'] = pd.to_datetime(df_results['Date'])
    df_merged = pd.merge(df_price, df_results, on='Date')
    return df_merged


def calculate_max_change_date(df_merged, column):
    df_merged['Price Change'] = df_merged[column].diff().abs()
    max_change_date = df_merged[df_merged['Price Change'] == df_merged['Price Change'].max()]['Date'].values[0]
    return max_change_date


def plot_coin(ax, df_merged, sentiment_column, max_change_date, coin_name, title:str,column='Close'):
    if sentiment_column not in df_merged.columns:
        raise KeyError(f"The sentiment column '{sentiment_column}' is not found in the DataFrame.")

    highlight_period_start = pd.to_datetime(max_change_date) - pd.Timedelta(days=30)
    highlight_period_end = pd.to_datetime(max_change_date) + pd.Timedelta(days=30)

    df_highlight = df_merged[(df_merged['Date'] >= highlight_period_start) & (df_merged['Date'] <= highlight_period_end)]

    color = 'tab:blue'
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel(f'{coin_name} {column}', color=color, fontsize=14)
    ax.plot(df_highlight['Date'], df_highlight[column], label=f'{coin_name} {column}', color=color, linewidth=2.5)
    ax.tick_params(axis='y', labelcolor=color, labelsize=12)
    ax.tick_params(axis='x', labelsize=12, rotation=45)
    ax.legend(loc='upper left', fontsize=12)
    ax.grid(True)

    ax.axvline(max_change_date, color='red', linestyle='--', linewidth=2, label='Max Price Change Date')
    ax.legend(loc='upper left', fontsize=12)

    ax.annotate('Max Price Change Date',
                xy=(max_change_date, df_highlight[df_highlight['Date'] == max_change_date][column].values[0]),
                xytext=(max_change_date + pd.Timedelta(days=5), df_highlight[df_highlight['Date'] == max_change_date][column].values[0] * 1.05),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                fontsize=12)
    ax.set_title(f'{coin_name} {column} Prices and {title} (Highlight Period)', fontsize=16)

    # Plot sentiment data as bar chart
    ax2 = ax.twinx()
    color = 'tab:green'
    ax2.set_ylabel(f'{sentiment_column}', color=color, fontsize=14)
    ax2.bar(df_highlight['Date'], df_highlight[sentiment_column], alpha=0.5, color=color, label=f'{sentiment_column}')
    ax2.tick_params(axis='y', labelcolor=color, labelsize=12)
    ax2.legend(loc='upper right', fontsize=12)


def plot_articles_and_price(ax, df_merged, max_change_date, coin_name, column='Close'):
    highlight_period_start = pd.to_datetime(max_change_date) - pd.Timedelta(days=30)
    highlight_period_end = pd.to_datetime(max_change_date) + pd.Timedelta(days=30)

    df_highlight = df_merged[(df_merged['Date'] >= highlight_period_start) & (df_merged['Date'] <= highlight_period_end)]

    color = 'tab:blue'
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel(f'{coin_name} {column}', color=color, fontsize=14)
    ax.plot(df_highlight['Date'], df_highlight[column], label=f'{coin_name} {column}', color=color, linewidth=2.5)
    ax.tick_params(axis='y', labelcolor=color, labelsize=12)
    ax.tick_params(axis='x', labelsize=12, rotation=45)
    ax.legend(loc='upper left', fontsize=12)
    ax.grid(True)

    ax.axvline(max_change_date, color='red', linestyle='--', linewidth=2, label='Max Price Change Date')
    ax.legend(loc='upper left', fontsize=12)

    ax.annotate('Max Price Change Date',
                xy=(max_change_date, df_highlight[df_highlight['Date'] == max_change_date][column].values[0]),
                xytext=(max_change_date + pd.Timedelta(days=5), df_highlight[df_highlight['Date'] == max_change_date][column].values[0] * 1.05),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                fontsize=12)
    ax.set_title(f'{coin_name} {column} Prices and Daily Article Count (Highlight Period)', fontsize=16)

    # Plot article count data as bar chart
    ax2 = ax.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('Daily Article Count', color=color, fontsize=14)
    ax2.bar(df_highlight['Date'], df_highlight['Article Count'], alpha=0.5, color=color, label='Daily Article Count')
    ax2.tick_params(axis='y', labelcolor=color, labelsize=12)
    ax2.legend(loc='upper right', fontsize=12)


def visualize_results(folder, pos_df, neg_df, price_df, article_count_df):  
    subfolder_name = os.path.basename(folder)

    # Merge price and sentiment data
    pos_merged = load_and_process_data(price_df, pos_df)
    pos_merged.rename(columns={'pos': 'Positive Sentiment'}, inplace=True)
    neg_merged = load_and_process_data(price_df, neg_df)
    neg_merged.rename(columns={'neg': 'Negative Sentiment'}, inplace=True)

    # Merge price and article count data
    article_count_merged = load_and_process_data(price_df, article_count_df)

    # Calculate the date of maximum price change
    max_change_date_pos = calculate_max_change_date(pos_merged, 'Close')
    max_change_date_neg = calculate_max_change_date(neg_merged, 'Close')
    max_change_date_articles = calculate_max_change_date(article_count_merged, 'Close')

    # Plot price and positive sentiment
    fig, ax = plt.subplots(figsize=(12, 8))
    plot_coin(ax, pos_merged, 'Positive Sentiment', max_change_date_pos, subfolder_name, 'Positive Sentiment')
    plt.savefig(os.path.join(folder, f'{subfolder_name}_price_pos.png'))
    plt.close()

    # Plot price and negative sentiment
    fig, ax = plt.subplots(figsize=(12, 8))
    plot_coin(ax, neg_merged, 'Negative Sentiment', max_change_date_neg, subfolder_name, 'Negative Sentiment')
    plt.savefig(os.path.join(folder, f'{subfolder_name}_price_neg.png'))
    plt.close()

    # Plot price and daily article count
    fig, ax = plt.subplots(figsize=(12, 8))  
    plot_articles_and_price(ax, article_count_merged, max_change_date_articles, subfolder_name)
    plt.savefig(os.path.join(folder, f'{subfolder_name}_price_articles.png'))  
    plt.close()