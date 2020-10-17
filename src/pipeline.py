from lark import Tree
from src.parsing import parser
from src.get_ast import GetTree
from src.check_semantic import TypeCollector, TypeBuilder, TypeChecker
from src.type_infer import BagsCollector, BagsReducer
from src.cool_ast import FuncDecl


def run_pipeline(code):

    res_tree = parser.parse(code)

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
        return False

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

    if errors != []:
        return False

    # TODO: apply changes to context

    return True


def search_for_errors(tyBags, errors):
    for key, value in tyBags.vars.items():
        if len(value) != 1:
            value.remove("@error")
            errors.append(
                "Can't infer type of: '" + str(key) + "', between" + str(sorted(value))
            )
    for key, child in tyBags.children.items():
        search_for_errors(child, errors)

