"""Q5 - Functions, parameters and scope (K4 Analyse)."""


def add_item_buggy(item, order=[]):
    order.append(item)
    return order


def add_item(item, order=None):
    if order is None:           # TODO 1: new list per call when none supplied
        order = []
    order.append(item)
    return order


def make_order():
    """Closure alternative: the list lives in the enclosing scope."""
    order = []

    def add(item):
        order.append(item)
        return list(order)
    return add


def bill(prices, gst_rate=0.05):
    """Returns two values (a tuple): total and GST."""
    total = sum(prices)
    return total, round(total * gst_rate, 2)


counter = 0


def local_demo():
    counter = 99               # new LOCAL name; global untouched
    return counter


def global_demo():
    global counter             # needed to rebind the global name
    counter += 1


def no_global_demo():
    try:
        counter += 1           # UnboundLocalError: assignment makes it local
    except UnboundLocalError as e:
        return f"UnboundLocalError: {e}"


def outer():
    n = 0

    def inner():
        nonlocal n             # rebinds the enclosing function's variable
        n += 1
    inner()
    inner()
    return n


if __name__ == "__main__":
    print(add_item_buggy("Tea"), add_item_buggy("Vada"))
    print(add_item("Tea"), add_item("Vada"))
    print("add_item_buggy.__defaults__ ->", add_item_buggy.__defaults__)
    print("add_item.__defaults__       ->", add_item.__defaults__)
    print("same list object returned twice:", add_item_buggy("X") is add_item_buggy("Y"))

    print("\nThree customers in sequence (independent orders):")
    for items in (["Tea", "Vada"], ["Coffee"], ["Idli", "Dosa", "Tea"]):
        order = None
        for it in items:
            order = add_item(it, order)
        print("  ", order)

    print("\nClosure alternative (one add() per customer):")
    c1, c2 = make_order(), make_order()
    c1("Tea"); c2("Coffee"); c1("Vada")
    print("  customer 1:", c1("Samosa"), "| customer 2:", c2("Bun"))

    print("\nParameter styles:")
    print("  positional :", bill([20, 15, 30]))
    print("  keyword    :", bill(prices=[20, 15, 30], gst_rate=0.12))
    total, gst = bill([20, 15, 30])
    print(f"  unpacked   : total={total} gst={gst}")

    print("\nScope demos:")
    print("  local_demo() ->", local_demo(), "| global counter =", counter)
    global_demo()
    print("  after global_demo() -> counter =", counter)
    print("  without global ->", no_global_demo())
    print("  nonlocal outer() ->", outer())
