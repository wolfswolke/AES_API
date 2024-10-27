# Endpoints for errors as 404, 500,...
import werkzeug

from flask_definitions import *

@app.errorhandler(404)
def page_not_found(e):
    try:
        if request.json:
            response_json = sanitize_input(request.json)
        else:
            response_json = "None"
    except werkzeug.exceptions.UnsupportedMediaType:
        response_json = "None"
    if request.path:
        response_path = sanitize_input(request.path)
    else:
        response_path = "None"
    if request.endpoint:
        response_endpoint = sanitize_input(request.endpoint)
    else:
        response_endpoint = "None"
    user_ip = ip_handler("remote")
    logger.error(f"<Path: {response_path}> "
                 f"<Endpoint: {response_endpoint}> "
                 f"<Methode: {sanitize_input(request.method)}><JSON: {response_json}>"
                 f"<IP: {user_ip}>")
    return jsonify({"error": "Page not found"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    try:
        if request.json:
            response_json = sanitize_input(request.json)
        else:
            response_json = "None"
    except werkzeug.exceptions.UnsupportedMediaType:
        response_json = "None"
    if request.path:
        response_path = sanitize_input(request.path)
    else:
        response_path = "None"
    if request.endpoint:
        response_endpoint = sanitize_input(request.endpoint)
    else:
        response_endpoint = "None"
    user_ip = ip_handler("remote")
    logger.error(f"<Path: {response_path}> "
                 f"<Endpoint: {response_endpoint}> "
                 f"<Methode: {sanitize_input(request.method)}><JSON: {response_json}>"
                 f"<IP: {user_ip}>")

    return jsonify({"error": "Internal Server Error"}), 500