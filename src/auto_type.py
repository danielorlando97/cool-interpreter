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
)


class AutoType(Type):
    def __init__(self):
        Type.__init__(self, "AUTO_TYPE")

