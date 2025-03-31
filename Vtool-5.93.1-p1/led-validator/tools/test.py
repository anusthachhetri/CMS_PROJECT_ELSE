from tools.led.syntax import SyntaxValidator
from tools.led.structure import StructureValidator
from tools.led.semantics import SemanticsValidator

filename = "test.html"

v = SyntaxValidator(filename, htmlvalidator="tidy")
v.validate()

v2 = StructureValidator(v)
v2.validate()

v3 = SemanticsValidator(v2)
v3.validate()
