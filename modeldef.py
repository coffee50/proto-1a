from collections import defaultdict, Counter
import langalg
import random
import re

nnName = "Proto"
nnVer = "1A"
nnBuild = "1.5"
buildDate = "27/10/2024"

CAPITALIZE_RESPONSES = False


class Proto1A:
    def __init__(self):
        self.ngram_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(Counter)))
        self.start_words = []

    def train(self, text):
        langalg.train_model(text, self)

    def generate_word(self, current_pos, current_word, exclude_words):
        return langalg.generate_word(self, current_pos, current_word, exclude_words)

    def generate_response(self, user_input, max_length=50, stop_threshold=0.05):
        return langalg.generate_response(self, user_input, max_length, stop_threshold)


def is_question(user_input):
    user_input = user_input.strip()
    question_words = ["what", "who", "where", "when", "why", "how", "is", "are", "do",
                      "does", "did", "can", "could", "should", "would"]
    return user_input.endswith("?") or user_input.split()[0].lower() in question_words


def main():
    try:
        with open('tt.txt', 'r') as file:
            training_text = file.read()
        training_text = training_text.strip()
        model = Proto1A()
        model.train(training_text)
        print(f"{nnName} {nnVer} {nnBuild} from {buildDate}")
        print(f"{nnName}: Hi! You just started a new chat. Type 'exit' to exit.")
        while True:
            user_input = input("You: ").lower()
            user_input_math = ""
            for char in user_input:
                if char == ',':
                    user_input_math += '.'
                elif char == '.':
                    user_input_math += '.'
                else:
                    user_input_math += char
            math_match = re.match(r"^\s*[\d.]+(?:\s*[+\-*/=]\s*[\d.]+)+\s*$", user_input_math)
            non_latin_match = re.findall(r"[^\u0000-\u007F]+", user_input)
            response = model.generate_response(user_input, max_length=40, stop_threshold=0.05)
            if CAPITALIZE_RESPONSES:
                response = response.capitalize()
            else:
                response = response.lower()
            if user_input == "exit":
                print(f"{nnName}: Have a great day!")
                break
            if not user_input.strip():
                blank_responses = [
                    "i didn't quite catch that. Could you try again?",
                    "anything you'd like to say?",
                    "i'm ready when you are!",
                    "bro forgot to type something",
                    "anything you'd like to share?",
                    "type something to get started.",
                    "anything you'd like to share?",
                    "are you trying to say something?",
                    "i didn't catch that, try again?",
                    "what did you want to say?",
                    "did you say something?",
                    "is this the silent treatment?",
                    "words, use them!",
                    "oh.",
                    "i'm listening, what's up?",
                    "i'm ready when you are.",
                    "i'm ready to chat.",
                    "share your thoughts.",
                    "what's on your mind?",
                    "bro is learning to type",
                    "bro...",
                    "try again",
                    "i'm waiting for your input",
                    "you scared me to death.",
                    "i'm ready when you are",
                    "is this thing on? hello?"
                ]
                print(f"{nnName}: {random.choice(blank_responses)}")
            else:
                if len(user_input.strip()) <= 1 or (len(user_input.strip()) == 2 and user_input.strip()[-1] == '?'):
                    question_mark_responses = ["What do you want to know?",
                                               "What do you mean?",
                                               "I'm not sure what you're asking.",
                                               "feel free to ask anything.",
                                               "i'm here to listen you.",
                                               "ask me anything",
                                               "what",
                                               "what does this mean?",
                                               "i'm not sure I understand.",
                                               "i'm a bit confused.",
                                               "can you explain that in a different way?",
                                               "i'm not sure what you're asking me to do.",
                                               "i don't understand what you're trying to say.",
                                               "i'm having trouble processing your request.",
                                               "could you be more specific?",
                                               "i'm not quite sure what you mean."]
                    response = random.choice(question_mark_responses)
                    print(f"{nnName}: {response}")
                elif non_latin_match:
                    question_mark_responses = [
                        "What do you want to know?",
                        "What do you mean?",
                        "I'm not sure what you're asking.",
                        "feel free to ask anything.",
                        "i'm here to listen you.",
                        "ask me anything",
                        "what",
                        "what does this mean?",
                        "i'm not sure I understand.",
                        "i'm a bit confused.",
                        "can you explain that in a different way?",
                        "i'm not sure what you're asking me to do.",
                        "i don't understand what you're trying to say.",
                        "i'm having trouble processing your request.",
                        "could you be more specific?",
                        "i'm not quite sure what you mean."
                    ]
                    response = random.choice(question_mark_responses)
                    print(f"{nnName}: {response}")
                elif is_question(user_input):
                    if random.random() < 0.5:
                        question_responses = ["nice question. ", "good question. ", "okay, let me answer. ",
                                              "the answer is... ", "you asked, ", "so... ", "this is ", "that's "]
                        response = random.choice(question_responses) + model.generate_response(user_input,
                                                                                               max_length=40,
                                                                                               stop_threshold=0.05)
                    print(f"{nnName}: {response}")
                elif math_match:
                    try:
                        result = eval(user_input_math)
                        math_responses = [
                            f"that's {result}",
                            f"that would be {result}.",
                            f"the answer is {result}.",
                            f"{user_input} equals {result}.",
                            f"i suppose it's {result}",
                            f"it's {result}",
                            f"is {result}.",
                            f"it would be {result}"
                        ]
                        response = random.choice(math_responses)
                    except (SyntaxError, NameError, ZeroDivisionError):
                        math_error_responses = [
                            "I'm not sure how to calculate that.",
                            "The given math is incorrect.",
                            "Sorry, but I don't really understand how to calculate that."]
                        response = random.choice(math_error_responses)
                    print(f"{nnName}: {response}")
                else:
                    print(f"{nnName}: {response}")

    except FileNotFoundError:
        print("Error: the training file 'tt.txt' was not found. The chatbot won't work without it."
              "Please ensure it is in the same directory as this script or create a new one."
              "Note: the training text needs to be at least 4000 characters long for the model to work properly.")


if __name__ == "__main__":
    main()
