import requests
from src import config


def get_all_tags(jwt_token=""):
    headers = {"Authorization": f"Bearer {jwt_token}"} if jwt_token else {}
    response = requests.get(f"{config.API_BASE_URL}/tags", headers=headers)
    data = response.json()
    return data


def preprocess(prompt, chat_history, jwt_token=""):
    tags = get_all_tags(jwt_token)

    found_tags = []
    found_tag_ids = set()

    for tag in tags:
        tag_label = tag.get("label", "")
        tag_id = tag.get("_id", "")

        if not tag_label or not tag_id:
            continue

        tag_found = False

        if tag_label.lower() in prompt.lower():
            tag_found = True

        if chat_history:
            for message in chat_history:
                message_content = getattr(message, "content", "") or ""
                if tag_label.lower() in message_content.lower():
                    tag_found = True
                    break

        if tag_found and tag_id not in found_tag_ids:
            found_tags.append({"label": tag_label, "id": tag_id})
            found_tag_ids.add(tag_id)

    result = prompt

    if found_tags:
        result += "\n\nPreprocessor:\n"
        for tag in found_tags:
            result += f"{tag['label']} is a tag with _id: {tag['id']}\n"

    return result
