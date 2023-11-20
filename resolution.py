import re


def Rule(output, *patterns):
    "A rule that produces `output` if the entire input matches any one of the `patterns`."
    return (output, [name_group(pat) + "$" for pat in patterns])


def name_group(pat):
    "Replace '{Q}' with '(?P<Q>.+?)', which means 'match 1 or more characters, and call it Q'"
    return re.sub("{(.)}", r"(?P<\1>.+?)", pat)


def word(w):
    "Return a regex that matches w as a complete word (not letters inside a word)."
    return r"\b" + w + r"\b"  # '\b' matches at word boundary


rules = [
    Rule("{P} ⇒ {Q}", "if {P} then {Q}", "if {P}, {Q}"),
    Rule("{P} ⋁ {Q}", "either {P} or else {Q}", "either {P} or {Q}"),
    Rule("{P} ⋀ {Q}", "both {P} and {Q}"),
    Rule("～{P} ⋀ ～{Q}", "neither {P} nor {Q}"),
    Rule("～{A}{P} ⋀ ～{A}{Q}", "{A} neither {P} nor {Q}"),  # The Kaiser neither ...
    Rule("～{Q} ⇒ {P}", "{P} unless {Q}"),
    Rule(
        "{P} ⇒ {Q}",
        "{Q} provided that {P}",
        "{Q} whenever {P}",
        "{P} implies {Q}",
        "{P} therefore {Q}",
        "{Q}, if {P}",
        "{Q} if {P}",
        "{P} only if {Q}",
    ),
    Rule("{P} ⋀ {Q}", "{P} and {Q}", "{P} but {Q}"),
    Rule("{P} ⋁ {Q}", "{P} or else {Q}", "{P} or {Q}"),
]

negations = [
    (word("not"), ""),
    (word("cannot"), "can"),
    (word("can't"), "can"),
    (word("won't"), "will"),
    (word("ain't"), "is"),
    ("n't", ""),  # matches as part of a word: didn't, couldn't, etc.
]


def match_rules(sentence, rules, defs):
    """Match sentence against all the rules, accepting the first match; or else make it an atom.
    Return two values: the Logic translation and a dict of {P: 'english'} definitions.
    """
    sentence = clean(sentence)
    for rule in rules:
        result = match_rule(sentence, rule, defs)
        if result:
            return result
    return match_literal(sentence, negations, defs)


def match_rule(sentence, rule, defs):
    "Match rule, returning the logic translation and the dict of definitions if the match succeeds."
    output, patterns = rule
    for pat in patterns:
        match = re.match(pat, sentence, flags=re.I)
        if match:
            groups = match.groupdict()
            for P in sorted(
                groups
            ):  # Recursively apply rules to each of the matching groups
                groups[P] = match_rules(groups[P], rules, defs)[0]
            return "(" + output.format(**groups) + ")", defs


def match_literal(sentence, negations, defs):
    "No rule matched; sentence is an atom. Add new proposition to defs. Handle negation."
    polarity = ""
    for neg, pos in negations:
        (sentence, n) = re.subn(neg, pos, sentence, flags=re.I)
        polarity += n * "～"
    sentence = clean(sentence)
    P = proposition_name(sentence, defs)
    defs[P] = sentence
    return polarity + P, defs


def proposition_name(sentence, defs, names="PQRSTUVWXYZBCDEFGHJKLMN"):
    "Return the old name for this sentence, if used before, or a new, unused name."
    inverted = {defs[P]: P for P in defs}
    if sentence in inverted:
        return inverted[sentence]  # Find previously-used name
    else:
        return next(P for P in names if P not in defs)  # Use a new unused name


def clean(text):
    "Remove redundant whitespace; handle curly apostrophe and trailing comma/period."
    return " ".join(text.split()).replace("’", "'").rstrip(".").rstrip(",")


sample_sentences = """
Polkadots and Moonbeams.
If you liked it then you shoulda put a ring on it.
If you build it, he will come.
It don't mean a thing, if it ain't got that swing.
If loving you is wrong, I don't want to be right.
Should I stay or should I go.
I shouldn't go and I shouldn't not go.
If I fell in love with you,
  would you promise to be true
  and help me understand.
I could while away the hours
  conferrin' with the flowers,
  consulting with the rain
  and my head I'd be a scratchin'
  while my thoughts are busy hatchin'
  if I only had a brain.
There's a federal tax, and a state tax, and a city tax, and a street tax, and a sewer tax.
A ham sandwich is better than nothing 
  and nothing is better than eternal happiness
  therefore a ham sandwich is better than eternal happiness.
If I were a carpenter
  and you were a lady,
  would you marry me anyway?
  and would you have my baby.
Either Danny didn't come to the party or Virgil didn't come to the party.
Either Wotan will triumph and Valhalla will be saved or else he won't and Alberic will have 
  the final word.
Sieglinde will survive, and either her son will gain the Ring and Wotan’s plan 
  will be fulfilled or else Valhalla will be destroyed.
Wotan will intervene and cause Siegmund's death unless either Fricka relents 
  or Brunnhilde has her way.
Figaro and Susanna will wed provided that either Antonio or Figaro pays and Bartolo is satisfied 
  or else Marcellina’s contract is voided and the Countess does not act rashly.
If the Kaiser neither prevents Bismarck from resigning nor supports the Liberals, 
  then the military will be in control and either Moltke's plan will be executed 
  or else the people will revolt and the Reich will not survive"""


sentences = """
Either today is Sunday or Monday.
I will dance only if you sing.
If the Kaiser neither prevents Bismarck from resigning nor supports the Liberals, 
  then the military will be in control and either Moltke's plan will be executed 
  or else the people will revolt and the Reich will not survive
""".split(
    "."
)

import textwrap


def logic(sentences, width=80):
    "Match the rules against each sentence in text, and print each result."
    for s in map(clean, sentences):
        logic, defs = match_rules(s, rules, {})
        print("\n" + textwrap.fill("English: " + s + ".", width), "\n\nLogic:", logic)
        for P in sorted(defs):
            print("{}: {}".format(P, defs[P]))


logic(sentences)
