def gen_fn():
    result = yield 1
    print(f'result of yield : {result}')
    result2 = yield 2
    print(f'result of 2nd yield : {result2}')
    return 'done'


if __name__ == '__main__':
    gen = gen_fn()
    print(gen.send(None))
    print(gen.send("first yield"))
    print(gen.send("2nd yield"))


