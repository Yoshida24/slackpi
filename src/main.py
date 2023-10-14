from modules.logger.logger import logger
from modules.bolt.bolt_wrapper import BoltWrapper
from route.route import listen


if __name__ == "__main__":
    BoltWrapper(listen).start()
