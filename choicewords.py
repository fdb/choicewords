import re
from random import seed, choice, randint

VARIABLE_TAG_START = '{{'
VARIABLE_TAG_END = '}}'

tag_re = re.compile('(%s.*?%s)' %
        (re.escape(VARIABLE_TAG_START), re.escape(VARIABLE_TAG_END)))

def choice_words(phrase_dict, root_key='root', variation=None):
    if variation is None:
        variation = randint(0, 9999999)
    return eval_phrase(phrase_dict, lookup_phrase(root_key, phrase_dict, variation), variation)

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
    v = phrase_dict.get(phrase_key)
    if v is None:
        raise ValueError('Could not find phrase with key "%s".' % phrase_key)
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

def parse_grammar_file(fname):
    phrases = []
    current_phrase = None 
    for line_number, line in enumerate(open(fname).readlines()):
        line = line.rstrip()
        if line.strip().startswith('#'):
            # Ignore lines with comments.
            continue
        elif len(line.strip()) == 0:
            # Empty lines reset the phrase.
            current_phrase = None
        elif line.startswith('  '):
            # Phrases are indented
            if current_phrase is None:
                raise ValueError("%s: Line without a key." % line_number)
            else:
                current_phrase['values'].append(line.strip())
        elif line.endswith(':'):
            # Keys end with ":"
              current_phrase = {'key':line[:-1], 'values': []}
              phrases.append(current_phrase)
        else:
            raise ValueError('%s: Do not know what to do with line "%s".' % (line_number, line))
    phrase_dict = {}
    for phrase in phrases:
        phrase_dict[phrase['key']] = phrase['values']
    return phrase_dict

def from_file(fname, root_key='root', variation=None):
    phrases = parse_grammar_file(fname)
    return choice_words(phrases, root_key)

#if __name__=='__main__':
#    import sys
#    print from_file(sys.argv[1])
