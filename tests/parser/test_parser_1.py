from lark import Tree 
from src.parsing import parser
from src.utils import adapt_tree, Node, Print_tree

def test1():
    test1 =''' 
        class Main inherits Object { 
            a : Int <- asd ;
            b : String <- 1000;
            c : Bool <- true;

            met ( d : Int ) : String {
                c <- false
            } ;
            } ; 
            '''

    correct1 = '''Tree(start, [Tree(class, [Token(CLASS, 'class'), Token(TYPE, 'Main'), Token(INHERITS, 'inherits'), Token(TYPE, 'Object'), Token(OCURLY, '{'), Tree(feature, [Token(ID, 'a'), Token(COLON, ':'), Token(TYPE, 'Int'), Token(LEFT_ARROW, '<-'), Tree(var_expr, [Token(ID, 'asd')])]), Token(SEMICOLON, ';'), Tree(feature, [Token(ID, 'b'), Token(COLON, ':'), Token(TYPE, 'String'), Token(LEFT_ARROW, '<-'), Token(INT, '1000')]), Token(SEMICOLON, ';'), Tree(feature, [Token(ID, 'c'), Token(COLON, ':'), Token(TYPE, 'Bool'), Token(LEFT_ARROW, '<-'), Token(TRUE, 'true')]), Token(SEMICOLON, ';'), Tree(feature, [Token(ID, 'met'), Token(OPAR, '('), Tree(param, [Token(ID, 'd'), Token(COLON, ':'), Token(TYPE, 'Int')]), Token(CPAR, ')'), Token(COLON, ':'), Token(TYPE, 'String'), Token(OCURLY, '{'), Tree(assign, [Token(ID, 'c'), Token(LEFT_ARROW, '<-'), Token(FALSE, 'false')]), Token(CCURLY, '}')]), Token(SEMICOLON, ';'), Token(CCURLY, '}')]), Token(SEMICOLON, ';')])'''

    res_tree_1 = parser.parse(test1)    

    if (str(res_tree_1) != correct1):
        res_tree_1 = adapt_tree(res_tree_1)
        Print_tree(res_tree_1)

    assert (str(res_tree_1) == correct1)











