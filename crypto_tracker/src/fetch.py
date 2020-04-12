import configparser
import requests

parser = configparser.ConfigParser()

parser.read("config.ini")

base_url = "https://pro-api.coinmarketcap.com/v1/"

currencies_listing = "/cryptocurrency/listings/latest"

currencies_mapping = "cryptocurrency/map"

currency_info = "/cryptocurrency/info"

currency_quotes = "/cryptocurrency/quotes/latest"

headers = {"Accepts": "Accepts",
           "X-CMC_PRO_API_KEY": parser.get("DEFAULT", "API_KEY")}

symbols = "XRP,BTC,ETH"

info_url_parameters = {"symbol": "XRP"}
quotes_url_parameters = {"symbol": "XRP,BTC,ETH", "convert": "EUR"}

response_currency_info = requests.get(url=f'{base_url}/{currency_info}', headers=headers, params=info_url_parameters)

response_currency_quotes = requests.get(url=f'{base_url}/{currency_quotes}', headers=headers,
                                        params=quotes_url_parameters)


def parse_data(data, symbol):
    currency = data[symbol]
    name = currency["name"]
    circulation_supply = currency["circulating_supply"]
    total_supply = currency["total_supply"]
    quotes = currency["quote"]["EUR"]

    price = quotes["price"]
    market_cap = quotes["market_cap"]
    percent_change_1h = quotes["percent_change_1h"]
    percent_change_24h = quotes["percent_change_24h"]
    percent_change_7d = quotes["percent_change_7d"]

    currency_data = {}
    currency_data.update({
        "Name": name,
        "Circulation Supply": circulation_supply,
        "Total Supply": total_supply,
        "Market Cap": market_cap,
        "Hour Change": str(percent_change_1h),
        "Day Change": str(percent_change_24h),
        "Week Change": str(percent_change_7d),
        "Price": price
    })

    return currency_data


def fetch_one_crypto_price(coin):
    response = requests.get(url=f'{base_url}/{currency_quotes}', headers=headers,
                            params={"symbol": coin, "convert": "EUR"})
    result = parse_data(response.json()["data"], coin)
    return result


def fetch_data():
    result = (response_currency_quotes.json())["data"]
    aggregated_data = {}

    for symbol in symbols.split(","):
        currency_data = parse_data(result, symbol)
        aggregated_data[symbol] = f"{(currency_data['Price']):.3f}"
    return aggregated_data


if __name__ == "__main__":
    fetch_one_crypto_price("XRP")
