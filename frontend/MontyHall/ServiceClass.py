import requests


class Service:

    def post_request(self, data: dict, url):
        response = requests.post(url, json=data, timeout=20)
        return response.json()

    def check_response(self, response):
        if response["status"] == "Good":
            return True
        return False
