"""In this file there is an example code 
for parsing a complex json."""
#%% Imports

import json
import pandas as pd

#%% Read Data
with open("clients.json", "r") as f:
    json_data = json.load(f)

#%%

clients = pd.json_normalize(
    data=json_data,
    record_path=["clients"],
    record_prefix="client_",
    errors="ignore",
).drop(columns=["client_contacts", "client_orders"])

#%%

contacts = pd.json_normalize(
    data=json_data,
    record_path=["clients", "contacts"],
    record_prefix="contact_",
    errors="ignore",
    meta=[
        ["clients", "uuid"]
    ],
    sep='_',
)

#%%

orders = pd.json_normalize(
    data=json_data,
    record_path=["clients", "orders"],
    record_prefix="order_",
    errors="ignore",
    meta=[
        ["clients", "uuid"]
    ],
    sep='_',
).drop(columns=["order_items"])

#%%

order_items = pd.json_normalize(
    data=json_data,
    record_path=["clients", "orders", "items"],
    record_prefix="order_item_",
    errors="ignore",
    meta=[
        ["clients", "orders", "uuid"]
    ],
    sep='_',
)


#%%

















clients = pd.json_normalize(
                data=json_data,
                record_path=["clients"],
                record_prefix="client_",
                errors='ignore',
                sep='_',
                ).drop(columns=[
                    "client_orders",
                    "client_contacts",
                    ])

clients.to_excel("clients.xlsx", index=False)

#%%

contacts = pd.json_normalize(
                data=json_data,
                record_path=["clients", "contacts"],
                meta=[
                    ["clients", "uuid"]
                ],
                record_prefix="contact_",
                errors='ignore',
                sep='_',
                )

contacts.to_excel("contacts.xlsx", index=False)

# %%

orders = pd.json_normalize(
                data=json_data,
                record_path=["clients", "orders"],
                meta=[
                    ["clients", "uuid"]
                ],
                record_prefix="order_",
                errors='ignore',
                sep='_',
                ).drop(columns=["order_items"])

orders.to_excel("orders.xlsx", index=False)

#%%

order_items = pd.json_normalize(
                data=json_data,
                record_path=["clients", "orders", "items"],
                meta=[
                    ["clients", "orders", "uuid"]
                ],
                record_prefix="item_",
                errors='ignore',
                sep='_',
                )

order_items.to_excel("order_items.xlsx", index=False)

# %%

clients_with_orders = pd.merge(
    clients,
    orders,
    left_on=["client_uuid"],
    right_on=["clients_uuid"],
    how="outer"
)


# %%
