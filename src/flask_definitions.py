from flask import Flask, jsonify, request, send_from_directory, abort, render_template, url_for, redirect
from logic.setup_handlers import load_config
from logic.global_handler import sanitize_input, ip_handler, session_manager
from logic.mongodb_handler import mongo
from logic.webhook_handler import discord_webhook
from logic.date_handler import get_current_date
import logging
from logic.logging_handler import setup_logger, log_exception
import json
import os

app = Flask(__name__)
logger = setup_logger('AES_API', logging.DEBUG)

config = load_config()
version = config['global']['version']
name = config['global']['name']
mongo_host = config['mongodb']['host']
mongo_db = config['mongodb']['db']
mongo_db_dev = config['mongodb']['db_dev']
mongo_aes_collection = config['mongodb']['aes_collection']
mongo_user_collection = config['mongodb']['user_collection']
use_discord = config['webhooks']['discord']['use']
discord_urls = config['webhooks']['discord']['urls']
dev_env = os.environ['DEV']
local_ip = config['local_ips']
