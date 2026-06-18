import logging

logger = logging.getLogger("url_shortener")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler = logging.FileHandler("/logs/app.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)