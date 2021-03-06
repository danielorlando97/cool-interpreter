from lark import Tree 
from src.parsing import parser
from src.utils import adapt_tree, Node, Print_tree

def test3():
    test3 =''' 
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
                    let z : Int <- d, x : String <- "asdd" in { 
                        case new B of 
                        y : Bool -> true ;
                        w : Int -> 5 ;
                        esac ;
                        
                     } ;
                } 
            } ;
        } ;

        class B inherits A {
            asd : Bool <- false ;
        } ;
            '''

    correct3 = '''Tree(start, [Tree(class, [Token(CLASS, 'class'), Token(TYPE, 'Main'), Token(INHERITS, 'inherits'), Token(TYPE, 'Object'), Token(OCURLY, '{'), Tree(feature, [Token(ID, 'a'), Token(COLON, ':'), Token(TYPE, 'Int'), Token(LEFT_ARROW, '<-'), Token(INT, '1000')]), Token(SEMICOLON, ';'), Tree(feature, [Token(ID, 'b'), Token(COLON, ':'), Token(TYPE, 'String'), Token(LEFT_ARROW, '<-'), Token(ESCAPED_STRING, '"asd"')]), Token(SEMICOLON, ';'), Tree(feature, [Token(ID, 'c'), Token(COLON, ':'), Token(TYPE, 'A'), Token(LEFT_ARROW, '<-'), Tree(new_expr, [Token(NEW, 'new'), Token(TYPE, 'A')])]), Token(SEMICOLON, ';'), Tree(feature, [Token(ID, 'met'), Token(OPAR, '('), Tree(param, [Token(ID, 'd'), Token(COLON, ':'), Token(TYPE, 'Int')]), Token(CPAR, ')'), Token(COLON, ':'), Token(TYPE, 'String'), Token(OCURLY, '{'), Tree(dispatch, [Tree(var_expr, [Token(ID, 'c')]), Token(DOT, '.'), Token(ID, 'init'), Token(OPAR, '('), Tree(var_expr, [Token(ID, 'b')]), Token(CPAR, ')')]), Token(CCURLY, '}')]), Token(SEMICOLON, ';'), Token(CCURLY, '}')]), Token(SEMICOLON, ';'), Tree(class, [Token(CLASS, 'class'), Token(TYPE, 'A'), Token(OCURLY, '{'), Tree(feature, [Token(ID, 'd'), Token(COLON, ':'), Token(TYPE, 'Int'), Token(LEFT_ARROW, '<-'), Token(INT, '0')]), Token(SEMICOLON, ';'), Tree(feature, [Token(ID, 'init'), Token(OPAR, '('), Tree(param, [Token(ID, 'e'), Token(COLON, ':'), Token(TYPE, 'String')]), Token(CPAR, ')'), Token(COLON, ':'), Token(TYPE, 'Bool'), Token(OCURLY, '{'), Tree(block, [Token(OCURLY, '{'), Tree(let_expr, [Token(LET, 'let'), Token(ID, 'z'), Token(COLON, ':'), Token(TYPE, 'Int'), Token(LEFT_ARROW, '<-'), Tree(var_expr, [Token(ID, 'd')]), Token(COMMA, ','), Token(ID, 'x'), Token(COLON, ':'), Token(TYPE, 'String'), Token(LEFT_ARROW, '<-'), Token(ESCAPED_STRING, '"asdd"'), Token(IN, 'in'), Tree(block, [Token(OCURLY, '{'), Tree(case_expr, [Token(CASE, 'case'), Tree(new_expr, [Token(NEW, 'new'), Token(TYPE, 'B')]), Token(OF, 'of'), Token(ID, 'y'), Token(COLON, ':'), Token(TYPE, 'Bool'), Token(RIGHT_ARROW, '->'), Token(TRUE, 'true'), Token(SEMICOLON, ';'), Token(ID, 'w'), Token(COLON, ':'), Token(TYPE, 'Int'), Token(RIGHT_ARROW, '->'), Token(INT, '5'), Token(SEMICOLON, ';'), Token(ESAC, 'esac')]), Token(SEMICOLON, ';'), Token(CCURLY, '}')])]), Token(SEMICOLON, ';'), Token(CCURLY, '}')]), Token(CCURLY, '}')]), Token(SEMICOLON, ';'), Token(CCURLY, '}')]), Token(SEMICOLON, ';'), Tree(class, [Token(CLASS, 'class'), Token(TYPE, 'B'), Token(INHERITS, 'inherits'), Token(TYPE, 'A'), Token(OCURLY, '{'), Tree(feature, [Token(ID, 'asd'), Token(COLON, ':'), Token(TYPE, 'Bool'), Token(LEFT_ARROW, '<-'), Token(FALSE, 'false')]), Token(SEMICOLON, ';'), Token(CCURLY, '}')]), Token(SEMICOLON, ';')])'''

    res_tree_3 = parser.parse(test3)

    if(str(res_tree_3) != correct3):
        print(res_tree_3)
        res_tree_3 = adapt_tree(res_tree_3)
        Print_tree(res_tree_3)   

    assert (str(res_tree_3) == correct3)

    











