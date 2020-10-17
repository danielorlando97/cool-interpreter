from lark import Tree
from src.parsing import parser
from src.get_ast import GetTree
from src.check_semantic import TypeCollector, TypeBuilder, TypeChecker
from src.type_infer import BagsCollector, BagsReducer
from src.cool_ast import FuncDecl

from src.pipeline import search_for_errors


def test4():
    test4 = """
        class A {
            a : AUTO_TYPE <- 5 ;

            h() : AUTO_TYPE {
                let z : Int <- 5, x : Int <- 5 in { 
                        z + x ;                      
                } 
            };
            
            f(a: AUTO_TYPE, b: AUTO_TYPE) : AUTO_TYPE {
                if (a=1) then b else
                    self.g(a + 1, b/2)
                fi
            };

            g(a: AUTO_TYPE, b: AUTO_TYPE) : AUTO_TYPE {
                if (b=1) then a else
                    self.f(a/2, b+1)
                fi
            };


        } ;


            """

    res_tree = parser.parse(test4)

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

    assert errors == []

