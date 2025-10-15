from model.customer_model import Customer

customer_collection = []


def save_customer(customer: Customer) -> str:
    print("Creando nuevo cliente")
    customer._id = str(len(customer_collection))
    customer_collection.append(customer)
    print(customer_collection)
    return customer._id


def get_all_customers() -> list:
    return customer_collection


def get_customer(_id: str) -> dict:
    return customer_collection[int(_id)]
