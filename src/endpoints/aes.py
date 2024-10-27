from flask_definitions import *
import os


@app.route('/api/v1/aes', methods=['GET'], strict_slashes=False)
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


@app.route('/api/v1/aes/<game>', methods=['GET', 'POST'], strict_slashes=False)
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
            try:
                token = data["token"]
                ret_val = mongo.validate_token(token)
            except KeyError:
                if 'session' in request.cookies:
                    user_id = session_manager.get_user_id(request.cookies['session'])
                    if user_id is None:
                        return jsonify({"status": "error", "message": "Not Authenticated"}), 401
                else:
                    return jsonify({"status": "error", "message": "Not Authenticated"}), 401
                ret_val = {"status": "success", "message": "Token found", "user_id": user_id}
            if ret_val["status"] == "error":
                return jsonify(ret_val), 400
            mainKey = data["mainKey"]
            if not mainKey.startswith("0x") or len(mainKey) != 66:
                return jsonify({"status": "error", "message": "Invalid Main Key"}), 400
            dynamicKeys = data["dynamicKeys"]
            if dynamicKeys:
                for key_object in dynamicKeys:
                    if not key_object["key"].startswith("0x") or len(key_object["key"]) != 66:
                        return jsonify({"status": "error", "message": "Invalid AES Key in dynamicKeys"}), 400
                    if key_object["name"].endswith(".pak") or key_object["name"].endswith(".utoc"):
                        if not "name" in key_object or not "key" in key_object or not "guid" in key_object:
                            return jsonify({"status": "error", "message": "Missing required parameter in dynamicKeys"}), 400
                    else:
                        return jsonify({"status": "error", "message": "Invalid AES Name in dynamicKeys"}), 400
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
