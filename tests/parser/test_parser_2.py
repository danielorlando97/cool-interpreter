from lark import Tree
from src.parsing import parser
from src.utils import adapt_tree, Node, Print_tree


def test2():
    test2 = """ 
        class Main inherits Object { 
            a : Int <- 1000 ;
            b : String <- "asd" ;
            c : A <- new A;

            met ( d : Int ) : String {
                c.init ( b ) 
            } ;
        } ;

        class A {
            d : Int <- 0 ;

            init ( e : String ) : Bool{
                {
                    d <- 5 ;
                    e ;
                } 
            } ;
        } ;
            """

    correct2 = """Tree(start, [Tree(cool_class, [Token(CLASS, 'class'), Token(TYPE, 'Main'), Token(INHERITS, 'inherits'), Token(TYPE, 'Object'), Token(OCURLY, '{'), Tree(attr_decl, [Token(ID, 'a'), Token(COLON, ':'), Token(TYPE, 'Int'), Token(LEFT_ARROW, '<-'), Tree(integer_atom, [Token(INT, '1000')])]), Token(SEMICOLON, ';'), Tree(attr_decl, [Token(ID, 'b'), Token(COLON, ':'), Token(TYPE, 'String'), Token(LEFT_ARROW, '<-'), Tree(string_atom, [Token(ESCAPED_STRING, '"asd"')])]), Token(SEMICOLON, ';'), Tree(attr_decl, [Token(ID, 'c'), Token(COLON, ':'), Token(TYPE, 'A'), Token(LEFT_ARROW, '<-'), Tree(new_expr, [Token(NEW, 'new'), Token(TYPE, 'A')])]), Token(SEMICOLON, ';'), Tree(func_decl, [Token(ID, 'met'), Token(OPAR, '('), Tree(param, [Token(ID, 'd'), Token(COLON, ':'), Token(TYPE, 'Int')]), Token(CPAR, ')'), Token(COLON, ':'), Token(TYPE, 'String'), Token(OCURLY, '{'), Tree(dispatch, [Tree(var_expr, [Token(ID, 'c')]), Token(DOT, '.'), Token(ID, 'init'), Token(OPAR, '('), Tree(var_expr, [Token(ID, 'b')]), Token(CPAR, ')')]), Token(CCURLY, '}')]), Token(SEMICOLON, ';'), Token(CCURLY, '}')]), Token(SEMICOLON, ';'), Tree(cool_class, [Token(CLASS, 'class'), Token(TYPE, 'A'), Token(OCURLY, '{'), Tree(attr_decl, [Token(ID, 'd'), Token(COLON, ':'), Token(TYPE, 'Int'), Token(LEFT_ARROW, '<-'), Tree(integer_atom, [Token(INT, '0')])]), Token(SEMICOLON, ';'), Tree(func_decl, [Token(ID, 'init'), Token(OPAR, '('), Tree(param, [Token(ID, 'e'), Token(COLON, ':'), Token(TYPE, 'String')]), Token(CPAR, ')'), Token(COLON, ':'), Token(TYPE, 'Bool'), Token(OCURLY, '{'), Tree(block_expr, [Token(OCURLY, '{'), Tree(assign, [Token(ID, 'd'), Token(LEFT_ARROW, '<-'), Tree(integer_atom, [Token(INT, '5')])]), Token(SEMICOLON, ';'), Tree(var_expr, [Token(ID, 'e')]), Token(SEMICOLON, ';'), Token(CCURLY, '}')]), Token(CCURLY, '}')]), Token(SEMICOLON, ';'), Token(CCURLY, '}')]), Token(SEMICOLON, ';')])"""

    res_tree_2 = parser.parse(test2)

    if str(res_tree_2) != correct2:
        print(str(res_tree_2))
        res_tree_2 = adapt_tree(res_tree_2)
        Print_tree(res_tree_2)

    assert str(res_tree_2) == correct2

