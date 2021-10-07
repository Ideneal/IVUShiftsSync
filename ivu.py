import requests


class IVU:

    def __init__(self):
        self.session = requests.Session()

    def login(self, username, password):
        self.session.get('https://www.webcrew.trenitalia.it/mbweb/pub/trenitalia/desktop/login')
        payload = {'j_username': username, 'j_password': password}
        self.session.post('https://www.webcrew.trenitalia.it/mbweb/j_security_check', data=payload)

    def shifts(self, begin_date = None):
        url = 'https://www.webcrew.trenitalia.it/mbweb/main/trenitalia/desktop/_-duty-table'

        if begin_date is not None:
            url += '?beginDate=' + begin_date
        
        r = self.session.get(url)
        return r.content