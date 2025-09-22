from math import floor

REDUCTION_CODES = {
    "SAVE10": lambda p: p * (0.1),
    "5OFF": lambda _: 5,
}

TAX_RATE = 0.2

CLIENT_ORDERS = (
    {"name": "Latte", "price": 4.25, "qty": 2},
    {"name": "Muffin", "price": 3.25, "qty": 1},
)

INVOICE_PRODUCT_FORMAT = "{name}          x{qty}    {price}€"

INVOICE_FORMAT = """
======== Reçu du Café ========
{products}
------------------------------
Sous-total:        {sub_total}€
Réduction:         {reduction}€
Taxe ({tax_rate_percent}%):       {tax_price}€
Total:             {total}€
==============================
Points de fidélité gagnés: {fidelity_points_gained}
------------------------------
"""


def calc_fidelity_points(price):
    return floor(price / 5)


def generate_invoice(client_orders, reduction_code=""):

    # No Tax / Reduction Considered
    sub_total = sum(map(lambda o: o["price"], client_orders))

    reduction = (
        0
        if (reduction_code not in REDUCTION_CODES.keys())
        else REDUCTION_CODES[reduction_code](sub_total)
    )

    # Tax / Reduction  Considered
    total = sub_total * (1 + TAX_RATE)

    invoice_data = {
        "products": "\n".join(
            map(lambda o: INVOICE_PRODUCT_FORMAT.format(**o), client_orders)
        ),
        "sub_total": round(sub_total, 2),
        "reduction": -round(reduction, 2),
        "tax_price": round(total - sub_total, 2),
        "tax_rate_percent": TAX_RATE * 100,
        "total": round(total, 2),
        "fidelity_points_gained": calc_fidelity_points(total),
    }

    return INVOICE_FORMAT.format(**invoice_data)


print("-" * 15, "invoice 1", "-" * 15)
print("with valid reduction code (5OFF):", "\n")
print(generate_invoice(CLIENT_ORDERS, "5OFF"))

print("-" * 15, "invoice 2", "-" * 15)
print("with valid reduction code (SAVE10):", "\n")
print(generate_invoice(CLIENT_ORDERS, "SAVE10"))

print("-" * 15, "invoice 3", "-" * 15)
print("with invalid reduction code:", "\n")
print(generate_invoice(CLIENT_ORDERS, "SOMETHING"))

print("-" * 15, "invoice 4", "-" * 15)
print("without reduction code:", "\n")
print(generate_invoice(CLIENT_ORDERS))
