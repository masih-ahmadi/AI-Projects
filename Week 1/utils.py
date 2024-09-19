def deescalate_text(text):
    # Simple replacement for demo purposes
    replacements = {'badword': '****', 'toxic': 'non-toxic'}
    words = text.split()
    cleaned_words = [replacements.get(word.lower(), word) for word in words]
    return ' '.join(cleaned_words)

def identify_target(text):
    # Dummy target identification for demo
    if "you" in text.lower():
        return "individual"
    elif "group" in text.lower():
        return "group"
    else:
        return "unknown"
