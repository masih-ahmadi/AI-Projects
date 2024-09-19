import re


def check_inclusion_of_characters(story, protagonist, friend):
    return protagonist.lower() in story.lower() and friend.lower() in story.lower()

def check_adherence_to_theme(story, theme):
    return any(word in story.lower() for word in theme.lower().split())

def contains_toxic_words(search_keywords):
    p = staticfiles_storage.path('bad_words.txt')
    content = open(p).readlines()[0]
    bad_words = content.split(",")
    for keyword in search_keywords:
        if keyword in bad_words:
            return True

    return False

def check_coherence(story):
    return "once upon a time" in story.lower() and "the end" in story.lower()

def check_tone_and_language(story):
    complex_words = re.findall(r'\b\w{10,}\b', story)
    return len(complex_words) < 5

def evaluate_story(story, protagonist, friend, theme):
    evaluations = {
        "inclusion_of_characters": check_inclusion_of_characters(story, protagonist, friend),
        "adherence_to_theme": check_adherence_to_theme(story, theme),
        "contains_toxic_words": not contains_toxic_words(story),
        "coherence_and_flow": check_coherence(story),
        "tone_and_language": check_tone_and_language(story)
    }

    is_valid = all(evaluations.values())
    return is_valid, evaluations
