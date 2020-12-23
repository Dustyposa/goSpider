import logging
from logging.handlers import TimedRotatingFileHandler
from types import FrameType
from typing import cast, Dict, Any
from pprint import pprint

from loguru import logger


class CustomAppHandler(TimedRotatingFileHandler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        self.format(record)
        print(record.asctime)
        pprint(record.__dict__)
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
        # #
        # # record.msg += " test"
        # # print(record.getMessage())
        # # # logger.log(20, record.getMessage())
        # # logger.opt(depth=2, exception=record.exc_info)
        # logger.opt(depth=depth, exception=record.exc_info).log(
        #     level,
        #     record.getMessage(),
        # )
        # ...
        # self.flush()
        # logger.opt(depth=1, exception=record.exc_info).log(self.level, record.getMessage())
        print(self.stream.write("123" + self.terminator))

        pass


def format_record(record: Dict[str, Any]) -> str:
    return record["message"]


handlers = [{"sink": CustomAppHandler("test.log")}]
# handlers = [{"sink": TimedRotatingFileHandler("test.log")}]

logger.add(sink=CustomAppHandler("test.log"), format=format_record)

logger.info("this is a logger")
