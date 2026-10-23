import json

import pytest

from app.services import learning_path


def test_generate_learning_path_returns_ordered_topics(monkeypatch):
    sample_topics = [
        {
            "name": "Arrays",
            "subtopics": ["Indexing", "Element access"],
            "description": "Elements stored at indexed positions.",
        },
        {
            "name": "Stacks",
            "subtopics": ["LIFO", "Push", "Pop"],
            "description": "A Last In, First Out data structure.",
        },
    ]

    mocked_ai_response = {
        "learning_path": [
            {
                "id": 2,
                "reason": "Study stacks after understanding basic data structures.",
            },
            {
                "id": 1,
                "reason": "Study arrays to understand indexed data storage.",
            },
        ]
    }

    def mock_generate_response(prompt, response_format=None):
        return json.dumps(mocked_ai_response)

    monkeypatch.setattr(
        learning_path,
        "generate_response",
        mock_generate_response,
    )

    result = learning_path.generate_learning_path(sample_topics)

    assert isinstance(result, dict)
    assert "learning_path" in result

    generated_path = result["learning_path"]

    assert len(generated_path) == 2

    # Verify that the AI's recommended order is preserved.
    assert generated_path[0]["order"] == 1
    assert generated_path[0]["topic"] == "Stacks"

    assert generated_path[1]["order"] == 2
    assert generated_path[1]["topic"] == "Arrays"

    # Verify that each entry has a meaningful explanation.
    for item in generated_path:
        assert isinstance(item["reason"], str)
        assert item["reason"].strip()


def test_generate_learning_path_rejects_empty_topics():
    with pytest.raises(ValueError):
        learning_path.generate_learning_path([])