"""

"""
# ------------------------------------------------------- #
# imports
# ------------------------------------------------------- #
from threading import Thread
import time
from waitress import serve

from flask_definitions import *
import endpoints.unknown
import endpoints.user_handeling
import endpoints.general
import endpoints.web
import endpoints.aes


# ------------------------------------------------------- #
# functions
# ------------------------------------------------------- #


def run():
    serve(app, host='0.0.0.0', port=8080, threads=100, connection_limit=2000, cleanup_interval=50, channel_timeout=190,)


def keep_alive():
    try:
        if dev_env == "true":
            logger.info("DEV api started.")
        else:
            logger.info("API started.")
        t = Thread(target=run)
        t.daemon = True
        t.start()
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print('Received keyboard interrupt, quitting threads.')
        logger.info("API stopped.")


# ------------------------------------------------------- #
# global variables
# ------------------------------------------------------- #


# ------------------------------------------------------- #
# main
# ------------------------------------------------------- #
if dev_env == "true":
    mongo.setup(mongo_host, mongo_db_dev, mongo_user_collection, mongo_aes_collection)
else:
    mongo.setup(mongo_host, mongo_db, mongo_user_collection, mongo_aes_collection)
session_manager.setup()
keep_alive()