
import csv
import os

FILENAME = "inventory_data.csv"
LOW_STOCK_LIMIT = 5

# Structure:
# {item_name: {"quantity": int, "description": str}}
inventory = {}


def load_data():
    """Load inventory data from the CSV file."""
    if not os.path.exists(FILENAME):
        return

    with open(FILENAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) == 2:
                name, quantity = row
                description = "No description provided."
            elif len(row) == 3:
                name, quantity, description = row
            else:
                continue

            name = name.strip()

            if not name:
                continue

            try:
                quantity = int(quantity)

                if quantity < 0:
                    print(f"Invalid quantity for '{name}'. Skipping.")
                    continue

                inventory[name] = {
                    "quantity": quantity,
                    "description": description.strip()
                    or "No description provided."
                }

            except ValueError:
                print(f"Invalid quantity for '{name}'. Skipping.")


def save_data():
    """Save inventory data to a CSV file."""
    with open(FILENAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        for name, data in inventory.items():
            writer.writerow([
                name,
                data["quantity"],
                data["description"]
            ])


def get_valid_quantity(prompt):
    """Accept only non-negative whole numbers."""
    while True:
        try:
            value = int(input(prompt))

            if value < 0:
                print("Quantity cannot be negative.")
            else:
                return value

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def find_item_key(input_name):
    """Find an item without considering letter case."""
    input_name = input_name.strip().lower()

    for name in inventory:
        if name.lower() == input_name:
            return name

    return None


def register_item():
    """Register a new school supply."""
    print("\n--- Register New Item ---")

    name = input("Enter item name: ").strip()

    if not name:
        print("Item name cannot be empty.")
        return

    if find_item_key(name) is not None:
        print("Item already exists. Use Add Quantity instead.")
        return

    quantity = get_valid_quantity("Enter initial quantity: ")

    description = input("Enter description (optional): ").strip()

    if not description:
        description = "No description provided."

    inventory[name] = {
        "quantity": quantity,
        "description": description
    }

    save_data()
    print(f"'{name}' registered successfully.")


def view_stock_list():
    """Display all items and their descriptions."""
    if not inventory:
        print("\nInventory is empty.")
        return

    print("\n--- School Supplies Stock List ---")
    print(f"{'Item Name':<25} | {'Quantity':<10} | Description")
    print("-" * 70)

    for name, data in inventory.items():
        print(
            f"{name:<25} | "
            f"{data['quantity']:<10} | "
            f"{data['description']}"
        )


def search_supply():
    """Search by item name or description."""
    keyword = input(
        "Enter item name, description, or keyword: "
    ).strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    found = False

    print("\n--- Search Results ---")

    for name, data in inventory.items():
        if (
            keyword in name.lower()
            or keyword in data["description"].lower()
        ):
            print(
                f"- {name}: {data['quantity']} "
                f"| Description: {data['description']}"
            )
            found = True

    if not found:
        print("No matching supplies found.")


def add_quantity():
    """Add stock when new supplies arrive."""
    print("\n--- Add Stock / Restock ---")

    name = input("Enter item name to restock: ").strip()
    key = find_item_key(name)

    if key is None:
        print("Item not found.")
        return

    print(f"Current stock: {inventory[key]['quantity']}")

    amount = get_valid_quantity("Enter quantity to add: ")

    inventory[key]["quantity"] += amount

    save_data()

    print(
        f"Stock updated. New quantity: "
        f"{inventory[key]['quantity']}"
    )


def release_quantity():
    """Release supplies without allowing negative stock."""
    print("\n--- Release Stock / Issue Items ---")

    name = input("Enter item name to release: ").strip()
    key = find_item_key(name)

    if key is None:
        print("Item not found.")
        return

    current_quantity = inventory[key]["quantity"]
    print(f"Current stock: {current_quantity}")

    amount = get_valid_quantity("Enter quantity to release: ")

    if amount > current_quantity:
        print("Error: Not enough stock available.")
        return

    inventory[key]["quantity"] -= amount

    save_data()

    print(
        f"Stock released successfully. "
        f"Remaining quantity: {inventory[key]['quantity']}"
    )


def edit_item_details():
    """Edit an item's name or description."""
    print("\n--- Edit Item Details ---")

    name = input("Enter item name to edit: ").strip()
    key = find_item_key(name)

    if key is None:
        print("Item not found.")
        return

    print(f"Current name: {key}")
    print(f"Current description: {inventory[key]['description']}")

    new_name = input(
        "Enter new name (press Enter to keep current): "
    ).strip()

    if new_name:
        existing_key = find_item_key(new_name)

        if existing_key is not None and existing_key != key:
            print("Another item already uses that name.")
            return

    new_description = input(
        "Enter new description (press Enter to keep current): "
    ).strip()

    if new_name:
        inventory[new_name] = inventory.pop(key)
        key = new_name

    if new_description:
        inventory[key]["description"] = new_description

    save_data()
    print("Item details updated successfully.")


def update_quantity():
    """Set the exact quantity of an existing item."""
    print("\n--- Set Stock Quantity ---")

    name = input("Enter item name: ").strip()
    key = find_item_key(name)

    if key is None:
        print("Item not found.")
        return

    print(f"Current quantity: {inventory[key]['quantity']}")

    quantity = get_valid_quantity("Enter new quantity: ")

    inventory[key]["quantity"] = quantity

    save_data()
    print("Quantity updated successfully.")


def delete_supply():
    """Delete an item from the inventory."""
    print("\n--- Delete Supply ---")

    name = input("Enter item name to delete: ").strip()
    key = find_item_key(name)

    if key is None:
        print("Item not found.")
        return

    confirm = input(
        f"Are you sure you want to delete '{key}'? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        del inventory[key]
        save_data()
        print(f"'{key}' deleted successfully.")
    else:
        print("Deletion cancelled.")


def check_low_stock():
    """Display items with five or fewer units."""
    print(f"\n--- Low Stock ( {LOW_STOCK_LIMIT} or fewer) ---")

    found = False

    for name, data in inventory.items():
        if data["quantity"] <= LOW_STOCK_LIMIT:
            print(f"- {name}: {data['quantity']}")
            found = True

    if not found:
        print("No supplies are low in stock.")


def main():
    """Run the inventory management system."""
    load_data()

    while True:
        print("\n===== SCHOOL SUPPLIES INVENTORY SYSTEM =====")
        print("1. Register New Item")
        print("2. View Stock List")
        print("3. Search Supply")
        print("4. Add Quantity / Restock")
        print("5. Release Quantity / Issue Items")
        print("6. Edit Item Details")
        print("7. Set Stock Quantity")
        print("8. Delete Supply")
        print("9. Check Low Stock")
        print("10. Exit")

        choice = input("Enter your choice (1-10): ").strip()

        if choice == "1":
            register_item()
        elif choice == "2":
            view_stock_list()
        elif choice == "3":
            search_supply()
        elif choice == "4":
            add_quantity()
        elif choice == "5":
            release_quantity()
        elif choice == "6":
            edit_item_details()
        elif choice == "7":
            update_quantity()
        elif choice == "8":
            delete_supply()
        elif choice == "9":
            check_low_stock()
        elif choice == "10":
            save_data()
            print("Inventory saved. Thank you for using the system!")
            break
        else:
            print("Invalid choice. Please select 1-10.")


if __name__ == "__main__":
    main()
    