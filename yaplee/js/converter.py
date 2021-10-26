import inspect
import ast
import textwrap

class JSFunc(object):
    def __init__(self, func, initial_scope={}):
        self._orig = func
        self._initial_scope = initial_scope

        source_code = self.__function_replacement(inspect.getsource(func))
        code_ast = ast.parse(textwrap.dedent(source_code))
        self._code = code_ast.body[0].body

        empty_scope = _Scope()
        initial_code_py = '\n'.join(
            "%s = %s" % (k, _to_str(v, empty_scope))
            for (k, v) in self._initial_scope.items()
        )

        if initial_code_py:
            initial_code_ast = ast.parse(textwrap.dedent(initial_code_py))
            self._initial_code_js = _to_str(
                initial_code_ast.body, empty_scope) + ";"
        else:
            self._initial_code_js = ""


    def __str__(self):
        return self._initial_code_js + _to_str(
            self._code,
            _Scope(self._initial_scope)
        )

    def __function_replacement(self, source):
        replace_to = {
            '.upper()': '.toUpperCase()'
        }
        for key, value in replace_to.items():
            source = source.replace(key, value)
        return source

    def __call__(self, *args, **kwargs):
        return self._orig(*args, **kwargs)


def _parse_assign(node, scope):
    value = _to_str(node.value, scope)
    target_iter = _to_str_iter(node.targets, scope)

    assignments = []

    for t in target_iter:
        is_in_scope = t in scope
        is_field_assignment = '.' in t
        is_arr_assignment = '[' in t

        if is_in_scope or is_field_assignment or is_arr_assignment:
            assignments.append(f"{t} = {value}")
        else:
            scope.add(t)
            assignments.append(f"var {t} = {value}")

    return ";".join(assignments)


def _parse_bool_op(node, scope):
    op = _to_str(node.op, scope)
    return op.join(_to_str_iter(node.values, scope))


def _parse_compare(node, scope):
    ops = _to_str_iter(node.ops, scope)
    comparators = _to_str_iter(node.comparators, scope)
    ops_comps = zip(ops, comparators)
    return "%s %s" % (
        _to_str(node.left, scope),
        " ".join("%s %s" % oc for oc in ops_comps),
    )


def _parse_call(node, scope):
    func = _to_str(node.func, scope)
    args = _to_str_iter(node.args, scope)
    return "%s(%s)" % (
        func,
        ", ".join(args),
    )


def _parse_dict(node, scope):
    keys = _to_str_iter(node.keys, scope)
    values = _to_str_iter(node.values, scope)
    kvs = zip(keys, values)
    return "{%s}" % ", ".join("%s: %s" % kv for kv in kvs)


def _parse_function_def(node, scope):
    new_scope = scope.enter_new()
    new_scope.add(x.arg for x in node.args.args)

    return "function %(name)s(%(args)s) {\n%(body)s\n}" % {
        "name": node.name,
        "args": _to_str(node.args, new_scope),
        "body": _to_str(node.body, new_scope),
    }


def _parse_lambda(node, scope):
    new_scope = scope.enter_new()
    new_scope.add(x.arg for x in node.args.args)

    return "((%(args)s) => (%(body)s))" % {
        "args": _to_str(node.args, new_scope),
        "body": _to_str(node.body, new_scope),
    }


def _parse_list(node, scope):
    return "[%s]" % ", ".join(_to_str(x, scope) for x in node.elts)


def _parse_arguments(node, scope):
    return ", ".join(x.arg for x in node.args)


_PARSERS = {
    "FunctionDef": _parse_function_def,
    "Return": "return %(value)s",
    "Delete": "delete %(targets)s",
    "Assign": _parse_assign,
    "AugAssign": "%(target)s %(op)s= %(value)s",
    "For": "%(iter)s.forEach((%(target)s, _i) => {\n%(body)s\n})",
    "While": "while (%(test)s) {\n%(body)s\n}",
    "If": "if (%(test)s) {\n%(body)s\n} else {\n%(orelse)s\n}",
    "Raise": "throw new Error(%(exc)s)",
    "Expr": "%(value)s",
    "Pass": "",
    "BoolOp": _parse_bool_op,
    "BinOp": "(%(left)s %(op)s %(right)s)",
    "UnaryOp": "(%(op)s%(operand)s)",
    "Lambda": _parse_lambda,
    "IfExp": "(%(test)s) ? (%(body)s) : (%(orelse)s)",
    "Dict": _parse_dict,
    "Compare": _parse_compare,
    "Call": _parse_call,
    "Constant": "%(value)s",
    "Attribute": "%(value)s.%(raw_attr)s",
    "Subscript": "%(value)s[%(slice)s]",
    "Name": "%(raw_id)s",
    "List": _parse_list,
    "Index": "%(value)s",
    "And": "&&",
    "Or": "||",
    "Add": "+",
    "Sub": "-",
    "Mult": "*",
    "Div": "/",
    "Mod": "%%", 
    "LShift": "<<",
    "RShift": ">>",
    "BitOr": "|",
    "BitXor": "^",
    "BitAnd": "&",
    "Invert": "~",
    "Not": "!",
    "UAdd": "+",
    "USub": "-",
    "Eq": "===",
    "NotEq": "!==",
    "Lt": "<",
    "LtE": "<=",
    "Gt": ">",
    "GtE": ">=",
    "Break": "break",
    "Continue": "continue",
    "arguments": _parse_arguments,

    "Num": "%(n)s",
    "Str": '%(s)s',
    "Bytes": '"%(s)s"',
    "NameConstant": "%(value)s",
}


def _to_str(node, scope):
    node_type = type(node)

    if node_type is list:
        return ";\n".join(_to_str(x, scope) for x in node)

    if node is None:
        return "null"

    if node_type is str:
        return '"%s"' % node

    if node_type in (int, float):
        return str(node)

    if node_type is bool:
        return "true" if node else "false"

    if node_type.__name__ not in _PARSERS:
        raise Exception("Unsupported operation in JS: %s" % node_type)

    parser = _PARSERS[node_type.__name__]

    if type(parser) is str:
        return parser % _DictWrapper(node.__dict__, scope)

    return parser(node, scope)


class _DictWrapper(dict):
    def __init__(self, dikt, scope):
        self._dict = dikt
        self._parsed_keys = set()
        self._scope = scope

    def __getitem__(self, k):
        raw = False

        if k.startswith("raw_"):
            k = k[4:]
            raw = True

        if k not in self._parsed_keys:
            if raw:
                self._dict[k] = self._dict[k]
            else:
                self._dict[k] = _to_str(self._dict[k], self._scope)
            self._parsed_keys.add(k)

        return self._dict[k]


def _to_str_iter(arg, scope):
    return (_to_str(x, scope) for x in arg)


class _Scope(object):
    def __init__(self, parent=None):
        self._parent = parent
        self._identifiers = set()

    def enter_new(self):
        return _Scope(self)

    def add(self, identifiers):
        for x in identifiers:
            self._identifiers.add(x)

    def __contains__(self, x):
        if x in self._identifiers:
            return True

        if self._parent is not None and x in self._parent:
            return True

        return False
