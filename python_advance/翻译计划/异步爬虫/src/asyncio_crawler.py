try:
    from asyncio import JoinableQueue as Queue
except ImportError:
    # 在 Python 3.5，asyncio.JoinableQueue 并入到了 Queue
    from asyncio import Queue


