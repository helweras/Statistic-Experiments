import requests


class ClientCheck:
    @staticmethod
    def get_response(url):
        response = requests.get(url=url)
        if response.status_code == 200:
            return True
        return False

    