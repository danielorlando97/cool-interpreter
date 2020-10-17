class AstNode:
    pass


class Program(AstNode):
    def __init__(self, class_list):
        self.cool_class_list = class_list

    def __str__(self):
        for cl in self.cool_class_list:
            return str(cl)


class CoolClass(AstNode):
    def __init__(self, feature_list, name, inherit=None):
        self.feature_list = feature_list
        self.id = name
        self.inherit = inherit

    def __str__(self):
        result = ""
        result = result + str(self.id + ":" + self.inherit) + "\n"
        for ft in self.feature_list:
            result = result + "    " + str(ft) + "\n"

        return result


class Feature(AstNode):
    pass


class AttrDecl(Feature):
    def __init__(self, idx, typex, body):
        self.id = idx
        self.type = typex
        self.body = body

    def __str__(self):
        return str(self.id + "," + self.type + " -> " + str(self.body))


class FuncDecl(Feature):
    def __init__(self, idx, params, body, typex):
        self.id = idx
        self.params = params
        self.body = body
        self.type = typex

    def __str__(self):
        return str(
            self.id
            + "("
            + str([str(p) for p in self.params])
            + ")"
            + " : "
            + self.type
            + " -> "
            + str(self.body)
        )


class Param(AstNode):
    def __init__(self, typex, idx):
        self.id = idx
        self.type = typex

    def __str__(self):
        return str(self.id + ": " + self.type)


class Expression(CoolClass):
    pass


class Dispatch(Expression):
    def __init__(self, exp, idx, exp_list):
        self.id = idx
        self.exp = exp
        self.exp_list = exp_list

    def __str__(self):
        return str("Dispatch")


class StaticDispatch(Expression):
    def __init__(self, exp, specific_type, idx, exp_list):
        self.id = idx
        self.exp = exp
        self.specific_type = specific_type
        self.exp_list = exp_list

    def __str__(self):

        return str("StaticDispatch")


class LetIn(Expression):
    def __init__(self, decl_list, exp):
        self.decl_list = decl_list
        self.exp = exp

    def __str__(self):
        return str("LetIn " + self.decl_list + ": " + str(self.exp))


class Case(Expression):
    def __init__(self, exp, case_list):
        self.exp = exp
        self.case_list = case_list

    def __str__(self):
        return str("Case " + str(self.exp) + ": " + self.case_list)


class NewType(Expression):
    def __init__(self, typex):
        self.type = typex

    def __str__(self):
        return str("NewType")


class Block(Expression):
    def __init__(self, expr_list):
        self.expr_list = expr_list

    def __str__(self):
        return str("block: " + str(self.expr_list))


class Assign(Expression):
    def __init__(self, idx, value):
        self.id = idx
        self.value = value

    def __str__(self):
        return str("Assign")


# Unary expressions
############################################


class Unary(Expression):
    def __init__(self, exp):
        self.exp = exp


class Not(Unary):
    def __str__(self):
        return str("Not " + str(self.exp))


class IsVoid(Unary):
    def __str__(self):
        return str("IsVoid? " + str(self.exp))


class Tilde(Unary):
    def __str__(self):
        return str("Tilde")


class ParenthExp(Unary):
    def __str__(self):
        return str("(" + str(self.exp) + ")")


# Binary expressions
##########################################


class Binary(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Comparisson(Binary):
    pass


class Leq(Comparisson):
    def __str__(self):
        return str("Leq")


class Eq(Comparisson):
    def __str__(self):
        return str("Eq")


class Le(Comparisson):
    def __str__(self):
        return str("Le")


class Arithmetic(Binary):
    pass


class Plus(Arithmetic):
    def __str__(self):
        return str("Plus")


class Minus(Arithmetic):
    def __str__(self):
        return str("Minus")


class Mult(Arithmetic):
    def __str__(self):
        return str("Mult")


class Div(Arithmetic):
    def __str__(self):
        return str("Div")


class WhileLoop(Binary):
    def __str__(self):
        return str("While")


# Ternary expressions
##########################################


class Ternary(Expression):
    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third


class IfThenElse(Ternary):
    def __str__(self):
        return str("IfThenElse")


# Atoms
#########################################


class Atom(Expression):
    def __init__(self, lex):
        self.lex = lex


class IntExp(Atom):
    def __str__(self):
        return str("Int")


class StringExp(Atom):
    def __str__(self):
        return str("String")


class BoolExp(Atom):
    def __str__(self):
        return str("Bool")


class IdExp(Expression):
    def __init__(self, lex):
        self.id = lex

    def __str__(self):
        return str("Id")

