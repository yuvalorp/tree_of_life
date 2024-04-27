import logging

logging.basicConfig(
    filename="logs.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m-%d %H:%M",
)
