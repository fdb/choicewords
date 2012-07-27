import re
from random import seed, choice, randint

VARIABLE_TAG_START = '{{'
VARIABLE_TAG_END = '}}'

tag_re = re.compile('(%s.*?%s)' %
        (re.escape(VARIABLE_TAG_START), re.escape(VARIABLE_TAG_END)))

def choice_words(phrase_dict, root_key='root', variation=None):
    if variation is None:
        variation = randint(0, 9999999)
    return eval_phrase(phrase_dict, phrase_dict[root_key], variation)

def eval_phrase(phrase_dict, phrase, variation):
    s = ""
    for token in tokenize(phrase):
        if not token.in_tag:
            s += token.text
        else:
            s += lookup_phrase(token.text, phrase_dict, variation)

    return s

class Token(object):

    def __init__(self, text, in_tag):
        self.in_tag = in_tag
        if in_tag:
            self.text = text[2:-2].strip()
        else:
            self.text = text

def tokenize(phrase):
    result = []
    in_tag = False
    for part in tag_re.split(phrase):
        if part:
            result.append(Token(part, in_tag))
        in_tag = not in_tag
    return result

def lookup_phrase(phrase_key, phrase_dict, variation):
    v = phrase_dict[phrase_key]
    if isinstance(v, list):  
        seed(variation)
        return choice(v)
    else:
        return v

def thank_you_note(variation=None):
    d = {
        "root": "Dear {{ giver }}, {{ thanks }} for the {{ object }}. It {{ rationale }} when {{ event }}. {{ salutations }}, {{ receiver }}.",
        "giver": ["Aunt Emma", "Dave and Edna", "Uncle Bob"],
        "thanks": ["thank you", "my greatest thanks"],
        "object": ["purple vase", "golden retriever", "dishwasher"],
        "rationale": ["came in handy", "proved necessary", "was useful"],
        "event": ["the house burned down", "the cat vomitted", "our baby was born", "my bike was stolen"],
        "salutations": ["Kind regards", "Best regards", "All the best", "Love"],
        "receiver": ["David", "God", "Emmy", "Stan", "Your son"]
        }
    return choice_words(d, 'root')

if __name__=='__main__':
    print thank_you_note()
