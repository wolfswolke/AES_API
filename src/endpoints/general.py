from flask_definitions import *


@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"}), 200


@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static' 'files'), 'robots.txt')


@app.route('/browserconfig.xml')
def browserconfig():
    return send_from_directory(os.path.join(app.root_path, 'static' 'files'), 'browserconfig.xml')


@app.route('/site.webmanifest')
def site_webmanifest():
    return send_from_directory(os.path.join(app.root_path, 'static', 'files'), 'site.webmanifest')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/android-chrome-192x192.png')
def android_chrome_192():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'android-chrome-192x192.png',
                               mimetype='image/png')


@app.route('/android-chrome-512x512.png')
def android_chrome_512():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'android-chrome-512x512.png',
                               mimetype='image/png')


@app.route('/apple-touch-icon.png')
def apple_touch_icon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'apple-touch-icon.png',
                               mimetype='image/png')


@app.route('/mstile-150x150.png')
def mstile_150():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'mstile-150x150.png',
                               mimetype='image/png')


@app.route('/favicon-16x16.png')
def favicon_16():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'favicon-16x16.png',
                               mimetype='image/png')


@app.route('/favicon-32x32.png')
def favicon_32():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'favicon-32x32.png',
                               mimetype='image/png')


@app.route('/safari-pinned-tab.svg')
def safari_pinned_tab():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'safari-pinned-tab.svg',
                               mimetype='image/svg+xml')
