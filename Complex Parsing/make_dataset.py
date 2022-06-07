"""Generate a random dataset of some fake shop's clients and their orders.

The dataset contains such data:

* client data (name, uuid)
* client contacts (list of contacts sets, sonsisting of phones and emeils,
last updates date and is_active flags)
* orders data (uuid, date, ordered items)

The dataset may be used for some educational purposes.
"""

import json
import uuid
from datetime import datetime
from random import choice
from typing import Callable, List

import faker
from faker.providers import address

ITEMS = [str(uuid.uuid4()) for i in range(1000)]


def generate_list_of_entities(fake_gen: faker.Faker,
                              func: Callable,
                              min_n: int = 1,
                              max_n: int = 10,
                              ) -> List[dict]:
    n = int(fake_gen.random_int(min_n, max_n))
    result = []
    for _ in range(n):
        result.append(func(fake_gen))

    return result


def generate_contacts(fake_gen: faker.Faker) -> dict:
    result = {
        "phone": fake_gen.phone_number(),
        "email": fake_gen.email(),
        "is_active": fake_gen.boolean(),
        "updated_at": fake_gen.date_time_between(
                                                datetime(2021, 1, 1),
                                                datetime(2022, 1, 1)
                                                 ).strftime(
                                                     "%Y-%m-%d %H-%M-%S"
                                                     ),
    }
    return result


def generate_item(fake_gen: faker.Faker) -> dict:
    return {
        "uuid": choice(ITEMS),
        "number_of_items": int(fake_gen.random_int(1, 50))
    }


def generate_order(fake_gen: faker.Faker) -> dict:
    result = {
        "uuid": str(uuid.uuid4()),
        "datetime": fake_gen.date_time_between(
                                            datetime(2021, 1, 1),
                                            datetime(2022, 1, 1),
                                            ).strftime("%Y-%m-%d %H-%M-%S"),
        "items": generate_list_of_entities(fake_gen, generate_item, 1, 20),
    }
    return result


def make_client(fake_gen: faker.Faker):
    name, second_name, *surname = fake_gen.name().split()
    result = {
        "uuid": str(uuid.uuid4()),
        "name": name,
        "second_name": second_name,
        "surname": ' '.join(surname),
        "address": fake_gen.address(),
        "contacts": generate_list_of_entities(
            fake_gen,
            generate_contacts,
            1,
            10,
            ),
        "orders": generate_list_of_entities(
            fake_gen,
            generate_order,
            1,
            10
            ),
    }
    return result


if __name__ == '__main__':

    fakegen = faker.Faker('ru_RU')
    fakegen.add_provider(address)
    clients = {"clients": [make_client(fakegen) for i in range(1000)]}

    with open("clients.json", "w") as f:
        json.dump(clients, f, indent=' ' * 4)
