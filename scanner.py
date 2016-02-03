from __future__ import print_function # use python 3 style print statements
import sys
import ply.lex as lex

tokens = (          # tokens list, every token returned MUST end up with a type in this list
    'IDENTIFIER',
    'INTLITERAL',
    'FLOATLITERAL',
    'STRINGLITERAL',
    'COMMENT',
    'KEYWORD',
    'OPERATOR',
    )

keywords = (        # this list allows identifiers to be flagged as keywords if in this list
    'PROGRAM',
    'BEGIN',
    'END',
    'FUNCTION',
    'READ',
    'WRITE',
    'IF',
    'ELSE',
    'ENDIF',
    'WHILE',
    'ENDWHILE',
    'CONTINUE',
    'BREAK',
    'RETURN',
    'INT',
    'VOID',
    'STRING',
    'FLOAT',
    )
    
t_ignore = ' \t'            # ignore and skip over spaces and tabs (special variable name)
    
def t_COMMENT(t):           # COMMENT must be before OPERATOR or the dashes will be seen as -
    r'--.*'                 # note: . matches any char EXCEPT \n
    pass

def t_OPERATOR(t):          # alternations in proper order to match < only if not <=
    r':=|\+|-|\*|/|!=|\(|\)|;|,|<=|>=|=|<|>'
    return t

def t_FLOATLITERAL(t):      # FLOAT must be before INT or 1.4 will be seen as 1, 0.4
    r'(\d+\.\d*|\d*\.\d+)'  # sadly, just d*/.d* matches a . without any digits.
    t.value=float(t.value)
    return t
    
def t_INTLITERAL(t):
    r'\d+'
    t.value=int(t.value)
    return t
    
def t_STRINGLITERAL(t):
    r'".*?"'                # need greedy (?) modifier on * to disallow "str"ing"
    return t
    
def t_IDENTIFIER(t):        # keywords match here also so check if the identifier is in
    r'[a-zA-Z][a-zA-Z0-9]*' # the keyword list
    if t.value in keywords:
        t.type='KEYWORD'
    return t
    
def t_newline(t):           # need to match newlines, in theory they could probably be ignored,
    r'\n|\r\n'              # but this function allows keeping track of line numbers.
    t.lexer.lineno+=1       # note nothing returned. (arbitrary function name)
    
def t_error(t):             # anything not matched so far is an error (special function name)
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


try:                        # attempt to open file, read it in, build lexer, feed it data,
    f=open(sys.argv[1],'r') # and iterate through resulting token list
except IndexError:
    print ("missing input file", file=sys.stderr)
except IOError:
    print ("cannot open", sys.argv[1], file=sys.stderr)
else:
    data=f.read()
    f.close()

    lexer = lex.lex() 
    lexer.input(data)

    for token in lexer:
        print ("Token Type: %s%s"%(token.type, '\r')) # add \r before \n to match sample out files
        print ("Value: %s%s"%(token.value, '\r'))

