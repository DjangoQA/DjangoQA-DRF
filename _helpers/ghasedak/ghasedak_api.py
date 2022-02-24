import requests


class Ghasedak:
    def __init__(self, apikey):
        self.apikey = apikey

    def request_api(self, opts):
        headers = {
            'Accept': "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            'charset': "utf-8",
            'apikey': self.apikey,
        }

        url = 'https://api.ghasedak.me/v2/' + opts['path']

        data = opts['data']

        response = requests.post(url, data=data, headers=headers)
        return response

    def verification(self, opts):
        data = dict(
            path="verification/send/simple?agent=python",
            data={
                'receptor': opts['receptor'],
                'type': opts['type'] if 'type' in opts.keys() else "1",
                'template': opts['template'],
                'param1': opts['param1'],
                'param2': opts['param2'] if 'param2' in opts.keys() else "",
                'param3': opts['param3'] if 'param3' in opts.keys() else ""
            }
        )

        response = self.request_api(data)
        if response.status_code == 200:
            return True
        return False
