"""This script aims to save the result into a new dataframe and calculate the 
sentiment mean scores
"""
import pandas as pd
from pandas import DataFrame

def save_results_to_a_dataframe(results: dict, corpus: DataFrame, output_file_path: str) -> DataFrame:
    """
    Merge the results (sentiment scores) with corpus and save the merged DataFrame to a CSV file.
    
    Args:
    results (dict): A dictionary containing sentiment scores with keys as index.
    corpus (DataFrame): The original DataFrame containing the text corpus.
    output_file_path (str): The file path where the resulting DataFrame should be saved.
    
    Returns:
    results_df (DataFrame): The results dataframe with sentiment scores for texts.
    """
    # Create a new DataFrame keeping the sentiment values
    results_df = pd.DataFrame(results).T
    results_df = results_df.reset_index().rename(columns={"index": "id"})
    
    # Merge the results DataFrame with the corpus DataFrame
    results_df = results_df.merge(corpus, on="id", how="left")

    # Drop columns
    columns_to_drop = ['URL', 'Title', 'Subtitle', 'Main_Content', 'concatenated_content', 'Preprocessed_Content']
    results_df = results_df.drop(columns=[col for col in columns_to_drop if col in results_df.columns])

    # Make sure the date format
    results_df['Date'] = pd.to_datetime(results_df['Date'])
    results_df['Date'] = results_df['Date'].dt.strftime('%Y-%m-%d')  
    
    # Save the merged DataFrame to a CSV file
    results_df.to_csv(output_file_path, index=False)
    print('Saved the result dataframe to an output file path.')

    return results_df


def get_mean_of_sentiment_and_article_counts(results_df: DataFrame) -> (DataFrame, DataFrame, DataFrame):
    # compute daily average positive sentiment scores
    pos_df = results_df.groupby("Date")[["pos"]].mean().reset_index()
    pos_df = pos_df.rename(columns={"pos": "Positive Sentiment"})
    pos_df['Date'] = pd.to_datetime(pos_df['Date'])
    pos_df['Date'] = pos_df['Date'].dt.strftime('%Y-%m-%d') 
    
    # compute daily average negative sentiment scores
    neg_df = results_df.groupby("Date")[["neg"]].mean().reset_index()
    neg_df = neg_df.rename(columns={"neg": "Negative Sentiment"})
    neg_df['Date'] = pd.to_datetime(neg_df['Date'])
    neg_df['Date'] = neg_df['Date'].dt.strftime('%Y-%m-%d') 

    # compute daily article numbers 
    daily_articles_df = results_df.groupby("Date").size().reset_index(name='Article Count')
    daily_articles_df['Date'] = pd.to_datetime(daily_articles_df['Date'])
    daily_articles_df['Date'] = daily_articles_df['Date'].dt.strftime('%Y-%m-%d') 
    
    return pos_df, neg_df, daily_articles_df


def save_sentiment(results: dict, corpus: DataFrame, output_file_path: str) -> (DataFrame, DataFrame, DataFrame):
    """
    Main function to save sentiment results to a DataFrame and compute the average of emotions.
    
    Args:
    results (dict): A dictionary containing sentiment scores with keys as index.
    corpus (DataFrame): The original DataFrame containing the text corpus.
    output_file_path (str): The file path where the resulting DataFrame should be saved.
    
    Returns:
    pos_df (DataFrame): DataFrame containing the average of positive emotions.
    neg_df (DataFrame): DataFrame containing the average of negative emotions.
    daily_articles_df (DataFrame): DataFrame containing the count of articles per day.
    """
    # Save results to DataFrame and save to CSV
    results_df = save_results_to_a_dataframe(results, corpus, output_file_path)
    
    # Compute the average of positive and negative emotions and article counts
    pos_df, neg_df, daily_articles_df = get_mean_of_sentiment_and_article_counts(results_df)
    
    return pos_df, neg_df, daily_articles_df