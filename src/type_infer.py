from src.type_bags import TyBags
from src.utils import find_types, get_common_ancestor, intersection
import src.visitor as visitor
from src.semantic import (
    SemanticError,
    Attribute,
    Method,
    Type,
    VoidType,
    ErrorType,
    Context,
    IntType,
    BoolType,
    StringType,
    AutoType,
)
from src.cool_ast import (
    AstNode,
    Program,
    CoolClass,
    FuncDecl,
    AttrDecl,
    Param,
    Assign,
    Binary,
    Arithmetic,
    Comparisson,
    Not,
    IsVoid,
    Tilde,
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
    Plus,
    Minus,
    Mult,
    Div,
    Le,
    Leq,
    Eq,
)


class BagsCollector:
    def __init__(self, context, errors=[]):
        self.context = context
        self.errors = errors

    @visitor.on("node")
    def visit(self, node, bags):
        pass

    @visitor.when(Program)
    def visit(self, node, tyBags=None):
        tyBags = TyBags()

        for cool_class in node.cool_class_list:
            self.visit(cool_class, tyBags)
        return tyBags

    @visitor.when(CoolClass)
    def visit(self, node, tyBags):
        tyBags = tyBags.create_child(node)

        self.current_type = self.context.get_type(node.id)

        tyBags.define_variable("self", [self.current_type.name])

        for method in self.current_type.methods:
            if method.return_type == AutoType():
                types = list(self.context.types.keys())
            else:
                types = [method.return_type.name]

            tyBags.define_variable(method.name, types)

        for attr in self.current_type.attributes:
            if attr.type == AutoType():
                types = list(self.context.types.keys())
            else:
                types = [attr.type.name]
            tyBags.define_variable(attr.name, types)

        for feat in node.feature_list:
            self.visit(feat, tyBags)
        return tyBags

    @visitor.when(AttrDecl)
    def visit(self, node, tyBags):
        return

    @visitor.when(FuncDecl)
    def visit(self, node, tyBags):
        self.current_method = self.current_type.get_method(node.id)
        method_tyBags = tyBags.create_child(node)

        for pname, ptype in zip(
            self.current_method.param_names, self.current_method.param_types
        ):
            if ptype == AutoType():
                method_tyBags.define_variable(pname, list(self.context.types.keys()))
            else:
                method_tyBags.define_variable(pname, [ptype.name])

        self.visit(node.body, method_tyBags)

        self.current_method = None

    @visitor.when(Assign)
    def visit(self, node, tyBags):
        return

    @visitor.when(Dispatch)
    def visit(self, node, tyBags):
        return

    @visitor.when(StaticDispatch)
    def visit(self, node, tyBags):
        return

    @visitor.when(LetIn)
    def visit(self, node, tyBags):
        let_tyBags = tyBags.create_child(node)
        decl_list, exp = node.decl_list, node.exp

        for idx, _type, _ in decl_list:
            typex = self.context.get_type(_type)

            if typex == AutoType():
                let_tyBags.define_variable(idx, list(self.context.types.keys()))
            else:
                let_tyBags.define_variable(idx, [typex.name])

        self.visit(exp, let_tyBags)

    # TODO
    @visitor.when(Case)
    def visit(self, node, tyBags):
        self.visit(node.exp, tyBags)

        for idx, typex, case_exp in node.case_list:

            new_tyBags = tyBags.create_child(case_exp)

            typex = self.context.get_type(typex)

            if typex == AutoType():
                new_tyBags.define_variable(idx, list(self.context.types.keys()))
            else:
                new_tyBags.define_variable(idx, [typex.name])

            self.visit(case_exp, new_tyBags)

    @visitor.when(Block)
    def visit(self, node, tyBags):
        for exp in node.expr_list:
            self.visit(exp, tyBags)

    @visitor.when(Not)
    def visit(self, node, tyBags):
        self.visit(node.exp, tyBags)

    # TODO
    @visitor.when(Tilde)
    def visit(self, node, tyBags):
        return

    @visitor.when(IsVoid)
    def visit(self, node, tyBags):
        self.visit(node.exp, tyBags)

    @visitor.when(ParenthExp)
    def visit(self, node, tyBags):
        self.visit(node.exp, tyBags)

    def arith(self, node, tyBags):

        self.visit(node.left, tyBags)
        self.visit(node.right, tyBags)

    @visitor.when(Plus)
    def visit(self, node, tyBags):
        self.arith(node, tyBags)

    @visitor.when(Minus)
    def visit(self, node, tyBags):
        self.arith(node, tyBags)

    @visitor.when(Div)
    def visit(self, node, tyBags):
        self.arith(node, tyBags)

    @visitor.when(Mult)
    def visit(self, node, tyBags):
        self.arith(node, tyBags)

    def comp(self, node, tyBags):
        self.visit(node.left, tyBags)
        self.visit(node.right, tyBags)

    @visitor.when(Leq)
    def visit(self, node, tyBags):
        self.comp(node, tyBags)

    @visitor.when(Eq)
    def visit(self, node, tyBags):
        self.comp(node, tyBags)

    @visitor.when(Le)
    def visit(self, node, tyBags):
        self.comp(node, tyBags)

    @visitor.when(WhileLoop)
    def visit(self, node, tyBags):
        pass
        self.visit(node.left, tyBags)
        self.visit(node.right, tyBags)

    @visitor.when(IfThenElse)
    def visit(self, node, tyBags):
        self.visit(node.first, tyBags)
        self.visit(node.second, tyBags)
        self.visit(node.third, tyBags)

    @visitor.when(StringExp)
    def visit(self, node, tyBags):
        pass

    @visitor.when(BoolExp)
    def visit(self, node, tyBags):
        pass

    @visitor.when(IntExp)
    def visit(self, node, tyBags):
        pass

    @visitor.when(IdExp)
    def visit(self, node, tyBags):
        pass

    @visitor.when(NewType)
    def visit(self, node, tyBags):
        pass


