

def calculateTax(item_list):
    total_tax = 0
    for item in item_list:
        total_tax += float(item["item_price"]) * 0.23 
    return total_tax