# To the extent possible under law, the person who associated CC0 with
# this project has waived all copyright and related or neighboring rights
# to this project.

# You should have received a copy of the CC0 legalcode along with this
# work. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

from sys import argv

from parser import Parser

parser = Parser()

parser.add_token(r":=")
parser.add_token(r"print")
parser.add_token(r"\\/")
parser.add_token(r"/\\")
parser.add_token(r"!=")
parser.add_token(r"<=")
parser.add_token(r">=")
parser.add_token(r"<<")
parser.add_token(r">>")

parser.add_token(r";")
parser.add_token(r"=")
parser.add_token(r"<")
parser.add_token(r">")
parser.add_token(r"\+")
parser.add_token(r"-")
parser.add_token(r"\*")
parser.add_token(r"/")
parser.add_token(r"\^")
parser.add_token(r"[0-9]+")
parser.add_token(r"[a-z]+")
parser.add_token(r"\(")
parser.add_token(r"\)")

parser.add_rule("B", [r"^", "C", r"$"])

parser.add_rule("C", ["S", r";"])
parser.add_rule("C", ["S", r";", "C"])

parser.add_rule("S", [r"[a-z]+", r":=", "E"])
parser.add_rule("S", [r"print", "E"])

parser.add_rule("E", ["E1"])
parser.add_rule("E", ["E", r"\\/", "E1"])

parser.add_rule("E1", ["E2"])
parser.add_rule("E1", ["E1", r"/\\", "E2"])

parser.add_rule("E2", ["ES"])
parser.add_rule("E2", ["E2", r"=", "ES"])
parser.add_rule("E2", ["E2", r"=!", "ES"])
parser.add_rule("E2", ["E2", r"<", "ES"])
parser.add_rule("E2", ["E2", r"<=", "ES"])
parser.add_rule("E2", ["E2", r">", "ES"])
parser.add_rule("E2", ["E2", r">=", "ES"])

parser.add_rule("ES", ["E3"])
parser.add_rule("ES", ["ES", r"<<", "E3"])
parser.add_rule("ES", ["ES", r">>", "E3"])

parser.add_rule("E3", ["E4"])
parser.add_rule("E3", ["E3", r"\+", "E4"])
parser.add_rule("E3", ["E3", r"-", "E4"])

parser.add_rule("E4", ["E5"])
parser.add_rule("E4", ["E4", r"\*", "E5"])
parser.add_rule("E4", ["E4", r"/", "E5"])

parser.add_rule("E5", ["E6"])
parser.add_rule("E5", [r"\+", "E5"])
parser.add_rule("E5", [r"-", "E5"])

parser.add_rule("E6", ["E7"])
parser.add_rule("E6", ["E7", r"\^", "E6"])

parser.add_rule("E7", [r"[0-9]+"])
parser.add_rule("E7", [r"[a-z]+"])
parser.add_rule("E7", [r"\(", "E", r"\)"])

