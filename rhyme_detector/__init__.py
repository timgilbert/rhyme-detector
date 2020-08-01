import pronouncing as p
import re
from typing import List, Dict

__version__ = "0.1.0"


def main():
    print("Hello, world!")

frost = "Whose woods these are I think I know / His house is in the forest though."


class Word(object):
    def __init__(self, word):
        self.word = word
        self.phones = [Phone(ph) for ph in p.phones_for_word(self.word)]

    def __repr__(self):
        #return (f"<Word '{self.word}' phones {self.phones}>")
        return (f"<Word '{self.word}' ({len(self.phones)})>")

    def rhymes(self, other: 'Word') -> float:
        matches = [mine.rhymes(theirs) for mine in self.phones for theirs in other.phones]
        return (len([m for m in matches if m]) * 1.0 / len(matches))


class Phone(object):
    def __init__(self, phone: str):
        self.phone = phone
        self.rhyming_part = re.sub(r'\d', '', p.rhyming_part(self.phone))
        self.stresses = p.stresses(self.phone)
        self.syllable_count = p.syllable_count(self.phone)

    def __repr__(self) -> str:
        return (f"<Phone '{self.phone}' ({self.syllable_count}), "
                f"rhyme {self.rhyming_part}, stresses {self.stresses}>")

    def rhymes(self, other: 'Phone') -> bool:
        return self.rhyming_part == other.rhyming_part


def rhymes(words: List[str]) -> bool:
    lastphrase_a = words[0].split()[-1]
    lastphrase_b = words[1].split()[-1]
    return lastphrase_b in p.rhymes(lastphrase_a)


def __line(words: List[Word]) -> str:
    return ' '.join((w.word for w in words))


def enjamb(text: str) -> List[str]:
    words = [Word(w) for w in re.sub(r"[^\w ']", '', text).split()]
    total = len(words)
    final = words[-1]
    mdict = {i: final.rhymes(words[i])
             for i in range(total - 1)
             if final.rhymes(words[i]) > 0.0}
    if len(mdict) == 1:
        split = list(mdict)[0] + 1
        return [__line(words[0:split]), __line(words[split:])]
    return [__line(words)]


def is_couplet(text: str) -> bool:
    return len(enjamb(text)) == 2


def hmm():
    for line in ["My beautiful Annabel Lee"]:
        print([Word(w) for w in line.split()])


if __name__ == "__main__":    main()
