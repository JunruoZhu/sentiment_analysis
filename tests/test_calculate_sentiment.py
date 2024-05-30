import pytest
import pandas as pd
import torch
from unittest.mock import MagicMock, patch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentiment_analysis.calculate_sentiment import compute_sentiment  # 替换为实际模块名称
from sentiment_analysis.calculate_sentiment import analyze_sentiment  # 替换为实际模块名称

@pytest.fixture
def sample_corpus():
    data = {
        'id': ['1', '2'],
        'Preprocessed_Content': ['This is a positive text.', 'This is a negative text.']
    }
    return pd.DataFrame(data)

@pytest.fixture
def mock_tokenizer():
    tokenizer = MagicMock()
    tokenizer.return_value = {
        "input_ids": torch.tensor([[1, 2, 3, 4]]),
        "attention_mask": torch.tensor([[1, 1, 1, 1]]),
        "overflow_to_sample_mapping": torch.tensor([0])
    }
    return tokenizer

@pytest.fixture
def mock_model():
    model = MagicMock()
    model.return_value = torch.tensor([[[0.1, 0.7, 0.2]]])  # Fake output logits
    return model

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def test_compute_sentiment(sample_corpus, mock_tokenizer, mock_model):
    with patch('transformers.AutoTokenizer.from_pretrained', return_value=mock_tokenizer):
        with patch('transformers.AutoModelForSequenceClassification.from_pretrained', return_value=mock_model):
            with patch('sentiment_analysis.calculate_sentiment.analyze_sentiment') as mock_analyze_sentiment:
                mock_analyze_sentiment.side_effect = lambda text, tokenizer, model: {
                    "neg": 0.1, "neu": 0.7, "pos": 0.2
                }

                results = compute_sentiment(sample_corpus)

                assert "1" in results
                assert "2" in results
                assert results["1"] == {"neg": 0.1, "neu": 0.7, "pos": 0.2}
                assert results["2"] == {"neg": 0.1, "neu": 0.7, "pos": 0.2}

if __name__ == "__main__":
    pytest.main()
