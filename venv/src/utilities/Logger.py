import logging


class Logger:

    def __init__(self, level="DEBUG",
                 file_name="mat_logger",
                 log_path="C:\\Users\\Chris Solimo\\PycharmProjects\\MAT_coding_challenge_solution\\venv\\logs",
                 logger_name="mat_logger"):
        log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)

        file_handler = logging.FileHandler("{0}/{1}.log".format(log_path, file_name))
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


