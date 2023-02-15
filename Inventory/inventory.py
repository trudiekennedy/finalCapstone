# ======== Import modules ========
# Tabulate for "view_all" function.  Reference material: https://pypi.org/project/tabulate.
from tabulate import tabulate


# ======== The beginning of the class ==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        """
        Returns the cost of the shoe in this method.
        """
        return self.cost

    def get_quantity(self):
        """
        Returns the quantity of the shoes.
        """
        return self.quantity

    def __str__(self):
        """
        Returns a string representation of a class.
        """
        return f"{self.product}, " \
               f"{self.code}, " \
               f"{self.country}, " \
               f"{self.cost}, " \
               f"{self.quantity}."


# ============= Shoe list ===========
shoe_list = []


# ==========Functions outside the class==============
def read_shoes_data():
    """
   This function will open the file inventory.txt
   and read the data from this file, then create a shoes object with this data
   and append this object into the shoes list. One line in this file represents
   data to create one object of shoes. You must use the try-except in this function
   for error handling. Remember to skip the first line using your code.
   """
    try:
        with open("inventory.txt", "r") as shoe_file:
            shoe_file = shoe_file.readlines()[1:]  # Skips the first line containing headers
            for line in shoe_file:
                line = line.strip("\n").split(",")  # Strips out new lines and commas
                shoe_list.append(Shoe(line[0], line[1], line[2], int(line[3]), int(line[4])))
    except FileNotFoundError:
        return "Unable to find 'inventory.txt'. Please check inventory file and try again."


def capture_shoes():
    """
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object to "inventory.txt"
    """
    product = input("Name of product: ").title()
    warehouse_location = input("Warehouse location: ").title()
    price = 0
    quantity = 0

    # Asks user to input new product code, checks input is 5-digit number & checks whether the code already exists.
    # If input isn't in the correct format or code already exists, the user will be asked to try again.
    while True:
        new_product_code = input("Enter 5 digit product code: SKU")
        if new_product_code.isdigit() and len(new_product_code) == 5:
            for shoe in shoe_list:
                if "SKU" + new_product_code == shoe.code:
                    print("This product code is already in use. Please enter a new code.")
                    break
            else:
                new_product_code = "SKU" + new_product_code
                break
        else:
            print("Please enter a 5 digit number without the SKU prefix.")

    while True:  # Ensures price input is a number. If not, provides an error and asks user to try again.
        try:
            price = int(input("Price: "))
            break
        except ValueError:
            print("Input not a number. Please try again!")
            continue

    while True:  # Ensures quantity input is a number. If not, provides an error and asks user to try again.
        try:
            quantity = int(input("Quantity of product: "))
            break
        except ValueError:
            print("Input not a number. Please try again!")
            continue

    # Calls append to file function to add product to the file.
    append_to_file(warehouse_location, new_product_code, product, price, quantity)


def view_all():
    """
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    """
    # Lists to store the row data and headers for the table
    shoe_table_data = []
    shoe_table_headers = ["Product", "Product Code", "Location", "Price(R)", "Quantity"]

    for shoe in shoe_list:
        shoe_table_data.append(shoe.__str__().split(','))  # Splits the str to a list for the table.

    # Displays info from "shoe_table_data" and "shoe_table_headers" together as a table
    print(tabulate(shoe_table_data, headers=shoe_table_headers, tablefmt='rounded_outline'))


def re_stock():
    """
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    """
    lowest_quantity = shoe_list[0]  # Initiates variable with the first object to compare within loop.
    item_index = 0

    # Loop to go through each value in "shoe_list" to find the shoe object with the lowest quantity.
    for index, shoe in enumerate(shoe_list):
        # Updates "lowest_quantity" & "item_index" if quantity of current object is less than object current assigned.
        # Displays a summary of the item with the lowest quantity.
        if shoe.quantity < lowest_quantity.quantity:
            lowest_quantity = shoe
            item_index = index
    print(f"{shoe_list[item_index].product} has the lowest stock quantity "
          f"with {shoe_list[item_index].quantity} pairs in stock.")

    while True:
        restock = input("Do you wish to restock? (Y/N): ").upper()
        # Y asks user how much they want to add to the quantity. If number not provided, an error is presented.
        if restock == "Y":
            while True:
                try:
                    restock_amount = int(input("How many do you want to add to the quantity?: "))
                    shoe_list[item_index].quantity += restock_amount
                    return f"{shoe_list[item_index].product} now has {shoe_list[item_index].quantity} pairs in stock."

                except ValueError:  # Error handling.
                    print("Input was not a number. Please try again!")
                    continue
        # N exits the "restock" menu and displays message to user that quantity has not been updated.
        elif restock == "N":
            return f"{shoe_list[item_index].product} stock quantity has not been updated."

        # Handles input if not "Y" or "N" - asks user to try again.
        else:
            print("Option not supported. Please try again!")
            continue


def search_shoe(code):
    """
     This function will search for a shoe in the list using the shoe code
     The shoe will be returned in a table format with the details of the object matching the code.
     If code doesn't match, a message will be displayed to the user.
    """
    shoe_values = []
    shoe_headers = ["Product", "Code", "Location", "Price(R)", "Quantity"]

    # Checks each object in the shoe list to see if code passed as an argument matches the code of an object.
    for shoe in shoe_list:
        if shoe.code == code:
            # Splits matching object's str into a list and returns it as a headed table.
            shoe_values.append(shoe.__str__().split(","))
            return tabulate(shoe_values, headers=shoe_headers, tablefmt='rounded_outline')
    # Message returned if no match.
    return f"There is no item with the code: {code}."


def value_per_item():
    """
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    """
    shoe_values = []
    shoe_headers = ["Product", "Cost(R)", "Quantity", "Value(R)"]

    # For each object in "shoe_list", gets value by multiplying cost by quantity and appends details to "shoe_values".
    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()
        shoe_values.append([shoe.product, shoe.cost, shoe.quantity, value])

    # Returns a table with headers listed in "shoe_headers" list, including the value for each product.
    print(tabulate(shoe_values, headers=shoe_headers, tablefmt='rounded_outline'))


def write_to_file():
    """
    This function writes "shoe_list to "inventory.txt" file - it overwrites existing content with content that has
    been updated in the "shoe_list".
    """
    with open('inventory.txt', 'w') as file:
        file.write("Country,Code,Product,Cost,Quantity")
        for shoe in shoe_list:
            file.write(f"\n{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}")


def append_to_file(warehouse_location, prod_code, product, shoe_cost, shoe_quantity):
    """
    This function appends the arguments passed in as a new line to "inventory.txt" file.
    """
    with open('inventory.txt', 'a') as file:
        file.write(f"\n{warehouse_location},{prod_code},{product},{shoe_cost},{shoe_quantity}")


def highest_qty():
    """
    This function determines the product with the highest quantity and
    print this shoe as being for sale.
    """
    highest_quantity = shoe_list[0]     # Initiates variable with the first object to compare within loop.
    item_index = 0

    #  Loop to go through each value in "shoe_list" to find the shoe object with the highest quantity.
    for index, shoe in enumerate(shoe_list):
        # Updates "highest_quantity" & "item_index" if quantity of current object is more than the object assigned.
        if shoe.quantity > highest_quantity.quantity:
            highest_quantity = shoe
            item_index = index

    # Displays a summary of the item with the highest quantity.
    print(f"{shoe_list[item_index].product} has the highest quantity "
          f"with {shoe_list[item_index].quantity} pairs in stock. "
          f"\nCurrent Price: R{shoe_list[item_index].cost}.\n")

    # Asks user if they want to put the product on sale.
    for_sale = input("Do you want to put this product on sale? (Y/N): ").upper()

    if for_sale == "Y":     # If "Y" asks how much the price needs to decrease and updates cost stored in "shoe_list".
        while True:
            try:
                discount = int(input("How much do you want to decrease the price by?: R"))
                shoe_list[item_index].cost -= discount
                print(f'{shoe_list[item_index].product} now costs R{shoe_list[item_index].cost}.')
                break
            except ValueError:  # If the input "discount" isn't a number, displays an error and asks user to try again.
                print("Not a valid number. Please try again.")

    elif for_sale == "N":   # If "N" displays message stating price not updated.
        print(f"{shoe_list[item_index].product}'s price has not been updated.")

    else:   # Handles input that isn't "Y" or "N".
        print(f"Option not supported.")


# ==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''
# Declares "menu_dict" to store the supported menu options.
menu_dict = {1: "view all",
             2: "add product",
             3: "search by product code",
             4: "view stock values",
             5: "check restock",
             6: "decide sale item",
             7: "exit"}

# Default menu prints out each item in menu_dict as options for the user.
while True:
    # Resets "shoe_list" by declaring an empty list then calls the "read_shoes_data" function:
    # This ensures "shoe_list" is updated if information is added or changed in other menu items.
    shoe_list = []
    read_shoes_data()

    # Prints main menu and each item in "menu_dict" to present the user with menu options.
    print("░" * 34 + " MAIN MENU " + "░" * 34)
    for key in menu_dict:
        print(f"{key}: {menu_dict[key]}")

    print("░" * 79)

    try:
        choice = int(input("Enter your selection (1-7): "))     # Asks user to enter a numeric selection.

        if choice == 1:     # View all.
            print("░" * 31 + " FULL  INVENTORY " + "░" * 31)
            view_all()

        elif choice == 2:   # Capture shoes.
            print("░" * 33 + " ADD PRODUCT " + "░" * 33)
            capture_shoes()

        elif choice == 3:   # Search by code.
            print("░" * 33 + " CODE SEARCH " + "░" * 33)
            while True:     # Ensures input matches product code format.
                product_code = input("Enter 5 digit product code: SKU")
                if product_code.isdigit() and len(product_code) == 5:
                    product_code = "SKU" + product_code
                    print(search_shoe(product_code))
                    break
                else:   # Error message if input format doesn't match product code format.
                    print("Invalid input. Please try again.")

        elif choice == 4:   # Inventory Values.
            print("░" * 31 + " INVENTORY VALUE " + "░" * 31)
            value_per_item()

        elif choice == 5:   # Restock.
            print("░" * 29 + " RESTOCK  SUGGESTION " + "░" * 29)
            print(re_stock())
            write_to_file()     # Overwrites "inventory.txt" file with new information to ensure price is updated.

        elif choice == 6:   # Sale suggestion.
            print("░" * 31 + " SALE SUGGESTION " + "░" * 31)
            highest_qty()
            write_to_file()     # Overwrites "inventory.txt" file with new information to ensure price is updated.

        elif choice == 7:   # Exit.
            print("Goodbye!")
            break

        else:   # Handles number that isn't in range 1-7.
            print("Incorrect selection. Please try again.")
            continue

    except ValueError:  # Handles if input isn't a number.
        print("Please enter a number listed in the menu!")
        continue
