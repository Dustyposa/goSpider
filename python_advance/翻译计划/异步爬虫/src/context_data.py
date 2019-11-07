import dis


def foo():
    bar()


def bar():
    pass


dis.dis(foo)
