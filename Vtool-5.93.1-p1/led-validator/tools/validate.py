import argparse

from tools.led.syntax import SyntaxValidator
from tools.led.structure import StructureValidator
from tools.led.semantics import SemanticsValidator

parser = argparse.ArgumentParser(description="Elsevier Linked Documents validator reference implementation")
parser.add_argument("document", help="Input LED document as HTML", nargs="+")
parser.add_argument("validator", help="HTML5 validator to use: tidy or NU html5validator. Requires ", nargs="?", default="tidy", choices=["tidy", "html5validator"])

if __name__ == '__main__':
    args = parser.parse_args()

    for filename in args.document:
        print("Validating syntax of document {}".format(filename))
        v = SyntaxValidator(filename, htmlvalidator="tidy")
        v.validate()
        print("Validating structure of document {}".format(filename))
        v2 = StructureValidator(v)
        v2.validate()
        print("Validating semantics of document {}".format(filename))
        v3 = SemanticsValidator(v2)
        v3.validate()
