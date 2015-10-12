import requests


class Ilias:
    base_url = 'https://ilias.fh-muenster.de/'

    URLS = {
        'login': 'ilias/ilias.php?lang=de&client_id=Bibliothek&cmd=post&cmdClass=ilstartupgui&cmdNode=i9&baseClass=ilStartUpGUI&rtoken=',
    }

    def __init__(self):
        self.session = requests.Session()

        # Initialize Cookies etc.
        self.session.get(self.base_url)


    def url(self, action):
        return '{base_url}{path}'.format(base_url=self.base_url, path=self.URLS[action])

    def auth(self, username, password):
        payload = {
            'cmd[showLogin]': 'Anmelden',
            'username': username,
            'password': password,
        }

        response = self.session.post(self.url('login'), data=payload)

        return 'Persönlicher Schreibtisch' in response.text
