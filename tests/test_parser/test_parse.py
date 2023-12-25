from project.parser.parser import dot_of_source
import inspect


def check_res(res):
    test_name = inspect.stack()[1][3]

    with open(f"tests/test_programs/{test_name}_truth.dot", "r") as truth:
        assert truth.read() == res


def test_parse_hello_world():
    program = 'print("Hello world!")'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_assign():
    program = 'x = 2\ny = 3\nreg = r"a*b"\ncfg = c"x -> y"  '
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_set():
    program = 'x = {"a", "m", 0, "n", g, u, 5}'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_load_graph():
    program = 'x = load_graph("path")'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_load_dot():
    program = 'x = load_dot("path")'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_add_start():
    program = 'x = load_dot("path")\ny = x.add_start(3)'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_add_final():
    program = 'x = load_dot("path")\ny = x.add_final(3)'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_set_start():
    program = 'x = load_dot("path")\ny = x.set_start(3)'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_set_final():
    program = 'x = load_dot("path")\ny = x.set_final(3)'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_get_reachable():
    program = 'x = load_dot("path")\ny = x.get_reachable'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_get_edges():
    program = 'x = load_dot("path")\ny = x.get_edges'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_get_labels():
    program = 'x = load_dot("path")\ny = x.get_labels'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_get_labels():
    program = 'x = load_dot("path")\ny = x.get_labels'
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_map():
    program = "x = map({(a, b) -> a.add_final(b)}, {0, 1, 2})"
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_filter():
    program = "x = filter({(a, b) -> a.add_final(b)}, {0, 1, 2})"
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_union():
    program = "x = x.union(y)"
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_intersect():
    program = "x = x.intersect(z)"
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_concat():
    program = "x = x.concat(y)"
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_star():
    program = "x = x*"
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_contains():
    program = "x = x in x"
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)


def test_parse_complex():
    program = "tests/test_programs/prog1.pql"
    with open(program) as source:
        program = source.read()
    dot = dot_of_source(program)
    dot_string = dot.to_string()

    check_res(dot_string)
