import src.visitor as visitor
from src.utils import get_common_ancestor

from src.semantic import (
    SemanticError,
    Attribute,
    Method,
    Type,
    VoidType,
    ErrorType,
    Context,
    Scope,
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

WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'
INVALID_COMPARISSON = 'Comparison is not defined between "%s" and "%s".'
BOOL_EXPECTED = 'Was expected a bool, not "%s".'
STATIC_DISPATCH_ERROR = 'Type "%s" is not descendent of "%s"'


class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(Program)
    def visit(self, node):
        self.context = Context()
        self.context.create_type("Object")
        self.context.types["Int"] = IntType()
        self.context.types["Void"] = VoidType()
        self.context.types["Bool"] = BoolType()
        self.context.types["String"] = StringType()
        self.context.types["AUTO_TYPE"] = AutoType()
        for cl in node.cool_class_list:
            self.visit(cl)

    @visitor.when(CoolClass)
    def visit(self, node):
        try:
            self.context.create_type(node.name)
        except SemanticError as err:
            self.errors.append(err.text)


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(Program)
    def visit(self, node):
        for cool_class in node.cool_class_list:
            self.visit(cool_class)

    @visitor.when(CoolClass)
    def visit(self, node):
        self.current_type = self.context.get_type(node.name)
        if node.inherit is not None:
            try:
                _type = self.context.get_type(node.inherit)
            except SemanticError as error:
                _type = ErrorType()
                self.errors.append(error.text)
            parent_type = _type

            try:
                self.current_type.set_parent(parent_type)
            except SemanticError as e:
                self.errors.append(e.text)
        for feat in node.feature_list:
            self.visit(feat)

    @visitor.when(AttrDecl)
    def visit(self, node):
        try:
            _type = self.context.get_type(node.type)
        except SemanticError as error:
            _type = ErrorType()
            self.errors.append(error.text)

        try:
            self.current_type.define_attribute(node.id, _type)
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(FuncDecl)
    def visit(self, node):
        param_names = [param.id for param in node.params]
        param_types_names = [param.type for param in node.params]
        param_types = []
        for p in param_types_names:
            try:
                _type = self.context.get_type(p)
            except SemanticError as error:
                _type = ErrorType()
                self.errors.append(error.text)
            param_types.append(_type)

        try:
            _type = self.context.get_type(node.type)
        except SemanticError as error:
            _type = ErrorType()
            self.errors.append(error.text)
        return_type = _type

        try:
            self.current_type.define_method(
                node.id, param_names, param_types, return_type
            )
        except SemanticError as e:
            self.errors.append(e.text)


class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(Program)
    def visit(self, node, scope=None):
        scope = Scope()
        for cool_class in node.cool_class_list:
            self.visit(cool_class, scope.create_child())
        return scope

    @visitor.when(CoolClass)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.name)
        scope.define_variable("self", self.current_type)
        for attr in self.current_type.attributes:
            scope.define_variable(attr.name, attr.type)

        for feat in node.feature_list:
            self.visit(feat, scope)
        self.current_type = None

    @visitor.when(AttrDecl)
    def visit(self, node, scope):
        pass

    @visitor.when(FuncDecl)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)
        method_scope = scope.create_child()

        for pname, ptype in zip(
            self.current_method.param_names, self.current_method.param_types
        ):
            method_scope.define_variable(pname, ptype)

        return_type = self.visit(node.body, method_scope)

        if not return_type.conforms_to(self.current_method.return_type):
            self.errors.append(
                INCOMPATIBLE_TYPES
                % (return_type.name, self.current_method.return_type.name)
            )

        if self.current_type.parent is not None:
            try:
                parent_method = self.current_type.parent.get_method(
                    self.current_method.name
                )
                if parent_method != self.current_method:
                    self.errors.append(WRONG_SIGNATURE % (parent_method.name, "parent"))
            except SemanticError:
                pass

        self.current_method = None

    @visitor.when(Dispatch)
    def visit(self, node, scope):
        exp_type = self.visit(node.exp_type, scope)
        try:
            method = exp_type.get_method(node.id)
        except SemanticError as e:
            self.errors.append(e.text)
            return ErrorType()

        if len(node.exp_list) != len(method.param_names):
            self.errors.append(
                "Method %s takes %d arguments but %d were given"
                % (method.name, len(method.param_names), len(node.exp_list))
            )

        for arg, ptype in zip(node.exp_list, method.param_types):
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms_to(ptype):
                self.errors.append(INCOMPATIBLE_TYPES % (arg_type.name, ptype.name))

        return method.return_type

    @visitor.when(StaticDispatch)
    def visit(self, node, scope):
        exp_type = self.visit(node.exp, scope)
        try:
            method = exp_type.get_method(node.id)
        except SemanticError as e:
            self.errors.append(e.text)
            return ErrorType()

        if len(node.exp_list) != len(method.param_names):
            self.errors.append(
                "Method %s takes %d arguments but %d were given"
                % (method.name, len(method.param_names), len(node.exp_list))
            )

        for arg, ptype in zip(node.exp_list, method.param_types):
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms_to(ptype):
                self.errors.append(INCOMPATIBLE_TYPES % (arg_type.name, ptype.name))

        try:
            specific_type = self.context.get_type(node.specific_type)
            if not exp_type.conforms_to(specific_type):
                self.errors.append(STATIC_DISPATCH_ERROR % (exp_type, specific_type))
        except SemanticError as e:
            self.errors.append(e.text)

        return method.return_type

    @visitor.when(LetIn)
    def visit(self, node, scope):
        let_scope = scope.create_child()
        decl_list, exp = node.decl_list, node.exp

        for idx, _type, expx in decl_list:
            try:
                typex = self.context.get_type(_type)
            except SemanticError as e:
                typex = ErrorType()
                self.errors.append(e.text)

            if expx is None:
                right_type = typex
            else:
                right_type = self.visit(expx, scope)

            if not right_type.conforms_to(typex):
                self.errors.append(INCOMPATIBLE_TYPES % (right_type, typex))

            let_scope.define_variable(idx, typex)

        let_type = self.visit(exp, let_scope)

        return let_type

    # TODO
    @visitor.when(Case)
    def visit(self, node, scope):
        _ = self.visit(node.exp, scope)
        return_type = None
        first = True

        for idx, _type, case_exp in node.case_list:
            try:
                typex = self.context.get_type(_type)
            except SemanticError as e:
                typex = ErrorType()
                self.errors.append(e.text)

            new_scope = scope.parent
            new_scope.define_variable(idx, typex)
            static_type = self.visit(case_exp, new_scope)

            if first:
                return_type = static_type
                first = False
            else:
                return_type = get_common_ancestor(
                    return_type, static_type, self.context
                )

        return return_type

    @visitor.when(Block)
    def visit(self, node, scope):

        for exp in node.expr_list:
            exp_type = self.visit(exp, scope)
        return exp_type

    @visitor.when(Assign)
    def visit(self, node, scope):
        if node.id == "self":
            self.errors.append(SELF_IS_READONLY)

        var = scope.find_variable(node.id)
        if var is None:
            self.errors.append(
                VARIABLE_NOT_DEFINED % (node.id, self.current_method.name)
            )
            var_type = ErrorType()
        else:
            var_type = var.type

        right_type = self.visit(node.value, scope)
        if not right_type.conforms_to(var_type):
            self.errors.append(INCOMPATIBLE_TYPES % (right_type.name, var_type.name))

        return var_type

    # TODO
    @visitor.when(Not)
    def visit(self, node, scope):
        exp_type = self.visit(node.exp, scope)
        bool_type = self.context.get_type("Bool")
        if exp_type != bool_type:
            self.errors.append(BOOL_EXPECTED % (exp_type))

        return bool_type

    # TODO
    @visitor.when(Tilde)
    def visit(self, node, scope):
        pass

    @visitor.when(IsVoid)
    def visit(self, node, scope):
        _ = self.visit(node.exp, scope)
        return self.context.get_type("Bool")

    @visitor.when(ParenthExp)
    def visit(self, node, scope):
        return self.visit(node.exp, scope)

    def arith(self, node, scope):
        int_type = IntType()
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms_to(int_type) or not right_type.conforms_to(int_type):
            self.errors.append(INVALID_OPERATION % (left_type.name, right_type.name))
        return int_type

    @visitor.when(Plus)
    def visit(self, node, scope):
        return self.arith(node, scope)

    @visitor.when(Minus)
    def visit(self, node, scope):
        return self.arith(node, scope)

    @visitor.when(Div)
    def visit(self, node, scope):
        return self.arith(node, scope)

    @visitor.when(Mult)
    def visit(self, node, scope):
        return self.arith(node, scope)

    def comp(self, node, scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if left_type != right_type:
            self.errors.append(INVALID_COMPARISSON % (left_type.name, right_type.name))
        return self.context.get_type("Bool")

    @visitor.when(Leq)
    def visit(self, node, scope):
        return self.comp(node, scope)

    @visitor.when(Eq)
    def visit(self, node, scope):
        return self.comp(node, scope)

    @visitor.when(Le)
    def visit(self, node, scope):
        return self.comp(node, scope)

    @visitor.when(WhileLoop)
    def visit(self, node, scope):
        conditional_type = self.visit(node.left, scope)
        _ = self.visit(node.right, scope)

        if conditional_type != self.context.get_type("Bool"):
            self.errors.append(BOOL_EXPECTED % (conditional_type))

        return self.context.get_type("Object")

    # TODO
    @visitor.when(IfThenElse)
    def visit(self, node, scope):
        conditional_type = self.visit(node.first, scope)
        then_type = self.visit(node.second, scope)
        else_type = self.visit(node.third, scope)
        bool_type = self.context.get_type("Bool")

        if conditional_type != bool_type:
            self.errors.append(BOOL_EXPECTED % (conditional_type))

        return get_common_ancestor(then_type, else_type, self.context)

    @visitor.when(StringExp)
    def visit(self, node, scope):
        return StringType()

    @visitor.when(BoolExp)
    def visit(self, node, scope):
        return BoolType()

    @visitor.when(IntExp)
    def visit(self, node, scope):
        return IntType()

    @visitor.when(IdExp)
    def visit(self, node, scope):
        var = scope.find_variable(node.lex)
        if var is None:
            self.errors.append(
                VARIABLE_NOT_DEFINED % (node.lex, self.current_method.name)
            )
            return ErrorType()
        return var.type

