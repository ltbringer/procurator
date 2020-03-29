"""
Setup coloredlogs
"""
import logging
import coloredlogs


L = logging.getLogger("Plute")
fmt = "%(asctime)s:%(msecs)03d %(name)s [%(filename)s:%(lineno)s] %(levelname)s %(message)s"
coloredlogs.install(level="INFO", logger=L, fmt=fmt)
