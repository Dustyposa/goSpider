import logging
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

from types import FrameType
from typing import cast, Dict, Any
from pprint import pprint

from loguru import logger
from orjson import dumps


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


    # def rotation_filename(self, path: str):
    #     return "_".join(path.split(".")) + ".log"


def format_record(record: Dict[str, Any]) -> str:
    return record["message"]


# handlers = [{"sink": CustomAppHandler("test.log")}]
handlers = [
    {"sink": sys.stderr, "level": logging.INFO},
    {"sink": CustomAppHandler("gunicorn_info", when="M"), "format": format_record}
    # {"sink": "asd.log", "level": logging.INFO, "rotation": "1 minute"}
]

#
logger.configure(handlers=handlers)
logger.add(sink=CustomAppHandler("test.log", when="M"), format=format_record)
# logger.configure(handlers=handlers)
logger.info("this is a logger， 加上中文")
import time
time.sleep(2 * 45)

logger.info("this is a logger2222222， 加上中文")
