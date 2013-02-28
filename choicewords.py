import re
from random import seed as _seed, choice

VARIABLE_TAG_START = '{{'
VARIABLE_TAG_END = '}}'

tag_re = re.compile('(%s.*?%s)' % (re.escape(VARIABLE_TAG_START), re.escape(VARIABLE_TAG_END)))


def choice_words(phrase_book, root_key='root', seed=None):
    if isinstance(seed, int):
        seed = str(seed << 10)
    _seed(seed)
    return eval_phrase(phrase_book, lookup_phrase(root_key, phrase_book))


def apply_filters(s, filters):
    for f in filters:
        if f == 'upper':
            s = s.upper()
        elif f == 'lower':
            s = s.lower()
        elif f == 'title':
            s = s.title()
    return s


def eval_phrase(phrase_book, phrase):
    s = ""
    for token in tokenize(phrase):
        if token.token_type == TOKEN_TEXT:
            s += token.text
        else:
            phrase = lookup_phrase(token.text, phrase_book)
            text = eval_phrase(phrase_book, phrase)
            s += apply_filters(text, token.filters)
    return s

TOKEN_TEXT = 'text'
TOKEN_REF = 'ref'


class Token(object):

    def __init__(self, text, token_type):
        self.token_type = token_type
        if token_type == TOKEN_REF:
            text_without_tags = text[2:-2].strip()
            text_and_filters = text_without_tags.split('|')
            self.text = text_and_filters[0]
            self.filters = text_and_filters[1:]
        else:
            self.text = text


def tokenize(phrase):
    result = []
    in_tag = False
    for part in tag_re.split(phrase):
        if part:
            token_type = TOKEN_REF if in_tag else TOKEN_TEXT
            result.append(Token(part, token_type))
        in_tag = not in_tag
    return result


def lookup_phrase(phrase_key, phrase_book):
    v = phrase_book.get(phrase_key)
    if v is None:
        raise ValueError('Could not find phrase with key "%s".' % phrase_key)
    assert isinstance(v, list)
    return choice(v)


def parse_phrase_book(fname):
    phrases = []
    current_phrase = None
    for line_number, line in enumerate(open(fname).readlines()):
        line = line.strip()
        if line.startswith('#'):
            # Ignore lines with comments.
            continue
        elif len(line) == 0:
            # Empty lines reset the phrase.
            current_phrase = None
        elif line.startswith('- '):
            # Phrases are prefixed with "- ".
            if current_phrase is None:
                raise ValueError("%s: line without a key." % line_number)
            else:
                current_phrase['values'].append(line[2:].strip())
        elif line.endswith(':'):
            # Keys end with ":"
            current_phrase = {'key': line[:-1], 'values': []}
            phrases.append(current_phrase)
        else:
            raise ValueError('%s: do not know what to do with line "%s".' % (line_number, line))
    phrase_book = {}
    for phrase in phrases:
        phrase_book[phrase['key']] = phrase['values']
    return phrase_book


def from_file(fname, root_key='root', seed=None):
    phrase_book = parse_phrase_book(fname)
    return choice_words(phrase_book, root_key, seed)


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage='Usage: %prog [options] <phrasebook_file>')
    parser.add_option('-r', '--root', help='the root key', default='root')
    parser.add_option('-s', '--seed', help='random seed index')
    parser.add_option('-n', '--amount', help='number of lines to generate', type="int", default=1)
    option, args = parser.parse_args()
    if len(args) == 1:
        for i in range(option.amount):
            print from_file(args[0], root_key=option.root, seed=option.seed)
    else:
        parser.print_help()
