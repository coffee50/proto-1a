import re
import random

POS_MAP = {
    r'ing$': 'verb',
    r'tion$': 'noun',
    r'ness$': 'noun',
    r'ly$': 'adverb',
    r'ful$': 'adjective',
    r'less$': 'adjective',
    r'able$': 'adjective',
    r'ible$': 'adjective',
    r'ive$': 'adjective',
    r'ic$': 'adjective',
    r'ed$': 'verb',
    r's$': 'noun',
    r'': 'noun'
}


def identify_pos(word):
    for ending, pos in POS_MAP.items():
        if re.search(ending, word, re.IGNORECASE):
            return pos
    return POS_MAP['']


def standardize_word(word):
    return identify_pos(word), word


def train_model(text, model):
    lines = text.split('\n')
    for line in lines:
        words = line.split()
        if words:
            pos, word = standardize_word(words[0])
            model.start_words.append((pos, word))
            for i in range(len(words) - 1):
                current_pos, current_word = standardize_word(words[i])
                next_pos, next_word = standardize_word(words[i + 1])
                model.ngram_counts[current_pos][current_word][next_pos][next_word] += 1


def generate_word(model, current_pos, current_word, exclude_words):
    if current_pos not in model.ngram_counts or current_word not in model.ngram_counts[current_pos]:
        return random.choice(model.start_words)
    next_pos_counts = model.ngram_counts[current_pos][current_word]
    next_pos = random.choice(list(next_pos_counts.keys()))
    next_words = list(next_pos_counts[next_pos].elements())
    next_words = [word for word in next_words if word not in exclude_words]
    if not next_words:
        return random.choice(model.start_words)
    return next_pos, random.choice(next_words)


def generate_response(model, user_input, max_length=25, stop_threshold=0.1):
    user_words = set(standardize_word(word) for word in user_input.split())
    words = user_input.split()
    if words:
        current_pos, current_word = standardize_word(words[-1])
    else:
        current_pos, current_word = random.choice(model.start_words)
    response = [current_word]
    for _ in range(max_length - 1):
        next_pos, next_word = generate_word(model, current_pos, current_word, user_words)
        if random.random() < stop_threshold or (next_pos, next_word) in model.start_words:
            break
        response.append(next_word)
        current_pos, current_word = next_pos, next_word
    return ' '.join(response)
