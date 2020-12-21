

def convertCurrency(base_currency, dest_currency, value):
    import requests
    url = 'https://api.exchangeratesapi.io/latest'
    url += '?base=' + base_currency

    try:
        response = requests.get(url)
        data = response.json()
        convert_rate = data[dest_currency]
        return value * convert_rate
    except Exception:
        print('Cant convert')

def calculateTax(item_list):
    total_tax = 0
    for item in item_list:
        total_tax += float(item["item_price"]) * 0.23 
    return total_tax