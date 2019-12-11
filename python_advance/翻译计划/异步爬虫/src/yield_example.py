import typing
import time


def a_yield() -> typing.Generator:
    print('start generator!')
    res = 'first step'
    print(res)
    send_data = yield res.split()[0]  # first stop ='s right
    res = 'second step to send'
    print(f'res: {res}, send data: {send_data}')

    send_data = yield res.split()[0]  # second stop ='s right
    res = 'third step'
    print(f'res: {res}, send data: {send_data}')

    yield res.split()[0]  # third stop ='s right
    res = 'last step'
    print(res)
    return 'generator over!'


def print_yield_data(data: str):
    print(f'from generator get data:\n{data}')
    print('-' * 50)
    time.sleep(3)


if __name__ == '__main__':
    test_generator_function = a_yield()
    yield_data = test_generator_function.send(None)  # 第一次必须发送 None
    # # yield_data = test_generator_function.send(1)  # 第一次必须发送 None
    print_yield_data(yield_data)
    yield_data = test_generator_function.send('hi generator!')  # resume generator
    print_yield_data(yield_data)
    yield_data = next(test_generator_function)  # resume generator
    print_yield_data(yield_data)
    try:
        next(test_generator_function)  # resume generator
    except StopIteration as e:
        print("return data:", e, sep='\n')
