import logging
import coloredlogs


coloredlogs.install(
    level=logging.INFO,
    fmt="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(name)s] %(message)s",
)

logger = logging.getLogger()
