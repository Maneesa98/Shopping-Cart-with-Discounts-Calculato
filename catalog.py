# Catalog of products and their prices
catalog = {
    "Product A": 20,
    "Product B": 40,
    "Product C": 50
}

# Discount rules
discount_rules = {
    "flat_10_discount": {
        "min_total": 200,
        "discount_amount": 10
    },
    "bulk_5_discount": {
        "min_quantity": 10,
        "discount_percent": 5
    },
    "bulk_10_discount": {
        "min_total_quantity": 20,
        "discount_percent": 10
    },
    "tiered_50_discount": {
        "min_total_quantity": 30,
        "min_product_quantity": 15,
        "discount_percent": 50
    }
}

# For displaying the catalog
print("\tCatalog of Products:")
print("Product\t\t\t\tPrice")
for product, price in catalog.items():
    print(f"{product}\t\t\t${price}")

# Get the quantity of the products and the choice of gift wrap for each product
quantities = {}
gift_wrap_choices = {}
for product in catalog:
    quantity = int(input(f"\nEnter the quantity needed for {product}: "))
    quantities[product] = quantity
    if quantity > 0:
        gift_wrap_choices[product] = input(f"Do you want {product} wrapped as a gift? (yes/no): ")

# Calculate product totals and subtotal
subtotal = 0
product_totals = {}
for product, price in catalog.items():
    quantity = quantities[product]
    product_total = quantity * price
    product_totals[product] = product_total
    subtotal += product_total

# Calculate total quantity
total_quantity = sum(quantities.values())

# Function to calculate the discount based on each discount rule
def calculate_discount(rule, total_quantity, subtotal):
    if rule not in discount_rules:
        return 0

    specific_detail = discount_rules[rule]

    if rule == "flat_10_discount":
        if subtotal > specific_detail["min_total"]:
            return specific_detail["discount_amount"]
    elif rule == "bulk_5_discount":
        discount_amount = 0
        for product, price in catalog.items():
            if product in quantities and quantities[product] > specific_detail["min_quantity"]:
                discount_amount += price * quantities[product] * (specific_detail["discount_percent"] / 100)
        return discount_amount
    elif rule == "bulk_10_discount":
        if total_quantity > specific_detail["min_total_quantity"]:
            return subtotal * (specific_detail["discount_percent"] / 100)
    elif rule == "tiered_50_discount":
        product_quantity_greater = False
        for product, price in catalog.items():
            if product in quantities and quantities[product] > specific_detail["min_product_quantity"]:
                product_quantity_greater = True
                break
        if total_quantity > specific_detail["min_total_quantity"] and product_quantity_greater:
            subtotal_discounted = 0
            for product, price in catalog.items():
                if product in quantities:
                    quantity = quantities[product]
                    subtotal_discounted += min(specific_detail["min_product_quantity"], quantity) * price
                    subtotal_discounted += max(0, quantity - specific_detail["min_product_quantity"]) * price * (1 - specific_detail["discount_percent"] / 100)
            return subtotal - subtotal_discounted
    
    return 0

# Applying the most beneficial discount
discount_name = ""
discount_amount = 0
for rule in discount_rules:
    discount = calculate_discount(rule, total_quantity, subtotal)
    if discount > discount_amount:
        discount_name = rule
        discount_amount = discount

# Function to calculate the gift wrap fee
def calculate_gift_wrap_fee(quantity):
    gift_wrap_fee_per_unit = 1
    return quantity * gift_wrap_fee_per_unit

# Calculate gift wrap fee
gift_wrap_fee = 0
for product, quantity in quantities.items():
    if quantity > 0 and product in gift_wrap_choices and gift_wrap_choices[product].lower() == "yes":
        gift_wrap_fee += calculate_gift_wrap_fee(quantity)

# Function to calculate the shipping fee
def calculate_shipping_fee(total_quantity):
    units_per_package = 10
    package_count = ((total_quantity + units_per_package - 1) // units_per_package)
    shipping_fee_per_package = 5
    return package_count * shipping_fee_per_package

# Calculate shipping fee
shipping_fee = calculate_shipping_fee(total_quantity)

# Function to calculate the total amount
def calculate_total(subtotal, discount_amount, shipping_fee, gift_wrap_fee):
    return subtotal - discount_amount + shipping_fee + gift_wrap_fee

# Calculate the total amount
total = calculate_total(subtotal, discount_amount, shipping_fee, gift_wrap_fee)

# Displaying the purchase details
print("\n\tPurchase Details")
print("Product\t\tQuantity\tTotal Amount")
for product, quantity in quantities.items():
    print(f"{product}\t{quantity}\t\t{product_totals[product]}")
print(f"Subtotal: {subtotal}")
print(f"\nDiscount Applied: {discount_name}\nDiscount Amount: {discount_amount}")
print(f"\nShipping Fee: {shipping_fee}")
print(f"Gift Wrap Fee: {gift_wrap_fee}")
print(f"\nTotal: {total}")
