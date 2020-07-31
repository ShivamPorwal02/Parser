import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP| NP VP PP | DetP VP| NP AdvP VP
VP -> V| V DetP|V PP| V AdvP |V NP| V AdjP
NP -> N
DetP -> Det|Det NP | Det AdjP | NP AdvP | Det NP AdvP 
PP -> P| P NP| P DetP | P NP ConjP|P DetP PP
AdjP ->  Adj| Adj NP ConjP | Adj NP | Adj VP| Adj AdjP
ConjP -> Conj NP VP | Conj NP | Conj VP|Conj VP PP
AdvP -> Adv|Adv VP ConjP | Adv ConjP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()
        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            #print(np)
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    contents = []
    contents.extend(
        word.lower() for word in
        nltk.word_tokenize(sentence)
        if any(c.isalpha() for c in word)
    )

    return contents


def np_chunk(tree):
    #print(tree.subtrees)
    
    #return []
    lst = []
    if tree.label() == "N":
        lst.append(tree.copy(True))

    for node in tree:
        if not type(node) is type(str()):
            rt_lst = np_chunk(node)
            lst.extend(rt_lst)

    return lst
  
    
"""def chunk(tree,height,res=[]):
    if height==0:
        return res
    else:
        if tree.label()=='VP':
            res.append('shivam')
        for tree in tree.subtrees():
            tree=chunk(tree,height-1,res)
    return res
    """
if __name__ == "__main__":
    main()
