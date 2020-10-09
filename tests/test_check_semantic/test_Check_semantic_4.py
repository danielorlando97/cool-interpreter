from lark import Tree
from src.parsing import parser
from src.get_ast import GetTree
from src.check_semantic import TypeCollector, TypeBuilder, TypeChecker


def test4():
    test4 = """ 
        class A {
            d : AUTO_TYPE <- 2 ;

            met1 ( e : String ) : AUTO_TYPE {
                    
                    e
            } ;

            a : AUTO_TYPE <- 5 ;
            b : String ;

            met2 ( e : String ) : String {
                    
                    b <- a
            } ;
        } ;

        
        
            """

    res_tree_4 = parser.parse(test4)

    ast = GetTree().transform(res_tree_4)

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

    assert errors == []

