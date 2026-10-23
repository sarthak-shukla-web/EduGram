import json

import pytest

from app.services import topic_extractor


def test_extract_topics_returns_valid_topics(monkeypatch):
    expected_topics = {
        "topics": [
            {
                "name": "Stacks",
                "subtopics": ["LIFO", "Push", "Pop"],
                "description": (
                    "A data structure that follows "
                    "Last In, First Out."
                ),
            }
        ]
    }

    def mock_generate_response(prompt, response_format=None):
        return json.dumps(expected_topics)

    monkeypatch.setattr(
        topic_extractor,
        "generate_response",
        mock_generate_response,
    )

    result = topic_extractor.extract_topics(
        "A stack follows LIFO. Push adds an element "
        "and pop removes one."
    )

    assert isinstance(result, dict)
    assert "topics" in result
    assert len(result["topics"]) == 1
    assert result["topics"][0]["name"] == "Stacks"
    assert "Push" in result["topics"][0]["subtopics"]


def test_extract_topics_rejects_empty_input():
    with pytest.raises(ValueError):
        topic_extractor.extract_topics("")