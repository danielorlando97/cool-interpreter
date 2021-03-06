from lark import Lark, Transformer

parser = Lark(
    """
          ?start : (class SEMICOLON)+

          ?class : CLASS TYPE [INHERITS TYPE] OCURLY (feature SEMICOLON)* CCURLY

        ?feature : ID OPAR [param (COMMA param)*] CPAR COLON TYPE OCURLY expr CCURLY
                 | ID COLON TYPE [LEFT_ARROW expr]

          ?param : ID COLON TYPE

           ?expr : ID LEFT_ARROW expr -> assign
                 | not

            ?not : NOT not
                 | comparison

     ?comparison : arithmetic LEQ arithmetic -> comparison_leq
                 | arithmetic LE arithmetic -> comparison_le
                 | arithmetic EQ arithmetic -> comparison_eq
                 | arithmetic
 
     ?arithmetic : arithmetic PLUS term -> arithmetic_add
                 | arithmetic MINUS term -> arithmetic_sub
                 | term

           ?term : term STAR factor -> term_mul
                 | term SLASH factor -> term_div
                 | factor

         ?factor : ISVOID factor
                 | tilde

          ?tilde : TILDE tilde
                 | dispatch

       ?dispatch : dispatch DOT ID OPAR [expr (COMMA expr)*] CPAR
                 | static_dispatch

?static_dispatch : static_dispatch AT TYPE DOT ID OPAR [expr (COMMA expr)*] CPAR
                 | atom

           ?atom : IF expr THEN expr ELSE expr FI -> if_expr
                 | WHILE expr LOOP expr POOL -> while_expr
                 | LET ID COLON TYPE [LEFT_ARROW expr] [(COMMA ID COLON TYPE [LEFT_ARROW expr])*] IN expr -> let_expr
                 | CASE expr OF (ID COLON TYPE RIGHT_ARROW expr SEMICOLON)+ ESAC -> case_expr
                 | NEW TYPE -> new_expr
                 | OPAR expr CPAR -> parenthized_expr
                 | ID -> var_expr
                 | OCURLY expr SEMICOLON [(expr SEMICOLON)*] CCURLY -> block
                 | constant

       ?constant : INT
                 | ESCAPED_STRING
                 | TRUE
                 | FALSE
 
// Terminals

TYPE : UCASE_LETTER [CNAME]
ID : LCASE_LETTER [CNAME]
SEMICOLON : ";"
CLASS : "class"
INHERITS : "inherits"
OCURLY : "{"
CCURLY : "}"
OPAR : "("
CPAR : ")"
COMMA : ","
COLON : ":"
LEFT_ARROW : "<-"
RIGHT_ARROW : "->"
NOT : "not"
LEQ : "<="
LE : "<"
EQ : "="
PLUS : "+"
MINUS : "-"
STAR : "*"
SLASH : "/"
ISVOID : "isvoid"
TILDE : "~"
DOT : "."
AT : "@"
IF : "if"
THEN : "then"
ELSE : "else"
FI : "fi"
WHILE : "while"
LOOP : "loop"
POOL : "pool"
LET : "let"
IN : "in"
CASE : "case"
OF : "of"
NEW : "new"
TRUE : "true"
FALSE : "false"
ESAC : "esac"

// Imports and Ignores

%import common.UCASE_LETTER
%import common.LCASE_LETTER
%import common.CNAME
%import common.INT
%import common.ESCAPED_STRING
%import common.WS


%ignore WS
""",
    parser="lalr",
    transformer=None,
)




