import threading
import requests
import logging


log = logging.getLogger('notifiers')
viber_url = 'https://megley.ru:4443'


def send_request(json_data, url):
    requests.post(url, json_data, headers={'Content-type': 'application/json'})


def notify_viber_in_bg(json_data, url=viber_url):
    t = threading.Thread(target=send_request, args=(json_data, url), kwargs={})
    t.setDaemon(True)
    t.start()
    log.info("{} отправляется на урл {}".format(json_data, url))
