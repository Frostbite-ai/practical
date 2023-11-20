import re

def Rule(output, *patterns):
    """
    Create a rule that produces `output` if the entire input matches any one of the `patterns`.
    """
    return (output, [name_group(pat) + "$" for pat in patterns])

def name_group(pat):
    """
    Replace '{Q}' with '(?P<Q>.+?)', which means 'match 1 or more characters, and call it Q'.
    """
    return re.sub("{(.)}", r"(?P<\1>.+?)", pat)

def word(w):
    """
    Return a regex that matches w as a complete word (not letters inside a word).
    """
    return r"\b" + w + r"\b"  # '\b' matches at word boundary

# Define rules for various logical sentence structures
rules = [
    Rule("{P} ⇒ {Q}", "if {P} then {Q}", "if {P}, {Q}"),
    # ... (other rules)
    Rule("～{Q} ⇒ {P}", "{P} unless {Q}"),
    # ... (more rules)
]

# Define negations and their replacements
negations = [
    (word("not"), ""),
    # ... (other negations)
    ("n't", ""),  # matches as part of a word: didn't, couldn't, etc.
]

def match_rules(sentence, rules, defs):
    """
    Match sentence against all the rules, or make it an atom if no rule matches.
    """
    sentence = clean(sentence)
    for rule in rules:
        result = match_rule(sentence, rule, defs)
        if result:
            return result
    return match_literal(sentence, negations, defs)

def match_rule(sentence, rule, defs):
    """
    Match a sentence with a rule and return the logic translation if the match succeeds.
    """
    output, patterns = rule
    for pat in patterns:
        match = re.match(pat, sentence, flags=re.I)
        if match:
            groups = match.groupdict()
            for P in sorted(groups):
                groups[P] = match_rules(groups[P], rules, defs)[0]
            return "(" + output.format(**groups) + ")", defs

def match_literal(sentence, negations, defs):
    """
    Treat the sentence as an atom if no rule matches, and handle negation.
    """
    polarity = ""
    for neg, pos in negations:
        (sentence, n) = re.subn(neg, pos, sentence, flags=re.I)
        polarity += n * "～"
    sentence = clean(sentence)
    P = proposition_name(sentence, defs)
    defs[P] = sentence
    return polarity + P, defs

def proposition_name(sentence, defs, names="PQRSTUVWXYZBCDEFGHJKLMN"):
    """
    Return the old name for this sentence, or a new, unused name.
    """
    inverted = {defs[P]: P for P in defs}
    if sentence in inverted:
        return inverted[sentence]
    else:
        return next(P for P in names if P not in defs)

def clean(text):
    """
    Clean the text by removing extra whitespace and handling punctuation.
    """
    return " ".join(text.split()).replace("’", "'").rstrip(".").rstrip(",")

# Example usage
sentences = [
    "Either today is Sunday or Monday.",
    "I will dance only if you sing.",
    # ... (other sentences)
]

def logic(sentences):
    """
    Apply the logic rules to each sentence and print the results.
    """
    for s in sentences:
        logic, defs = match_rules(s, rules, {})
        print("\nEnglish: ", s, "\nLogic:", logic)
        for P in sorted(defs):
            print("{}: {}".format(P, defs[P]))

logic(sentences)
