import json
import datetime
from app.customer import Customer
from app.shop import Shop
from app.car import Car


def shop_trip():
    with open("app/config.json", "r") as f:
        config = json.load(f)

    fuel_price = config["FUEL_PRICE"]
    shops = [Shop(s) for s in config["shops"]]

    customers = []
    for c_data in config["customers"]:
        cust = Customer(c_data)
        cust.car = Car(c_data["car"])
        customers.append(cust)

    for customer in customers:
        home_location = customer.location
        print(f"{customer.name} has {customer.money} dollars")

        trip_costs = []
        for shop in shops:
            dist = customer.distance_km(shop)
            fuel_cost_total = customer.car.calc_fuel_cost(dist, fuel_price) * 2

            products_cost = shop.total_products_cost(customer.product_cart)

            total_trip_cost = fuel_cost_total + products_cost
            trip_costs.append((total_trip_cost, shop))

            print(f"{customer.name}'s trip to the {shop.name}"
                  f" costs {total_trip_cost:.2f}")

        best_cost, best_shop = min(trip_costs, key=lambda x: x[0])

        if best_cost <= customer.money:
            print(f"{customer.name} rides to {best_shop.name}")
            customer.location = best_shop.location

            print(f"Date: {datetime.datetime.now().strftime(
                '%d/%m/%Y %H:%M:%S')}")
            print(f"Thanks, {customer.name}, for your purchase!")
            print("You have bought:")

            print(f"Total cost is {best_cost:.2f} dollars")

            print(f"{customer.name} rides home")
            customer.location = home_location
            customer.money -= best_cost
            print(f"{customer.name} now has {customer.money:.2f} dollars\n")
        else:
            print(f"{customer.name} doesn't have enough"
                  f" money to make a purchase in any shop\n")


if __name__ == "__main__":
    shop_trip()
