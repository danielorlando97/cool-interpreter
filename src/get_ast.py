from lark import Transformer
from src.cool_ast import (
    Program,
    CoolClass,
    FuncDecl,
    AttrDecl,
    Param,
    Assign,
    Not,
    Le,
    Leq,
    Eq,
    Plus,
    Minus,
    Mult,
    Div,
    IsVoid,
    Dispatch,
    StaticDispatch,
    IfThenElse,
    WhileLoop,
    LetIn,
    Case,
    NewType,
    ParenthExp,
    IdExp,
    Block,
    IntExp,
    StringExp,
    BoolExp,
)


class GetTree(Transformer):
    def start(self, children):
        class_list = []
        for item in children:
            try:
                if item.value == ";":
                    pass
            except AttributeError:
                class_list.append(item)
        return Program(class_list)

    def cool_class(self, children):
        name = children[1].value
        if children[2].value == "inherits":
            inherit = children[3].value
            n = 5
        else:
            inherit = None
            n = 3

        feat_list = []

        while n < len(children):
            try:
                if children[n].value == "}":
                    break
            except AttributeError:
                feat_list.append(children[n])

            n += 1

        return CoolClass(feat_list, name, inherit)

    def func_decl(self, children):
        idx = children[0].value
        param_list = []
        n = 2
        while n < len(children):
            try:
                if children[n].value == ")":
                    break
                elif children[n].value == ",":
                    n += 1
            except AttributeError:
                param_list.append(children[n])
                n += 1

        n += 2
        return_type = children[n].value
        n += 2
        expr_body = children[n]
        return FuncDecl(idx, param_list, expr_body, return_type)

    def attr_decl(self, children):
        idx = children[0].value
        typex = children[2].value
        if len(children) > 3:
            body = children[4]
        else:
            body = None

        return AttrDecl(idx, typex, body)

    def param(self, children):
        return Param(children[2].value, children[0].value)

    def assign(self, children):
        return Assign(children[0].value, children[2])

    def not_expr(self, children):
        return Not(children[1])

    def comparison_leq(self, children):
        return Leq(children[0], children[2])

    def comparison_le(self, children):
        return Le(children[0], children[2])

    def comparison_eq(self, children):
        return Eq(children[0], children[2])

    def arithmetic_add(self, children):
        return Plus(children[0], children[2])

    def arithmetic_sub(self, children):
        return Minus(children[0], children[2])

    def term_mul(self, children):
        return Mult(children[0], children[2])

    def term_div(self, children):
        return Div(children[0], children[2])

    def isvoid_expr(self, children):
        return IsVoid(children[1])

    def tilde_expr(self, children):
        return IsVoid(children[1])

    def dispatch(self, children):
        exp = children[0]
        idx = children[2]

        args = []
        n = 4
        while n < len(children):
            try:
                if children[n].value == ")":
                    break
            except AttributeError:
                args.append(children[n])
                n += 2

        return Dispatch(exp, idx, args)

    def staticDispatch(self, children):
        exp_type = children[0]
        static_type = children[2]
        idx = children[4]

        args = []
        n = 6
        while n < len(children):
            try:
                if children[n].value == ")":
                    break
            except AttributeError:
                args.append(children[n])
                n += 2

        return StaticDispatch(exp_type, static_type, idx, args)

    def if_expr(self, children):
        return IfThenElse(children[1], children[3], children[5])

    def while_expr(self, children):
        return WhileLoop(children[1], children[3])

    def let_expr(self, children):
        decl_list = []

        n = 1

        while True:

            idx = children[n].value
            n += 2
            typex = children[n]

            if children[n + 1].value == "<-":
                n += 2
                expr = children[n]
            else:
                expr = None

            decl_list.append((idx, typex, expr))
            n += 1

            if children[n].value == "in":
                break

            n += 1

        body = children[n + 1]

        return LetIn(decl_list, body)

    def case_expr(self, children):
        expr = children[1]

        n = 3

        case_list = []
        while children[n].value != "esac":
            idx = children[n].value
            typex = children[n + 2].value
            case_expr = children[n + 4]
            case_list.append((idx, typex, case_expr))
            n += 6
        return Case(expr, case_list)

    def new_expr(self, children):
        return NewType(children[1].value)

    def parenthized_expr(self, children):
        return ParenthExp(children[1])

    def var_expr(self, children):
        return IdExp(children[0].value)

    def block_expr(self, children):
        expr_list = []

        n = 1
        while True:
            expr_list.append(children[n])
            n += 2
            try:
                if children[n].value == "}":
                    break
            except AttributeError:
                continue

        return Block(expr_list)

    def integer_atom(self, chidren):
        return IntExp(chidren[0].value)

    def string_atom(self, chidren):
        return StringExp(chidren[0].value)

    def bool_atom(self, chidren):
        return BoolExp(chidren[0].value)
