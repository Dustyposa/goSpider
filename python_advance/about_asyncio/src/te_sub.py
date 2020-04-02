import asyncio


async def async_readline(proc: asyncio.subprocess.Process):
    while proc.returncode is None and not proc.stdout.at_eof():
        out = await proc.stdout.readline()
        print(F"OUT:{out}")


async def async_in(proc: asyncio.subprocess.Process):
    while proc.returncode is None:
        await asyncio.sleep(1)  # 人为阻塞
        proc.stdin.write("321\n".encode("u8"))


async def main():
    proc = await asyncio.create_subprocess_exec(
        *["python3", "ru.py"],
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={
            "PYTHONUNBUFFERED": '1',
        }
    )
    # print(f"return code: {proc.returncode}")
    tasks = [
        asyncio.create_task(async_readline(proc)),
        # asyncio.create_task(async_in(proc)),
    ]
    done, pending = await asyncio.wait(
        tasks,
        timeout=4,
        return_when=asyncio.FIRST_COMPLETED
    )
    [i.cancel() for i in pending]
    print(f"done: {[i.result() for i in done]}")
    # print(f"pending: {pending}")
    # print(proc.returncode)
    # proc.kill()

    # proc.terminate()
    # await proc.wait()
    print(await proc.communicate())

    print(proc.returncode)


if __name__ == "__main__":
    asyncio.run(main())
