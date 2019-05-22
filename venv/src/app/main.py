import threading

from sao.ReadStream import ReadStream
from utilities.Logger import Logger

logger = Logger(level="INFO").get_logger()
logger.info("*** Starting application ****")

t1 = threading.Thread(target=ReadStream)
t1.start()
