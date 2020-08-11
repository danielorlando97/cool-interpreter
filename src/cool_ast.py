class AstNode:
    pass

class Program(AstNode):
    def __init__(self, class_list):
        self.cool_class_list = class_list

class Cool_class(AstNode):
    def __init__(self, feature_list):
        self.feature_list = feature_list

class Feature (AstNode):
    pass

class AttrDecl (Feature):
    def __init__(self, idx, typex, value):
        self.id = idx
        self.type = typex
        self .value = value

class FuncDecl (Feature):
    def __init__(self, idx, params, body, typex):
        self.id = idx
        self.params = params
        self.body = body
        self.type = typex

class Param(AstNode):
    def __init__(self, typex, idx):
        self.id = idx
        self.type = typex

class Expression(Cool_class):
    pass

class Dispatch(Expression):
    def __init__(self, exp_type, idx, exp_list):
        self.id = idx
        self.exp_type = exp_type
        self.exp_list = exp_list

class StaticDispatch(Expression):
    def __init__(self, exp , especific_type , idx, exp_list):
        self.id = idx
        self.exp = exp
        self.especific_type = especific_type
        self.exp_list = exp_list

class LetIn(Expression):
    def __init__(self, decl_list, exp):
        self.decl_list = decl_list
        self.exp = exp

class Case(Expression):
    def __init__(self, exp, case_list):
        self.exp = exp
        self.case_list = case_list

class NewType(Expression):
    def __init__(self, typex):
        self.type = typex

class Block(Expression):
    def __init__(self, expr_list):
        self.expr_list = expr_list 

# Unary expressions
############################################

class Unary(Expression):
    def __init__(self, exp):
        self.exp = exp

class Not(Unary):
    pass

class IsVoid(Unary):
    pass

class Tilde(Unary):
    pass

class ParenthExp(Unary):
    pass


# Binary expressions
##########################################

class Binary(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Comparisson(Binary):
    pass

class Leq(Comparisson):
    pass

class Eq(Comparisson):
    pass

class Le(Comparisson):
    pass

class Arithmetic(Binary):
    pass

class Plus(Arithmetic):
    pass

class Minus(Arithmetic):
    pass

class Mult(Arithmetic):
    pass

class Div(Arithmetic):
    pass

class WhileLoop(Binary):
    pass

# Ternary expressions
##########################################

class Ternary(Expression):
    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third

class IfThenElse(Ternary):
    pass


# Atoms
#########################################

class Atom(Expression):
    def __init__(self, lex):
        self.lex = lex

class IntExp(Atom):
    pass

class StringExp(Atom):
    pass

class BoolExp(Atom):
    pass

class IdExp(Atom):
    pass

