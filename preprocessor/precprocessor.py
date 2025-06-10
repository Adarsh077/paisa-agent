import requests
import config

def get_all_tags():
    response = requests.get(f"{config.API_BASE_URL}/tags")
    data = response.json()
    return data


def preprocess(prompt, chat_history):
    tags = get_all_tags()

    # Find tags mentioned in the prompt and chat_history
    found_tags = []
    found_tag_ids = set()  # To avoid duplicates
    
    for tag in tags:
        tag_label = tag.get('label', '')
        tag_id = tag.get('_id', '')
        
        if not tag_label or not tag_id:
            continue
            
        tag_found = False
        
        # Search for tag label in prompt (case-insensitive)
        if tag_label.lower() in prompt.lower():
            tag_found = True
        
        # Search for tag label in chat_history (case-insensitive)
        if chat_history:
            for message in chat_history:
                message_content = getattr(message, 'content', '') or ''
                if tag_label.lower() in message_content.lower():
                    tag_found = True
                    break
        
        # Add tag if found and not already added
        if tag_found and tag_id not in found_tag_ids:
            found_tags.append({
                'label': tag_label,
                'id': tag_id
            })
            found_tag_ids.add(tag_id)

    # Format output
    result = prompt

    if found_tags:
        result += "\n\nPreprocessor:\n"
        for tag in found_tags:
            result += f"{tag['label']} is a tag with _id: {tag['id']}\n"

    return result
