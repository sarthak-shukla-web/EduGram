import json

from app.services.ai_engine import AIEngineError, generate_response


MAX_TOPICS = 40

LEARNING_PATH_SCHEMA = {
    "type": "object",
    "properties": {
        "learning_path": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "reason": {"type": "string"},
                },
                "required": ["id", "reason"],
            },
        }
    },
    "required": ["learning_path"],
}


def _validate_and_build_path(result: dict, topics: list[dict]) -> dict:
    """Validate the AI's ordering and construct the final learning path."""

    if not isinstance(result, dict):
        raise AIEngineError("The AI returned an invalid response.")

    learning_path = result.get("learning_path")

    if not isinstance(learning_path, list):
        raise AIEngineError("The AI response does not contain a valid learning path.")

    if len(learning_path) != len(topics):
        raise AIEngineError("The AI did not include every topic.")

    expected_ids = set(range(1, len(topics) + 1))
    returned_ids = set()
    validated_items = []

    for item in learning_path:
        if not isinstance(item, dict):
            raise AIEngineError("The AI returned an invalid topic entry.")

        topic_id = item.get("id")
        reason = item.get("reason")

        # bool is a subclass of int in Python, so reject it explicitly.
        if isinstance(topic_id, bool) or not isinstance(topic_id, int):
            raise AIEngineError("The AI returned an invalid topic ID.")

        if topic_id not in expected_ids:
            raise AIEngineError("The AI returned an unknown topic ID.")

        if topic_id in returned_ids:
            raise AIEngineError("The AI returned a duplicate topic ID.")

        if not isinstance(reason, str) or not reason.strip():
            raise AIEngineError("The AI returned an empty explanation.")

        returned_ids.add(topic_id)
        validated_items.append({
            "id": topic_id,
            "reason": reason.strip(),
        })

    if returned_ids != expected_ids:
        raise AIEngineError("The AI did not include every topic exactly once.")

    # Only Python determines the final topic names and order numbers.
    final_path = []

    for order, item in enumerate(validated_items, start=1):
        topic = topics[item["id"] - 1]

        final_path.append({
            "order": order,
            "topic": topic["name"].strip(),
            "reason": item["reason"],
        })

    return {"learning_path": final_path}


def generate_learning_path(topics: list[dict]) -> dict:
    """Generate a validated learning sequence from extracted topics."""

    if not isinstance(topics, list) or not topics:
        raise ValueError("At least one topic is required.")

    if len(topics) > MAX_TOPICS:
        raise ValueError(
            f"A maximum of {MAX_TOPICS} topics can be processed at once."
        )

    for topic in topics:
        if (
            not isinstance(topic, dict)
            or not isinstance(topic.get("name"), str)
            or not topic["name"].strip()
        ):
            raise ValueError("Every topic must have a non-empty name.")

    names = [topic["name"].strip().casefold() for topic in topics]

    if len(names) != len(set(names)):
        raise ValueError("Input topics must have unique names.")

    # The model receives IDs, names, and descriptions.
    # It returns IDs, so it does not need to reproduce topic names.
    numbered_topics = [
        {
            "id": index,
            "name": topic["name"].strip(),
            "description": topic.get("description", ""),
            "subtopics": topic.get("subtopics", []),
        }
        for index, topic in enumerate(topics, start=1)
    ]

    topic_data = json.dumps(numbered_topics, ensure_ascii=False)

    prompt = f"""
You are EduGram, an educational learning-path assistant.

Arrange the supplied topics into a sensible study sequence.

Rules:
1. Include every supplied topic exactly once.
2. Use the integer IDs exactly as supplied.
3. Never invent IDs or omit any IDs.
4. Put foundational topics before topics that depend on them.
5. Give a short, student-friendly explanation for each topic's position.
6. Return only the requested structured output.

The topics are:
<topics>
{topic_data}
</topics>

Return the topics in the recommended learning order.
"""

    for attempt in range(2):
        current_prompt = prompt

        if attempt == 1:
            current_prompt += f"""

IMPORTANT: Your previous response was invalid.
Return exactly {len(topics)} entries.
Use every integer ID from 1 to {len(topics)} exactly once.
Each entry must contain an integer "id" and a non-empty string "reason".
Keep every reason to one short sentence.
"""

        try:
            response = generate_response(
                current_prompt,
                response_format=LEARNING_PATH_SCHEMA,
            )

            result = json.loads(response)

            return _validate_and_build_path(result, topics)

        except json.JSONDecodeError as exc:
            if attempt == 1:
                raise AIEngineError(
                    "The AI returned invalid JSON after retrying. "
                    "Please try again."
                ) from exc

        except AIEngineError:
            if attempt == 1:
                raise AIEngineError(
                    "Could not generate a valid learning path after retrying. "
                    "Please try again."
                )

    raise AIEngineError("Could not generate a learning path.")