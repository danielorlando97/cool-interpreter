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
                    a;
                    b;
                    c;
                    e;
                } 
            } ;
        } ;

        class Main inherits Object { 
            a : Int <- 1000 ;
            b : String <- "asd" ;
            c : A <- new A;
            c : Int <- 5;

            met1 ( d : Int ) : String {
                b + a
            } ;
        } ;

        

        class B inherits A {
            asd : Bool <- false ;
            b : String <- "asd" ;

            met2 (  ) : String {
                if b = "asd" then 1 else 2 fi
            } ;

            met3 (  ) : String {
                if b = 5 then "a" else "b" fi
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
        'Attribute "c" is already defined in Main.',
        'Variable "a" is not defined in "init".',
        'Variable "b" is not defined in "init".',
        'Variable "c" is not defined in "init".',
        'Cannot convert "String" into "Bool".',
        'Operation is not defined between "String" and "Int".',
        'Cannot convert "Int" into "String".',
        'Cannot convert "Int" into "String".',
        'Comparison is not defined between "String" and "Int".',
    ]

