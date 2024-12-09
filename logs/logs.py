import logging


logging.basicConfig(
    filename='logs/logs.log',
    encoding='utf-8',
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


def logs(report):
    logging.info(report)
