# -*- coding: utf-8 -*-
"""
Utilities related to logging.
"""
import logging
import os


def setup_logger(
    output=None, label="nessai", log_level="WARNING", filehandler_kwargs=None
):
    """
    Setup the logger.

    Based on the implementation in Bilby:
    https://git.ligo.org/lscsoft/bilby/-/blob/master/bilby/core/utils/log.py

    Parameters
    ----------
    output : str, optional
        Path of to output directory.
    label : str, optional
        Label for this instance of the logger.
    log_level : {'ERROR', 'WARNING', 'INFO', 'DEBUG'}, optional
        Level of logging passed to logger.
    filehandler_kwargs : dict, optional
        Keyword arguments for configuring the FileHandler. See logging
        documentation for details.

    Returns
    -------
    :obj:`logging.Logger`
        Instance of the Logger class.
    """
    from .. import __version__ as version

    if type(log_level) is str:
        try:
            level = getattr(logging, log_level.upper())
        except AttributeError:
            raise ValueError("log_level {} not understood".format(log_level))
    else:
        level = int(log_level)

    logger = logging.getLogger("nessai")
    logger.setLevel(level)

    if (
        any([type(h) == logging.StreamHandler for h in logger.handlers])
        is False
    ):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(name)s %(levelname)-8s: %(message)s",
                datefmt="%m-%d %H:%M",
            )
        )
        stream_handler.setLevel(level)
        logger.addHandler(stream_handler)

    if any([type(h) == logging.FileHandler for h in logger.handlers]) is False:
        if label:
            if output:
                if not os.path.exists(output):
                    os.makedirs(output, exist_ok=True)
            else:
                output = "."
            log_file = os.path.join(output, f"{label}.log")
            if filehandler_kwargs is None:
                filehandler_kwargs = {}
            file_handler = logging.FileHandler(log_file, **filehandler_kwargs)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)-8s: %(message)s", datefmt="%H:%M"
                )
            )

            file_handler.setLevel(level)
            logger.addHandler(file_handler)

    for handler in logger.handlers:
        handler.setLevel(level)

    logger.info(f"Running Nessai version {version}")

    return logger
