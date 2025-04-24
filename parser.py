# To the extent possible under law, the person who associated CC0 with
# this project has waived all copyright and related or neighboring rights
# to this project.

# You should have received a copy of the CC0 legalcode along with this
# work. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

from re import finditer, search

class Parse:
  def __init__(self, nonterminal, children):
    self.nonterminal = nonterminal
    self.children = children

  def __repr__(self):
    return "Parse(" + repr(self.nonterminal) + ", " + repr(self.children) + ")"

  def __str__(self):
    if type(self.children) is str:
      return "{" + self.nonterminal + ", " + str(self.children) + "}"
    else:
      return "{" + self.nonterminal + ", " + ", ".join(str(child) for child in self.children) + "}"

class Parser:
  def __init__(self):
    self.tokens = []
    self.rules = {}
    self.initialized = False

  def add_rule(self, nonterminal, pattern):
    assert pattern
    node = {"table": self.rules}
    for symbol in pattern[:: -1]:
      if symbol not in node["table"]:
        node["table"][symbol] = {"table": {}}
      node = node["table"][symbol]
    assert "nonterminal" not in node
    node["nonterminal"] = nonterminal
    self.initialized = False

  def add_token(self, token):
    self.tokens.append(token)
    self.initialized = False

  @staticmethod
  def find_rules(table, partial_parse, i):
    if -i > len(partial_parse) or partial_parse[i].nonterminal not in table:
      return []
    rules = [
      (nonterminal, length + 1)
      for nonterminal, length in Parser.find_rules(table[partial_parse[i].nonterminal]["table"], partial_parse, i - 1)]
    if "nonterminal" in table[partial_parse[i].nonterminal]:
      return rules + [(table[partial_parse[i].nonterminal]["nonterminal"], 1)]
    else:
      return rules

  def initialize(self):
    rules = Parser.list_rules(self.rules)
    self.precede = {}
    for token in self.tokens:
      self.precede[token] = set()
    for nonterminal, pattern in rules:
      self.precede[nonterminal] = set()
      for symbol in pattern:
        self.precede[symbol] = set()
    for nonterminal, pattern in rules:
      for i in range(1, len(pattern)):
        self.precede[pattern[i]].add(pattern[i - 1])
    size = 0
    new_size = sum(len(self.precede[symbol]) for symbol in self.precede)
    while new_size > size:
      for nonterminal, pattern in rules:
        self.precede[pattern[0]].update(self.precede[nonterminal])
      size = new_size
      new_size = sum(len(self.precede[nonterminal]) for nonterminal in self.precede)
    self.initialized = True

  @staticmethod
  def list_rules(table):
    return (
      [(nonterminal, pattern + [symbol]) for symbol in table for nonterminal, pattern in Parser.list_rules(table[symbol]["table"])] +
      [(table[symbol]["nonterminal"], [symbol]) for symbol in table if "nonterminal" in table[symbol]])

  def parse(self, string):
    # for symbol in self.precede:
    #   print(symbol, self.precede[symbol])
    # print()
    if not self.initialized:
      self.initialize()
    partial_parses = [[]]
    for token in self.tokenize(string):
      current_partial_parses = [partial_parse + [token] for partial_parse in partial_parses]
      partial_parses = []
      while current_partial_parses:
        new_partial_parses = [
          partial_parse[: -length] + [Parse(nonterminal, partial_parse[-length :])]
          for partial_parse in current_partial_parses
          for nonterminal, length in Parser.find_rules(self.rules, partial_parse, -1)]
        partial_parses = partial_parses + current_partial_parses
        current_partial_parses = new_partial_parses
      partial_parses = [
        partial_parse
        for partial_parse in partial_parses
        if len(partial_parse) < 2 or partial_parse[-2].nonterminal in self.precede[partial_parse[-1].nonterminal]]
      # print(len(partial_parses))
      # for partial_parse in partial_parses:
      #   print(", ".join(str(parse) for parse in partial_parse))
      # print()
    return [partial_parse[0] for partial_parse in partial_parses if len(partial_parse) == 1]

  def tokenize(self, string):
    yield Parse(r"^", "")
    for match in finditer(r"|".join(self.tokens) + r"|[ \n]+|.", string):
      if search(r"^(?:" + r"|".join(self.tokens) + r")$", match.group()):
        for regex in self.tokens:
          if search(r"^" + regex + r"$", match.group()):
            yield Parse(regex, match.group())
            break
      elif search(r"^[ \n]+$", match.group()):
        pass
      else:
        raise Exception()
    yield Parse(r"$", "")
