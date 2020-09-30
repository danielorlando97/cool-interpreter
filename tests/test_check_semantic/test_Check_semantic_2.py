from lark import Tree
from src.parsing import parser
from src.get_ast import GetTree
from src.check_semantic import TypeCollector, TypeBuilder, TypeChecker


def test2():
    test2 = """ 
        class A {
            d : Int <- 0 ;

            init ( e : String ) : Bool {
                {
                    let z : Int <- d, x : Int <- 5 in { 
                        z + x ;                      
                     } ;
                } 
            } ;
        } ;

        class Main inherits Object { 
            a : Int <- 1000 ;
            b : String <- "asd" ;
            c : A <- new A;

            met1 ( d : Int ) : String {
                c.init ( d ) 
            } ;
        } ;

        

        class B inherits A {
            asd : Bool <- false ;
            b : String <- "asd" ;

            met2 ( d : Int ) : String {
                c.init ( b ) 
            } ;
        } ;
            """

    res_tree_2 = parser.parse(test2)

    ast = GetTree().transform(res_tree_2)

    errors = []

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    print("================= TYPE COLLECTOR =================")
    print("Errors:", errors)
    print("Context:")
    print(context)
    print("")

    print("================= TYPE BUILDER =================")
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    print("Errors: [")
    for error in errors:
        print("\t", error)
    print("]")
    print("Context:")
    print(context)

    print("=============== CHECKING TYPES ================")
    checker = TypeChecker(context, errors)
    scope = None
    _ = checker.visit(ast, scope)
    print("Errors: [")
    for error in errors:
        print("\t", error)
    print("]")

    assert errors == [
        'Cannot convert "Int" into "Bool".',
        'Cannot convert "Int" into "String".',
        'Cannot convert "Bool" into "String".',
        'Variable "c" is not defined in "met2".',
        'Method "init" is not defined in <error>.',
    ]

