
##FONTE https://rosettacode.org/wiki/S-Expressions#Python
import re
 
dbg = False
 
term_regex = r'''(?mx)
    \s*(?:
        (?P<brackl>\()|
        (?P<brackr>\))|
        (?P<num>\-?\d+\.\d+|\-?\d+)|
        (?P<sq>"[^"]*")|
        (?P<s>[^(^)\s]+)
       )'''
 
def parse_sexp(sexp):
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
            assert stack, "Trouble with nesting of brackets"
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
    assert not stack, "Trouble with nesting of brackets"
    return out[0]
 
def print_sexp(exp):
    out = ''
    if type(exp) == type([]):
        out += '(' + ' '.join(print_sexp(x) for x in exp) + ')'
    elif type(exp) == type('') and re.search(r'[\s()]', exp):
        out += '"%s"' % repr(exp)[1:-1].replace('"', '\"')
    else:
        out += '%s' % exp
    return out
 
 
if __name__ == '__main__':
    sexp ="""
    (mealy
( symbols-in a b)
( symbols-out 0 1)
( states q0 q1 q2 q3 )
( start q0 )
( finals q3 )
( trans
( q0 q1 a 0) ( q0 q3 b 0) ( q1 q2 b 1) ( q1 q3 a 1)
( q2 q3 a 0) ( q2 q3 b 1) ( q3 q0 b 1) ( q3 q3 a 1 ) ) )
    """

#     """
#     (moore
# ( symbols-in a b)
# ( symbols-out 0 1)
# ( states q0 q0' q1 q2 q3 q3' )
# ( start q0 )
# ( finals q3 q3' )
# ( trans
# ( q0 q1 a ) ( q0 q3 b) ( q1 q3' a ) ( q1 q2 b)
# ( q2 q0' a ) ( q2 q3 ' b) ( q3 q3 ' a ) ( q3 q0' b)
# ( q3' q3' a ) ( q ' q0' b ) )
# ( out-fn
# ( q0 ( ) ) ( q0' 1) ( q1 0)
# ( q2 1) ( q3 0) ( q3 ' 1 ) ) )
#     """

    
 
    print('Input S-expression: %r' % (sexp, ))
    parsed = parse_sexp(sexp)
    print("\nParsed to Python:", parsed)
 
    print("\nThen back to: '%s'" % print_sexp(parsed))