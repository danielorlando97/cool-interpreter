from lark import Tree
from src.parsing import parser
from src.get_ast import GetTree
from src.check_semantic import TypeCollector, TypeBuilder, TypeChecker
from src.type_infer import BagsCollector, BagsReducer
from src.cool_ast import FuncDecl
from src.pipeline import search_for_errors


def test2():
    test2 = """
        class A {

            met1 ( e : String ) : AUTO_TYPE {
                    {
                    a <- 5 ;
                    a <- b ;
                    b <- "asd" ;
                    b <- true ;
                    b <- c ;
                    c ;
                    } + 5
            } ;

            a : AUTO_TYPE ;
            b : AUTO_TYPE ;
            c : AUTO_TYPE ;


        } ;       


            """

    res_tree = parser.parse(test2)

    ast = GetTree().transform(res_tree)

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
    _ = checker.visit(ast)
    print("Errors: [")
    for error in errors:
        print("\t", error)
    print("]")

    if errors != []:
        assert False

    errors = []

    print("================= BAGS COLLECTOR =================")
    collector = BagsCollector(context, errors)

    bags = collector.visit(ast)
    print("LIST:")
    print(bags)
    print("")

    print("================= BAGS REDUCER =================")
    collector = BagsReducer(bags, context, errors)

    bags = collector.visit(ast)
    print("LIST:")
    print(bags)
    print("")

    search_for_errors(bags, errors)

    print("Errors: [")
    for error in errors:
        print("\t", error)
    print("]")

    assert errors == [
        "Can't infer type of: 'a', between['A', 'AUTO_TYPE', 'Bool', 'Int', 'Object', 'String', 'Void']",
        "Can't infer type of: 'b', between['A', 'AUTO_TYPE', 'Bool', 'Int', 'Object', 'String', 'Void']",
    ]
