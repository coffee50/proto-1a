import random
import langlogic

SYNONYM_MAP = {
    "hej": "hey",
    "yeah": "yes",
    "yes": "yeah",
    "yo": "hi",
    "sup": "hi",
    "hey": "sup",
    "hi": "hello",
    "yea": "yes",
    "yep": "yes",
    "no": "no",
    "the": "a",
    "a": "the",
    "da": "the",
    "nah": "no",
    "nop": "no",
    "okay": "ok",
    "ok": "ok",
    "u": "you",
    "alright": "ok",
    "hello": "hi",
    "sure": "ok",
    "fine": "ok",
    "dont": "don't",
    "do not": "don't",
    "don't": "don't",
    "didnt": "didn't",
    "did not": "didn't",
    "didn't": "didn't",
    "wont": "won't",
    "shouldnt": "shouldn't",
    "couldnt": "couldn't",
    "wouldnt": "wouldn't",
    "hasnt": "hasn't",
    "havent": "haven't",
    "hadnt": "hadn't",
    "isnt": "isn't",
    "arent": "aren't",
    "wasnt": "wasn't",
    "werent": "weren't",
    "thats": "that's",
    "whats": "what's",
    "heres": "here's",
    "theres": "there's",
    "wheres": "where's",
    "im": "I'm",
    "youre": "you're",
    "theyre": "they're",
    "won't": "wont",
    "shouldn't": "shouldnt",
    "couldn't": "couldnt",
    "wouldn't": "wouldnt",
    "hasn't": "hasnt",
    "haven't": "havent",
    "hadn't": "hadnt",
    "isn't": "isnt",
    "aren't": "arent",
    "wasn't": "wasnt",
    "weren't": "werent",
    "that's": "thats",
    "what's": "whats",
    "here's": "heres",
    "there's": "theres",
    "where's": "wheres",
    "I'm": "im",
    "you're": "youre",
    "they're": "theyre",
    "aight": "alright",
    "lets": "let's",
    "let's": "let's",
    "bro": "you",
    "fuck": "bad",
    "who": "someone",
    "did": "do",
    "broski": "bro",
    "zverev": "nikita",
    "nikita": "zverev",
    "osama": "laden",
    "kulkov": "kulkoff",
    "kulkoff": "kulkov",
    "egor": "kvadratev",
    "happy": "joyful",
    "sad": "dejected",
    "big": "large",
    "small": "tiny",
    "good": "excellent",
    "bad": "terrible",
    "hot": "scorching",
    "cold": "freezing",
    "funny": "hilarious",
    "scary": "terrifying",
    "easy": "simple",
    "hard": "difficult",
    "new": "fresh",
    "old": "ancient",
    "start": "begin",
    "end": "finish",
    "love": "adore",
    "hate": "despise",
    "friend": "companion",
    "enemy": "foe",
    "smart": "intelligent",
    "dumb": "foolish",
    "brave": "courageous",
    "scared": "fearful",
    "pretty": "beautiful",
    "ugly": "hideous",
    "human": "person",
    "person": "human",
    "individual": "person",
    "you": "yourself",
    "yourself": "you",
    "brother": "dude",
    "dude": "bro",
    "buddy": "pal",
    "comrade": "buddy",
    "cheerful": "happy",
    "gloomy": "sad",
    "huge": "big",
    "little": "small",
    "great": "good",
    "awful": "bad",
    "boiling": "hot",
    "icy": "cold",
    "amusing": "funny",
    "frightening": "scary",
    "effortless": "easy",
    "challenging": "hard",
    "brand-new": "new",
    "aged": "old",
    "commence": "start",
    "conclude": "end",
    "cherish": "love",
    "loathe": "hate",
    "brilliant": "smart",
}


def standardize_word(word):
    word = SYNONYM_MAP.get(word.lower(), word)
    return langlogic.standardize_word(word)


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


def generate_response(model, user_input, max_length=50, stop_threshold=0.05):
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
