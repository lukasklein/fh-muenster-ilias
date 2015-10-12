import requests
import lxml.html
from lxml.cssselect import CSSSelector


class Item:
    def __repr__(self):
        return '{name} <{url}>'.format(name=self.name, url=self.url)


class Ilias:
    base_url = 'https://ilias.fh-muenster.de/'

    URLS = {
        'login': 'ilias/ilias.php?lang=de&client_id=Bibliothek&cmd=post&cmdClass=ilstartupgui&cmdNode=i9&baseClass=ilStartUpGUI&rtoken=',
        'selected_items': 'ilias/ilias.php?baseClass=ilPersonalDesktopGUI&cmd=jumpToSelectedItems',
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

    def get_selected_items(self):
        response = self.session.get(self.url('selected_items'))

        tree = lxml.html.fromstring(response.text)

        item_sel = CSSSelector('div[headers="th_selected_items"]')
        name_sel = CSSSelector('h4.il_ContainerItemTitle')
        icon_sel = CSSSelector('img.ilListItemIcon')

        results = item_sel(tree)

        for result in results:
            item = Item()

            name = name_sel(result)[0]

            try:
                name = CSSSelector('a')(name)[0]
            except IndexError:
                pass

            item.name = name.text
            item.url = name.get('href')

            icon = icon_sel(result)[0]
            item.icon = icon.get('src')

            yield item