class BagsReducer:
    def __init__(self, tyBags, context, errors=[]):
        self.current_type = None
        self.current_method = None
        self.context = context
        self.errors = errors
        self.tyBags = tyBags
        self.change = True

    @visitor.on("node")
    def visit(self, node, tyBags, restriction):
        pass

    @visitor.when(Program)
    def visit(self, node, tyBags=None, restriction=None):

        while self.change:
            self.change = False

            for cool_class in node.cool_class_list:
                self.visit(cool_class, self.tyBags, [])

        return self.tyBags

    @visitor.when(CoolClass)
    def visit(self, node, tyBags, restriction):
        self.current_type = self.context.get_type(node.id)
        tyBags = tyBags.children[node]

        for feat in node.feature_list:
            self.visit(feat, tyBags, [])
        self.current_type = None

    @visitor.when(AttrDecl)
    def visit(self, node, tyBags, restriction):
        if node.body is None:
            return
        else:
            self.change = (
                tyBags.reduce_bag(node, self.visit(node.body, tyBags, []))
            ) or self.change

    @visitor.when(FuncDecl)
    def visit(self, node, tyBags, restriction):
        pass
        self.current_method = self.current_type.get_method(node.id)
        method_tyBags = tyBags.children[node]

        return_types = self.visit(node.body, method_tyBags, [])

        self.change = method_tyBags.reduce_bag(node, return_types) or self.change

        self.current_method = None

    @visitor.when(Assign)
    def visit(self, node, tyBags, restriction):
        types = self.visit(node.value, tyBags, [])

        self.change = tyBags.reduce_bag(node, types) or self.change
        return tyBags.find_variable(node.id)

    @visitor.when(Dispatch)
    def visit(self, node, tyBags, restriction):

        exp_type = self.context.types[self.visit(node.exp, tyBags, [])[0]]

        for arg in node.exp_list:
            arg_types = self.visit(arg, tyBags, [])
            self.change = tyBags.reduce_bag(arg, arg_types) or self.change

        while tyBags.parent is not None:
            tyBags = tyBags.parent

        for _, ty in tyBags.children.items():

            if ty.vars["self"][0] == exp_type.name:
                tyBags = ty
                break

        return tyBags.find_variable(node.id)

    # TODO
    @visitor.when(StaticDispatch)
    def visit(self, node, tyBags, restriction):
        pass

    @visitor.when(LetIn)
    def visit(self, node, tyBags, restriction):
        pass
        let_tyBags = tyBags.children[node]
        decl_list, exp = node.decl_list, node.exp

        for idx, _type, expx in decl_list:
            typex = self.context.get_type(_type)

            if expx is not None:
                self.change = (
                    tyBags.reduce_bag(node, self.visit(expx, tyBags, [])) or self.change
                )

        let_types = self.visit(exp, let_tyBags, [])

        return let_types

    # TODO
    @visitor.when(Case)
    def visit(self, node, tyBags, restriction):
        pass
        _ = self.visit(node.exp, tyBags, [])
        return_types = []
        ances_type = None

        for idx, typex, case_exp in node.case_list:

            new_tyBags = tyBags.children[case_exp]

            typex = self.context.get_type(typex)

            static_types = self.visit(case_exp, new_tyBags, [])

            if len(static_types) == 0:
                ances_type = get_common_ancestor(
                    ances_type, self.context.get_type[static_types[0]], self.context
                )

            else:
                return_types = set.union(set(return_types), set(static_types))

        return set.union(set(return_types), set([ances_type.name]))

    @visitor.when(Block)
    def visit(self, node, tyBags, restriction):
        l = []
        for exp in node.expr_list[0 : len(node.expr_list) - 1]:
            exp_types = self.visit(exp, tyBags, l)

        last = node.expr_list[len(node.expr_list) - 1]
        exp_types = self.visit(last, tyBags, restriction)
        if len(restriction) > 0:
            tyBags.reduce_bag(last, restriction)

        return exp_types

    @visitor.when(Not)
    def visit(self, node, tyBags, restriction):
        _ = self.visit(node.exp, tyBags, [])

        return [BoolType().name]

    # TODO
    @visitor.when(Tilde)
    def visit(self, node, tyBags, restriction):
        pass

    @visitor.when(IsVoid)
    def visit(self, node, tyBags, restriction):
        _ = self.visit(node.exp, tyBags, [])
        return [BoolType().name]

    @visitor.when(ParenthExp)
    def visit(self, node, tyBags, restriction):
        self.visit(node.exp, tyBags, [])

    def arith(self, node, tyBags):

        _ = self.visit(node.left, tyBags, [IntType().name])
        _ = self.visit(node.right, tyBags, [IntType().name])
        self.change = tyBags.reduce_bag(node.left, [IntType().name]) or self.change
        self.change = tyBags.reduce_bag(node.right, [IntType().name]) or self.change
        return [IntType().name]

    @visitor.when(Plus)
    def visit(self, node, tyBags, restriction):
        return self.arith(node, tyBags)

    @visitor.when(Minus)
    def visit(self, node, tyBags, restriction):
        return self.arith(node, tyBags)

    @visitor.when(Div)
    def visit(self, node, tyBags, restriction):
        return self.arith(node, tyBags)

    @visitor.when(Mult)
    def visit(self, node, tyBags, restriction):
        return self.arith(node, tyBags)

    def comp(self, node, tyBags):
        _ = self.visit(node.left, tyBags, [])
        _ = self.visit(node.right, tyBags, [])
        return [BoolType().name]

    @visitor.when(Leq)
    def visit(self, node, tyBags, restriction):
        return self.comp(node, tyBags)

    @visitor.when(Eq)
    def visit(self, node, tyBags, restriction):
        return self.comp(node, tyBags)

    @visitor.when(Le)
    def visit(self, node, tyBags, restriction):
        return self.comp(node, tyBags)

    @visitor.when(WhileLoop)
    def visit(self, node, tyBags, restriction):
        pass
        _ = self.visit(node.left, tyBags, [BoolType().name])
        _ = self.visit(node.right, tyBags, [])

        return [self.context.get_type("Object").name]

    @visitor.when(IfThenElse)
    def visit(self, node, tyBags, restriction):
        pass
        _ = self.visit(node.first, tyBags, [BoolType().name])
        then_types = self.visit(node.second, tyBags, [])
        else_types = self.visit(node.third, tyBags, [])

        inters = intersection(then_types, else_types)

        if len(inters) > 0:
            return inters

        return list(set.union(set(then_types), set(else_types)))

    @visitor.when(StringExp)
    def visit(self, node, tyBags, restriction):
        pass
        return [StringType().name]

    @visitor.when(BoolExp)
    def visit(self, node, tyBags, restriction):
        pass
        return [BoolType().name]

    @visitor.when(IntExp)
    def visit(self, node, tyBags, restriction):
        pass
        return [IntType().name]

    @visitor.when(IdExp)
    def visit(self, node, tyBags, restriction):
        return tyBags.find_variable(node.id)

    @visitor.when(NewType)
    def visit(self, node, tyBags, restriction):
        return [node.type]

