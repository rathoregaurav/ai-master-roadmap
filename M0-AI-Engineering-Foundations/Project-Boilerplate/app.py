import logging

try:
    from loguru import logger
except ModuleNotFoundError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("ai-foundations")


def main() -> None:
    logger.info("AI engineering environment is ready.")


if __name__ == "__main__":
    main()
