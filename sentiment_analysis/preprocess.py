#!/usr/bin/python
# -*- coding: utf-8 -*-
"""It preprocess the input corpus data to remove some noise and create a new 
column to save the content
"""

import pandas as pd
from pandas import Series


def concat_title_and_text(title_column:Series, subtitle_column:Series, content_column:Series) -> Series:
    """concatenate texts and save the concatenated one as a new column"""
    concatenated_column = title_column + ' ' + subtitle_column + ' ' + content_column

    return concatenated_column


def remove_noise(df_column:Series) -> Series:
    """remove noise influencing sentiment scores from the concatenated content column"""
    # Remove "Good morning"
    df_column = df_column.str.replace('Good morning.', '', regex=True)
    # Remove new line marks
    df_column = df_column.str.replace(r'\n', ' ', regex=True)
    # Remove multiple spaces
    df_column = df_column.str.replace(r'\s+', ' ', regex=True)
    
    return df_column.str.strip()

def preprocess_main(df: pd.DataFrame) -> pd.DataFrame:
    # Concatenate title, subtitle, and content
    df['concatenated_content'] = concat_title_and_text(df['Title'], df['Subtitle'], df['Main_Content'])
    
    # Remove noise from concatenated content
    df['Preprocessed_Content'] = remove_noise(df['concatenated_content'])
    
    return df