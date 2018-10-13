##FONTE https://rosettacode.org/wiki/S-Expressions#Python
import re
from typing import List

dbg = False
 
term_regex = r'''(?mx)
	\s*(?:
		(?P<brackl>\()|
		(?P<brackr>\))|
		(?P<num>\-?\d+\.\d+|\-?\d+)|
		(?P<sq>"[^"]*")|
		(?P<s>[^(^)\s]+)
	   )'''
 
def parse_sexp(sexp) -> List:
	stack = []
	out = []
	if dbg: print("%-6s %-14s %-44s %-s" % tuple("term value out stack".split()))
	for termtypes in re.finditer(term_regex, sexp):
		term, value = [(t,v) for t,v in termtypes.groupdict().items() if v][0]
		if dbg: print("%-7s %-14s %-44r %-r" % (term, value, out, stack))
		if   term == 'brackl':
			stack.append(out)
			out = []
		elif term == 'brackr':
			assert stack, "Problema com os parênteses"
			tmpout, out = out, stack.pop(-1)
			out.append(tmpout)
		elif term == 'num':
			v = float(value)
			if v.is_integer(): v = int(v)
			out.append(v)
		elif term == 'sq':
			out.append(value[1:-1])
		elif term == 's':
			out.append(value)
		else:
			raise NotImplementedError("Error: %r" % (term, value))
	assert not stack, "Problema com os parênteses"
	return out[0]

def to_sexp_visual(lista):

	def format_item(item):

		if type(item) in [int, str]:
			return str(item)

		elif type(item) == list and not item:
			return "()"

		elif type(item) == list and (type(item[-1]) != list or not item[-1]):
			return "\n\t({})".format(
				" ".join([format_item(sub) for sub in item])
			)

		else:
			return "\n(" + " ".join([format_item(x) for x in item]) + "\n)"

	s_expression = ""

	for item in lista:
		str_item = format_item(item)

		if "trans" in str_item or "out-fn" in str_item:
			s_expression += str_item.replace("\n", "\n\t")

		else:
			s_expression += str_item

	return "(" + s_expression + "\n)"


def print_sexp(exp) -> str:
	out = ''
	if type(exp) == type([]):
		out += '(' + ' '.join(print_sexp(x) for x in exp) + ')'
	elif type(exp) == type('') and re.search(r'[\s()]', exp):
		out += '"%s"' % repr(exp)[1:-1].replace('"', '\"')
	else:
		out += '%s' % exp
	return out