def evaluate(context, parse):
  if parse.nonterminal == "B" and len(parse.children) == 3:
    evaluate(context, parse.children[1])
  if parse.nonterminal == "C" and len(parse.children) == 2:
    evaluate(context, parse.children[0])
  if parse.nonterminal == "C" and len(parse.children) == 3:
    evaluate(context, parse.children[0])
    evaluate(context, parse.children[2])
  if parse.nonterminal == "S" and len(parse.children) == 3:
    context[parse.children[0].children] = evaluate(context, parse.children[2])
  if parse.nonterminal == "S" and len(parse.children) == 2:
    print(evaluate(context, parse.children[1]))
  if parse.nonterminal == "E" and len(parse.children) == 1:
    return evaluate(context, parse.children[0])
  if parse.nonterminal == "E" and len(parse.children) == 3 and parse.children[1].nonterminal == r"\\/":
    return evaluate(context, parse.children[0]) or evaluate(context, parse.children[2])
  if parse.nonterminal == "E1" and len(parse.children) == 1:
    return evaluate(context, parse.children[0])
  if parse.nonterminal == "E1" and len(parse.children) == 3 and parse.children[1].nonterminal == r"/\\":
    return evaluate(context, parse.children[0]) and evaluate(context, parse.children[2])
  if parse.nonterminal == "E2" and len(parse.children) == 1:
    return evaluate(context, parse.children[0])
  if parse.nonterminal == "E2" and len(parse.children) == 3 and parse.children[1].nonterminal == r"=":
    return 1 if evaluate(context, parse.children[0]) == evaluate(context, parse.children[2]) else 0
  if parse.nonterminal == "E2" and len(parse.children) == 3 and parse.children[1].nonterminal == r"!=":
    return evaluate(context, parse.children[0]) - evaluate(context, parse.children[2])
  if parse.nonterminal == "E2" and len(parse.children) == 3 and parse.children[1].nonterminal == r"<":
    return 1 if evaluate(context, parse.children[0]) < evaluate(context, parse.children[2]) else 0
  if parse.nonterminal == "E2" and len(parse.children) == 3 and parse.children[1].nonterminal == r"<=":
    return 1 if evaluate(context, parse.children[0]) <= evaluate(context, parse.children[2]) else 0
  if parse.nonterminal == "E2" and len(parse.children) == 3 and parse.children[1].nonterminal == r">":
    return 1 if evaluate(context, parse.children[0]) > evaluate(context, parse.children[2]) else 0
  if parse.nonterminal == "E2" and len(parse.children) == 3 and parse.children[1].nonterminal == r">=":
    return 1 if evaluate(context, parse.children[0]) >= evaluate(context, parse.children[2]) else 0
  if parse.nonterminal == "ES" and len(parse.children) == 1:
    return evaluate(context, parse.children[0])
  if parse.nonterminal == "ES" and len(parse.children) == 3 and parse.children[1].nonterminal == r"<<":
    return evaluate(context, parse.children[0]) << evaluate(context, parse.children[2])
  if parse.nonterminal == "ES" and len(parse.children) == 3 and parse.children[1].nonterminal == r">>":
    return evaluate(context, parse.children[0]) >> evaluate(context, parse.children[2])
  if parse.nonterminal == "E3" and len(parse.children) == 1:
    return evaluate(context, parse.children[0])
  if parse.nonterminal == "E3" and len(parse.children) == 3 and parse.children[1].nonterminal == r"\+":
    return evaluate(context, parse.children[0]) + evaluate(context, parse.children[2])
  if parse.nonterminal == "E3" and len(parse.children) == 3 and parse.children[1].nonterminal == r"-":
    return evaluate(context, parse.children[0]) - evaluate(context, parse.children[2])
  if parse.nonterminal == "E4" and len(parse.children) == 1:
    return evaluate(context, parse.children[0])
  if parse.nonterminal == "E4" and len(parse.children) == 3 and parse.children[1].nonterminal == r"\*":
    return evaluate(context, parse.children[0]) * evaluate(context, parse.children[2])
  if parse.nonterminal == "E4" and len(parse.children) == 3 and parse.children[1].nonterminal == r"/":
    return evaluate(context, parse.children[0]) // evaluate(context, parse.children[2])
  if parse.nonterminal == "E5" and len(parse.children) == 1:
    return evaluate(context, parse.children[0])
  if parse.nonterminal == "E5" and len(parse.children) == 2 and parse.children[0].nonterminal == r"\+":
    return evaluate(context, parse.children[1])
  if parse.nonterminal == "E5" and len(parse.children) == 2 and parse.children[0].nonterminal == r"-":
    return -evaluate(context, parse.children[1])
  if parse.nonterminal == "E6" and len(parse.children) == 1:
    return evaluate(context, parse.children[0])
  if parse.nonterminal == "E6" and len(parse.children) == 3 and parse.children[1].nonterminal == r"\^":
    return evaluate(context, parse.children[0]) ** evaluate(context, parse.children[2])
  if parse.nonterminal == "E7" and len(parse.children) == 1:
    return evaluate(context, parse.children[0])
  if parse.nonterminal == "E7" and len(parse.children) == 3:
    return evaluate(context, parse.children[1])
  if parse.nonterminal == r"[0-9]+":
    return int(parse.children)
  if parse.nonterminal == r"[a-z]+":
    return context[parse.children]

if len(argv) < 2:
  print("python example.py example")
  quit()

file = open(argv[1], "r", encoding = "utf-8")

if not file:
  print("Unable to open file")
  quit()

parses = parser.parse(file.read())

if len(parses) != 1:
  print("Parse error")
  quit()

evaluate({}, parses[0])
