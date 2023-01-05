import tkinter as tk
from tkinter import messagebox

class IceCream:
    def __init__(self, price, flavor):
        self.__price = price
        self.__flavor = flavor

class CashRegister(tk.Frame):
    """
    contains available_items and shopping_cart
    """
    def __init__(self, parent, shopping_cart=[]):
        tk.Frame.__init__(self, parent)
        self.pack()

        list = self.make_list()
        var = tk.Variable(value=list)
        self.message = tk.StringVar()
        self.shopping_cart = shopping_cart

        tk.Label(self, text="Select an Ice Cream").grid(column=0, row=0)
        self.lb1 = tk.Listbox(self, height=15, width=40, listvariable=var)
        self.lb1.grid(column=0, row=1)
        self.btn1 = tk.Button(self, text="Add item to cart", command=self.add_item_to_cart)
        self.btn1.grid(column=0, row=2)

        tk.Label(self, text="Your Ice Cream Shopping Cart").grid(column=1, row=0)
        self.lb2 = tk.Listbox(self, height=15, width=40)
        self.lb2.grid(column=1, row=1)
        self.btn2 = tk.Button(self, text="Remove item from cart", command=self.remove_item_from_cart)
        self.btn2.grid(column=1, row=2)

        self.btn3 = tk.Button(self, text="Preview Cart", command=self.preview_cart)
        self.btn3.grid(column=0, columnspan=2, row=3)

        tk.Message(self, text="Cart", textvariable=self.message, width=400).grid(column=0, columnspan=2, row=5)

    def add_available_items(self):
        available_items = {}
        file = open("ice_cream.txt")
        count = 0
        for line in file:
            flavor = line.split(', ')[0]
            price = float(line.split(', ')[1])
            available_items[count] = IceCream(flavor=flavor, price=price)
            count += 1
        file.close()
        return available_items

    def make_list(self):
        list = []
        self.available_items = self.add_available_items()
        count = 0
        for i in range(len(self.available_items)):
            flavor = self.available_items[i]._IceCream__flavor
            price = self.available_items[i]._IceCream__price
            list.append(f"{count+1}. {flavor}: ${price:.2f}")
            count += 1
        return list

    def add_item_to_cart(self):
        for i in range(len(self.available_items)):
            yes = self.lb1.selection_includes(i)
            if yes == 1:
                lb_item = self.lb1.get(i)
                self.lb2.insert(tk.END, lb_item)
                self.shopping_cart.append(lb_item+"\n")

    def remove_item_from_cart(self):
        for i in range(len(self.available_items)):
            yes = self.lb2.selection_includes(i)
            if yes == 1:
                self.lb2.delete(i)

    def preview_cart(self):
        msg = ["\n\n"]
        items = {i: self.shopping_cart.count(i) for i in self.shopping_cart}
        total = 0
        total_items = 0
        for key in items.keys():
            num = key.split(". ")[0]
            flavor = (key.split(": ")[0]).split(". ")[1]
            price = float(key.split("$")[1])
            quantity = int(items[key])
            msg.append(f"{num}. {flavor}: ${price:.2f}.\n Quantity: {quantity}. Subtotal: ${price * quantity:.2f}.\n\n")
            total += price * quantity
            total_items += quantity
        msg.append(f"\nYou have {total_items} items in your cart.\n")
        msg.append(f"\nYour total is: ${total:.2f}\n\n\n")
        self.message.set("".join(msg))

    def checkout(self):
        # first to call preview_cart()
        self.preview_cart()

        # ask user to confirm
        confirm = input("Enter Y or y to continue to checkout, press other key to void ")
        if confirm == "Y" or confirm == "y":
            # update available items
            for i in range(len(self.__shopping_cart)):
                # find the index of the item in the available_items
                self.__available_items[i]._RetailItem__set_quantity(
                    self.__available_items[i].get_quantity())

            # clear the shopping cart
            self.__shopping_cart = []

            # display updated available items
            self.display_all_items()

def main():
    root = tk.Tk()
    root.geometry("500x700+700+200")
    root.title("The Ice Cream Truck")
    CashRegister(root)
    root.mainloop()

main()