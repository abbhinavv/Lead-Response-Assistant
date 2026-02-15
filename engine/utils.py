def contains_any(text, keywords):
    text = text.lower()
    return any(keyword in text for keyword in keywords)
