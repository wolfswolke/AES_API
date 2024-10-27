import requests


def discord_webhook(urls, data):
    if type(urls) is str:
        urls = [urls]
    for url in urls:
        requests.post(url, json=data)


def sender(url, title, description, color=790874):
    webhook_data = {
        "content": "",
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color
            }
        ],
        "attachments": []
    }
    discord_webhook(url, webhook_data)