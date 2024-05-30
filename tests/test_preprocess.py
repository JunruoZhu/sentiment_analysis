import pytest
import pandas as pd

from sentiment_analysis.preprocess import concat_title_and_text, remove_noise, preprocess_main

@pytest.fixture
def sample_data():
    # Create a sample DataFrame
    data = {
        'Title': ['test title. '],
        'Subtitle': ['test subtitle.'],
        'Main_Content': ['test main content. Good morning. I have many tasks to work on.  ']
    }
    df = pd.DataFrame(data)
    return df

def test_concat_title_and_text():
    # Create a sample DataFrame
    data = {
        'Title': ['test title. '],
        'Subtitle': ['test subtitle.'],
        'Main_Content': ['test main content. Good morning. I have many tasks to work on.  ']
    }
    df = pd.DataFrame(data)
    # Apply the function
    df['concatenated_content'] = concat_title_and_text(df['Title'], df['Subtitle'], df['Main_Content'])
    # Check if the result is as expected
    expected_output = pd.Series(['test title.  test subtitle. test main content. Good morning. I have many tasks to work on.  '])
    assert df['concatenated_content'].equals(expected_output), "The concatenated column does not match expected output"

def test_remove_noise():
    # Create a sample DataFrame
    data = {
        'concatenated_content': ['test title.  test subtitle. test main content. Good morning. I have many tasks to work on.  ']
    }
    df = pd.DataFrame(data)
    # Apply the function 
    df['Preprocessed_Content'] = remove_noise(df['concatenated_content'])
    # check if the result is as expected
    expected_output = pd.Series(['test title. test subtitle. test main content. I have many tasks to work on.'])
    assert df['Preprocessed_Content'].equals(expected_output), "The noise was not removed as expected"

def test_preprocess_main(sample_data):
    df = sample_data
    preprocessed_df = preprocess_main(df)
    
    assert 'concatenated_content' in preprocessed_df.columns
    assert 'Preprocessed_Content' in preprocessed_df.columns
    
    assert preprocessed_df['concatenated_content'].iloc[0] == 'test title.  test subtitle. test main content. Good morning. I have many tasks to work on.  '
    assert preprocessed_df['Preprocessed_Content'].iloc[0] == 'test title. test subtitle. test main content. I have many tasks to work on.'

if __name__ == "__main__":
    pytest.main()
