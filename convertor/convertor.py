import requests


class Convertor:
    urls = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'
    data = None

    def __init__(self):
        pass

    def request(self):
        responce = requests.get(self.urls)

        if responce.status_code == 200:
            return responce.json()
        else:
            return None

    def getData(self, code):
        result=None
        if self.data == None:
            self.data = self.request()
        for i in self.data:
            if i['Ccy'] == code:
                result = i
                break
        if result == None:
            return None
        else:
            return result

