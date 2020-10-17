class TyBags:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
        self.children = {}
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.vars)

    def __str__(self):
        output = ""

        for key, value in self.vars.items():
            output += "\t" + str(key) + ":" + str(value) + "\n"
        for key, chil in self.children.items():
            output += "\n"
            try:
                output += key.id + "--->"
            except AttributeError:
                output += "let or case--->"
            output += "\n"
            output += str(chil)
        return output

    def __repr__(self):
        return str(self)

    def create_child(self, key):
        child = TyBags(self)
        self.children[key] = child
        return child

    def reduce_bag(self, node, types):
        types = list(types)

        try:
            varName = node.id
        except AttributeError:
            return False

        varTypes = list(self.find_variable(varName))

        inters = self.intercect(varTypes, types)

        if len(inters) == 0:
            if not "@error" in varTypes and not "@error" in types:
                self.modify_variable(
                    varName, list(set.union(set(varTypes), set(types))) + ["@error"]
                )
            else:
                self.modify_variable(
                    varName, list(set.union(set(varTypes), set(types)))
                )
        else:
            if "@error" in varTypes:
                self.modify_variable(
                    varName, list(set.union(set(varTypes), set(types)))
                )
            elif "@error" in types:
                self.modify_variable(varName, types)
            else:
                self.modify_variable(varName, inters)

        NewVarTypes = self.find_variable(varName)
        # ret = self.compare(varTypes, NewVarTypes)

        return not sorted(varTypes) == sorted(NewVarTypes)

    def intercect(self, var1, types):
        return list(set(var1) & set(types))

    def restict(self, var1, types):
        types = list(set(var1) & set(types))

    def increment(self, var1, types):
        types = list(set.union(set(var1), set(types)))

    def define_variable(self, name, types):
        self.vars[name] = types

    def find_variable(self, name):
        try:
            return self.vars[name]
        except KeyError:
            if self.parent is not None:
                return self.parent.find_variable(name)
            else:
                return None

    def modify_variable(self, name, types):
        try:
            _ = self.vars[name]
            self.vars[name] = types
        except KeyError:
            if self.parent is not None:
                self.parent.modify_variable(name, types)
            else:
                None

    def compare(self, s, t):
        newt = list(t)
        try:
            for elem in s:
                newt.remove(elem)
        except ValueError:
            return False
        return not newt
