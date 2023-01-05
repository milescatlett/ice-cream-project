"""
This program creates a gui window which operates as an ice cream truck. It utilizes an IceCream class, CashRegister
class, and also reads a file to get ice cream data.
Author: Miles Catlett
Date: 10/9/2022
"""
import tkinter as tk

class IceCream:
    """
    Class of ice cream objects with index, flavor and price.
    """
    def __init__(self, index, flavor, price):
        # Private attributes for IceCream class
        self.__flavor = flavor
        self.__price = price
        self.__quantity = 0
        self.__index = index

    # Public getter methods
    def get_index(self):
        return self.__index

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    # Public setter methods
    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_all(self):
        return [self.__index, self.__flavor, self.__price]

    def __str__(self):
        return f"{self.__flavor} - ${self.__price:.2f}"

    def display_subtotal(self):
        return f"{self.__flavor} - ${self.__price:.2f} ({self.__quantity})\n \
        Subtotal = ${self.__price * self.__quantity:.2f}\n\n"


class CashRegister(tk.Frame):
    """
    Contains available_items and shopping_cart. Creates tkinter elements for the ice cream truck.
    """
    def __init__(self, parent, shopping_cart={}):
        tk.Frame.__init__(self, parent)

        # Adds a logo to the top of the screen
        self.image = tk.PhotoImage(file="logo.png")
        self.logo = tk.Label(parent, image=self.image)
        self.logo.pack(side=tk.TOP)

        self.pack()
        # Private attributes for CashRegister class
        self.__shopping_cart = shopping_cart
        self.__available_items = get_available_items()
        item_list = []
        for key in self.__available_items.keys():
            item_list.append(self.__available_items[key].__str__())
        var = tk.Variable(value=item_list)
        self.message = tk.StringVar()

        tk.Label(self, text="Select an Ice Cream").grid(column=0, row=1)
        self.lb1 = tk.Listbox(self, height=15, width=40, listvariable=var)
        self.lb1.grid(column=0, row=2)
        self.btn1 = tk.Button(self, text="Add item to cart", command=self.add_item_to_cart)
        self.btn1.grid(column=0, row=3)

        tk.Label(self, text="Your Ice Cream Shopping Cart").grid(column=1, row=1)
        self.lb2 = tk.Listbox(self, height=15, width=40)
        self.lb2.grid(column=1, row=2)
        self.btn2 = tk.Button(self, text="Remove item from cart", command=self.remove_item_from_cart)
        self.btn2.grid(column=1, row=3)

        # self.btn3 = tk.Button(self, text="Preview Cart", command=self.preview_cart) # uncomment for preview btn
        # self.btn3.grid(column=0, columnspan=2, row=4) # uncomment for preview btn

        self.btn3 = tk.Button(self, text="Reset Cart", command=self.reset)
        self.btn3.grid(column=0, columnspan=2, row=5)

        tk.Message(self, text="Cart", textvariable=self.message, width=400).grid(column=0, columnspan=2, row=6)

        self.btn3 = tk.Button(self, text="Check Out", command=self.checkout)
        self.btn3.grid(column=0, columnspan=2, row=7)

    # Public getter/setter methods

    # Adds item to cart using a listbox, also adds item to the shopping_cart (dict)
    def add_item_to_cart(self):
        for key in self.__available_items.keys():
            yes = self.lb1.selection_includes(key)
            if yes == 1:
                lb_item = self.lb1.get(key)
                self.lb2.insert(tk.END, lb_item)
                num = len(self.__shopping_cart) + 1
                self.__shopping_cart[num] = self.__available_items[key]
        self.preview_cart() # comment for preview btn

    # Removes item from cart using a listbox, also removes item from the shopping_cart (dict)
    def remove_item_from_cart(self):
        # I made a copy of the dictionary to avoid an error message. I cleared the ice cream, and then recreated
        # the shopping cart (using the copy) after removing the items.
        copy = []
        for i in self.__shopping_cart.keys():
            copy.append(self.__shopping_cart[i].get_all())
        self.__shopping_cart.clear()
        for j in range(len(copy)):
            yes = self.lb2.selection_includes(j)
            if yes == 1:
                self.lb2.delete(j)
                copy.remove(copy[j])
        for k in range(len(copy)):
            self.__shopping_cart[k] = IceCream(int(copy[k][0]), copy[k][1], float(copy[k][2]))
        self.preview_cart() # comment for preview btn

    # This method uses a list.join() method to return the contents of the cart as a string
    def preview_cart(self):
        # I used a set to record the unique items. I created a list to match the shopping cart item with the
        # unique items in the set. I was able to use the match list to count the number of occurrences for each item
        # in the cart.
        msg = ["\n\n"]
        total = 0
        preview = set(())
        for key in self.__shopping_cart.keys():
            index = self.__shopping_cart[key].get_index()
            preview.add(index)
        match = []
        for i in preview:
            for j in self.__shopping_cart.keys():
                if i == int(self.__shopping_cart[j].get_index()):
                    match.append([i, j])
                    break
        for k in match:
            count = 0
            for x in self.__shopping_cart.keys():
                if k[0] == int(self.__shopping_cart[x].get_index()):
                    count += 1
            self.__shopping_cart[k[1]].set_quantity(count)
            subtotal = self.__shopping_cart[k[1]].get_price() * self.__shopping_cart[k[1]].get_quantity()
            total += subtotal
            msg.append(self.__shopping_cart[k[1]].display_subtotal())
        msg.append(f"Total: ${total:.2f}\n\n")
        self.message.set("".join(msg))

    def checkout(self):
        self.__shopping_cart.clear()
        self.lb2.delete(0, tk.END)
        self.message.set("\n\nThank you for your business.\n\nEnjoy your ice cream!\n\n")

    def reset(self):
        self.__shopping_cart.clear()
        self.lb2.delete(0, tk.END)
        self.preview_cart()

def get_available_items():
    """
    This function reads a file to get the ice cream items. I did this to declutter the code in this window.
    :return: available_items: dictionary
    """
    available_items = {}
    file = open("ice_cream.txt")
    count = 0
    for line in file:
        index = count
        flavor = line.split(', ')[0]
        price = float(line.split(', ')[1])
        available_items[count] = IceCream(index, flavor, price)
        count += 1
    file.close()
    return available_items

def main():
    """
    Creates the tkinter window for the ice cream truck.
    :return: None
    """
    root = tk.Tk()
    root.geometry("500x700+700+200")
    root.title("The Ice Cream Truck")
    CashRegister(root)
    root.mainloop()

main()