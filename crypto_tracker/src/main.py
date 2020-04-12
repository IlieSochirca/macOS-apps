import rumps

from src.fetch import fetch_data, fetch_one_crypto_price


class TinkerApp(rumps.App):
    def __init__(self):
        super().__init__("Tinker",
                         icon="coin.png")
        self.data = fetch_data()

        self.preferences_menu = rumps.MenuItem("Preferences")
        self.xrp = rumps.MenuItem(title=f"XRP/EUR: {self.data['XRP']} \u20ac", callback=self.update_data)
        self.btc = rumps.MenuItem(title=f"BTC/EUR: {self.data['BTC']} \u20ac", callback=self.update_data)
        self.eth = rumps.MenuItem(title=f"ETH/EUR: {self.data['ETH']} \u20ac", callback=self.update_data)
        self.preferences_menu.update([self.xrp, self.btc, self.eth])
        self.new_menu = rumps.MenuItem("New Crypto")
        self.add_menu = rumps.MenuItem("Add new preference")
        self.new_menu.add(self.add_menu)
        self.update_button = rumps.MenuItem("Update data")
        self.menu = [self.preferences_menu, self.new_menu, self.update_button]

    @rumps.clicked("Update data")
    def update_data(self, sender):
        self.update()

    @rumps.clicked("New Crypto", "Add new preference")
    def set_currency_symbol(self, sender):
        window = rumps.Window(dimensions=(320, 80))
        window.title = 'Set new currency for tracking'
        window.message = "Enter a new symbol that will be added to tracking"
        response = window.run()
        currency_sign = response.text
        result = fetch_one_crypto_price(currency_sign)
        self.preferences_menu.add(
            rumps.MenuItem(f"{currency_sign.upper()}/EUR: {result['Price']:.3F} \u20ac", callback=self.update_data))

    def update(self):
        fetched_data = fetch_data()
        self.preferences_menu.clear()
        self.preferences_menu.update(
            [rumps.MenuItem(title=f"{elem}/EUR: {self.data[elem]} \u20ac", callback=self.update_data) for elem in
             fetched_data])


if __name__ == '__main__':
    app = TinkerApp()
    app.run()
