from flask_definitions import *


@app.route('/api/v1/aes/', methods=['GET'])
def get_all_aes():
    try:
        aes_list = mongo.get_all_aes()
        if not aes_list:
            logger.error("Failed to get all AES Items")
            return jsonify([]), 404
        return_list = []
        for aes_item in aes_list:
            return_list.append(aes_item["game"])
        return render_template('game_list.html', games=return_list)
    except Exception as e:
        log_exception(logger, e)
        return jsonify([]), 500


@app.route('/api/v1/aes/<game>', methods=['GET', 'POST'])
def get_aes(game):
    if not game:
        return jsonify({"status": "error", "message": "Game name not specified."}), 400
    game = sanitize_input(game)
    if request.method == 'GET':
        try:
            aes_list = mongo.get_aes_by_game(game)
            if not aes_list:
                logger.error(f"Tried to get unknown game: {game}")
                return jsonify([]), 404
            aes_list = aes_list[0]
            return jsonify({
                "mainKey": aes_list["mainKey"],
                "dynamicKeys": aes_list["dynamicKeys"],
                "version": aes_list["version"],
                "unloaded": []
            }), 200
        except Exception as e:
            log_exception(logger, e)
            return jsonify([]), 500
    if request.method == 'POST':
        try:
            data = request.get_json()
            mainKey = data["mainKey"]
            if not mainKey.startswith("0x") or len(mainKey) != 66:
                return jsonify({"status": "error", "message": "Invalid Main Key"}), 400
            dynamicKeys = data["dynamicKeys"]
            token = data["token"]
            ret_val = mongo.validate_token(token)
            if ret_val["status"] == "error":
                return jsonify(ret_val), 400
            if dynamicKeys:
                for key_object in dynamicKeys:
                    for aes_keys in key_object:
                        if not aes_keys.startswith("0x") or len(aes_keys) != 66:
                            return jsonify({"status": "error", "message": "Invalid AES Key in dynamicKeys"}), 400
                        if not aes_keys["name"].endswith(".pak"):
                            return jsonify({"status": "error", "message": "Invalid AES Name in dynamicKeys"}), 400
                        if aes_keys not in ["guid", "key", "name"]:
                            return jsonify({"status": "error", "message": "Missing required parameter in dynamicKeys"}), 400
            else:
                dynamicKeys = []
            ret = mongo.add_aes(mainKey, game, dynamicKeys, ret_val["user_id"])
            if not ret:
                return jsonify({"status": "error", "message": "Internal Server Error"}), 500
            elif ret["status"] == "error":
                return jsonify(ret), 400
            return jsonify({"status": "success", "message": "AES Item added"}), 200
        except Exception as e:
            log_exception(logger, e)
            return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    return jsonify({"status": "error", "message": "Invalid Request Method"}), 405
