# this function has only one task, take the order id, search in csv and return the order details

import pandas as pd
# Load the orders dataset once
orders_df = pd.read_csv("sample_data/orders.csv")
def get_order(order_id: str):
    #  Returns the order details for the given order ID.
    order = orders_df[
        orders_df["order_id"].str.upper() == order_id.upper()
    ]
    if order.empty:
        return None
    return order.iloc[0].to_dict()