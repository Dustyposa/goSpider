import logging
from types import FrameType
from typing import cast

from loguru import logger


# print(logging.getLogger("uvicorn.asgi"))
# print(logging.getLogger("uvicorn.access"))


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        print(dir(record))
        # Get corresponding Loguru level if it exists
        # try:
        #     level = logger.level(record.levelname).name
        # except ValueError:
        #     level = str(record.levelno)
        # #
        # # # Find caller from where originated the logged message
        # frame, depth = logging.currentframe(), 2
        # while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
        #     frame = cast(FrameType, frame.f_back)
        #     depth += 1
        #
        record.msg += " test"
        print(record.getMessage())
        # # logger.log(20, record.getMessage())
        # logger.opt(depth=2, exception=record.exc_info)
        # logger.opt(depth=2, exception=record.exc_info).log(
        #     self.level,
        #     record.getMessage() + "test",
        # record.msg,
        # )
        # ...
        # self.flush()



# logger.add(sys.stdout, format="{time:HH:mm:ss!UTC}", serialize=True, enqueue=True)
# logger.add(log_handler, format="{time:HH:mm:ss!UTC}", serialize=True, enqueue=True)
logger.add(InterceptHandler("INFO"))

logger.info("this is a logger")
