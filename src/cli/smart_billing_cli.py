from src.config.supabase_config import SupabaseConfig
from src.dao.menu_dao import MenuDAO
from src.dao.customer_dao import CustomerDAO
from src.dao.cart_dao import CartDAO
from src.service.billing_service import BillingService


def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


class SmartBillingCLI:
    def __init__(self):
        config = SupabaseConfig()
        client = config.get_client()

        self.menu_dao = MenuDAO(client)
        self.customer_dao = CustomerDAO(client)
        self.cart_dao = CartDAO(client)
        self.billing_service = BillingService(self.menu_dao, self.cart_dao, self.customer_dao)

    def run(self):
        while True:
            try:
                clear_screen()
                print("=== SMART BILLING SYSTEM ===")
                print("1. Display Menu")
                print("2. Menu Management")
                print("3. Cart (Place Order)")
                print("4. Bill (Generate)")
                print("5. Display Customers")
                print("6. Customer Management")
                print("7. Exit")

                choice = input("Enter choice: ").strip()
                if choice == '1':
                    self.display_menu_items()
                elif choice == '2':
                    self.menu_management()
                elif choice == '3':
                    self.place_order()
                elif choice == '4':
                    self.generate_bill()
                elif choice == '5':
                    self.display_customers()
                elif choice == '6':
                    self.customer_management()
                elif choice == '7':
                    print("Exiting... Goodbye!")
                    break
                else:
                    print("Invalid choice.")
            except Exception as e:
                print(f"Error: {e}")

    def display_menu_items(self):
        print("\n--- MENU ITEMS ---")
        items = self.menu_dao.get_all_items()
        if not items:
            print("No items in menu.")
        else:
            print(f"{'No.':<5} {'Item':<15} {'Price':>10}")
            print("-" * 32)
            for idx, item in enumerate(items, start=1):
                print(f"{idx:<5} {item['item_name']:<15} {float(item['item_price']):>10.2f}")
        input("\nPress Enter to continue...")  # Pause after display only

    def menu_management(self):
        while True:
            clear_screen()
            print("--- MENU MANAGEMENT ---")
            print("1. Add Item")
            print("2. Update Item")
            print("3. Delete Item")
            print("4. Exit")

            choice = input("Enter choice: ").strip()
            if choice == '1':
                self.add_menu_item()
            elif choice == '2':
                self.update_menu_item()
            elif choice == '3':
                self.delete_menu_item()
            elif choice == '4':
                break
            else:
                print("Invalid choice.")

    def add_menu_item(self):
        try:
            name = input("Enter new item name: ").strip()
            price = float(input("Enter item price: ").strip())
            self.menu_dao.add_item(name, price)
            print("Item added successfully.")
        except Exception as e:
            print(f"Failed to add item: {e}")
        input("Press Enter to continue...")

    def update_menu_item(self):
        items = self.menu_dao.get_all_items()
        if not items:
            print("No menu items to update.")
            input("Press Enter to continue...")
            return
        self.display_menu_items()
        try:
            num = int(input("Enter item No. to update: ").strip())
            if num < 1 or num > len(items):
                raise ValueError("Invalid item number.")
            item = items[num-1]
            name = input(f"New name [{item['item_name']}]: ").strip() or item['item_name']
            price_input = input(f"New price [{item['item_price']}]: ").strip()
            price = float(price_input) if price_input else float(item['item_price'])
            self.menu_dao.update_item(item['item_id'], name, price)
            print("Item updated successfully.")
        except Exception as e:
            print(f"Failed to update item: {e}")
        input("Press Enter to continue...")

    def delete_menu_item(self):
        items = self.menu_dao.get_all_items()
        if not items:
            print("No menu items to delete.")
            input("Press Enter to continue...")
            return
        self.display_menu_items()
        try:
            num = int(input("Enter item No. to delete: ").strip())
            if num < 1 or num > len(items):
                raise ValueError("Invalid item number.")
            item = items[num-1]
            self.menu_dao.delete_item(item['item_id'])
            print("Item deleted successfully.")
        except Exception as e:
            print(f"Failed to delete item: {e}")
        input("Press Enter to continue...")

    def place_order(self):
        items = self.menu_dao.get_all_items()
        if not items:
            print("Menu is empty, cannot place order.")
            input("Press Enter to continue...")
            return
        print("\n--- PLACE ORDER: Select items ---")
        for idx, item in enumerate(items, start=1):
            print(f"{idx}. {item['item_name']} - {float(item['item_price']):.2f}")
        print("Enter item number and quantity. Enter 0 to finish.")

        order = []
        while True:
            try:
                item_num = int(input("Item No: ").strip())
                if item_num == 0:
                    break
                if item_num < 1 or item_num > len(items):
                    print("Invalid item number.")
                    continue
                qty = int(input("Quantity: ").strip())
                if qty < 1:
                    print("Quantity must be positive.")
                    continue
                order.append((items[item_num-1]['item_id'], qty))
            except ValueError:
                print("Invalid input. Enter numeric values only.")
                continue

        if not order:
            print("No items selected.")
            input("Press Enter to continue...")
            return

        print("\n--- Select Customer ---")
        customers = self.customer_dao.get_all_customers()
        for idx, cust in enumerate(customers, start=1):
            print(f"{idx}. {cust['cust_name']} (Mobile: {cust.get('mobile', '')})")
        print(f"{len(customers)+1}. Add New Customer")

        cust_id = None
        while True:
            try:
                cust_choice = int(input("Customer No: ").strip())
                if cust_choice == len(customers) + 1:
                    cust_id = self.add_customer_interactive()
                    if cust_id == -1:
                        print("Customer addition failed. Order cancelled.")
                        input("Press Enter to continue...")
                        return
                    break
                elif 1 <= cust_choice <= len(customers):
                    cust_id = customers[cust_choice - 1]['cust_id']
                    break
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid input")

        try:
            for item_id, qty in order:
                self.cart_dao.add_to_cart(cust_id, item_id, qty)
            print("Items added to cart successfully.")
        except Exception as e:
            print(f"Error adding items to cart: {e}")
        input("Press Enter to continue...")

    def add_customer_interactive(self) -> int:
        try:
            print("\n--- Add New Customer ---")
            name = input("Enter customer name: ").strip()
            mobile = input("Enter mobile number: ").strip()
            cust_id = self.customer_dao.add_customer(name, mobile)
            print("Customer added.")
            return cust_id
        except Exception as e:
            print(f"Failed to add customer: {e}")
            return -1

    def generate_bill(self):
        print("\n--- Generate Bill ---")
        customers = self.customer_dao.get_all_customers()
        if not customers:
            print("No customers available.")
            input("Press Enter to continue...")
            return
        for idx, cust in enumerate(customers, start=1):
            print(f"{idx}. {cust['cust_name']} (Mobile: {cust.get('mobile', '')})")
        try:
            cust_choice = int(input("Select customer No to generate bill: ").strip())
            if cust_choice < 1 or cust_choice > len(customers):
                raise ValueError("Invalid customer choice.")
            cust_id = customers[cust_choice - 1]['cust_id']

            bill = self.billing_service.calculate_bill(cust_id)
            self.print_bill(bill)
            self.billing_service.clear_customer_cart(cust_id)
        except Exception as e:
            print(f"Could not generate bill: {e}")
        input("Press Enter to continue...")

    def print_bill(self, bill: dict):
        print("\n" + "="*40)
        print(" " * 10 + "SMART BILLING")
        print("="*40)
        print("-"*40)
        print(f"{'S.No':<5} {'Item':<15} {'Qty':<5} {'Price':>8} {'Total':>8}")
        print("-"*40)
        for idx, item in enumerate(bill['items'], start=1):
            print(f"{idx:<5} {item['item_name']:<15} {item['qty']:<5} {item['price_per_item']:>8.2f} {item['total_price']:>8.2f}")
        print("-"*40)
        print(f"{'Subtotal:':>33} {bill['subtotal']:>7.2f}")
        print(f"{'GST (5%):':>33} {bill['gst']:>7.2f}")
        print(f"{'TOTAL:':>33} {bill['total']:>7.2f}")
        print("="*40)
        print(" " * 7 + "THANK YOU! VISIT AGAIN")
        print("="*40)

    def display_customers(self):
        print("\n--- CUSTOMERS ---")
        customers = self.customer_dao.get_all_customers()
        if not customers:
            print("No customers found.")
        else:
            print(f"{'No.':<5} {'Name':<15} {'Mobile':<15} {'Date':<12} {'Total Amount':>12}")
            print("-"*65)
            for idx, cust in enumerate(customers, start=1):
                name = cust['cust_name']
                mobile = cust.get('mobile', '')
                date_shopping = str(cust.get('date_of_shopping', ''))
                total_amount = float(cust.get('total_amount', 0))
                print(f"{idx:<5} {name:<15} {mobile:<15} {date_shopping:<12} {total_amount:>12.2f}")
        input("\nPress Enter to continue...")

    def customer_management(self):
        while True:
            clear_screen()
            print("--- CUSTOMER MANAGEMENT ---")
            print("1. Add Customer")
            print("2. Update Customer")
            print("3. Delete Customer")
            print("4. Exit")

            choice = input("Enter choice: ").strip()
            if choice == '1':
                self.add_customer_interactive()
            elif choice == '2':
                self.update_customer()
            elif choice == '3':
                self.delete_customer()
            elif choice == '4':
                break
            else:
                print("Invalid choice.")

    def update_customer(self):
        customers = self.customer_dao.get_all_customers()
        if not customers:
            print("No customers to update.")
            input("Press Enter to continue...")
            return
        self.display_customers()
        try:
            num = int(input("Enter customer No to update: ").strip())
            if num < 1 or num > len(customers):
                raise ValueError("Invalid number.")
            cust = customers[num-1]
            name = input(f"New name [{cust['cust_name']}]: ").strip() or cust['cust_name']
            mobile = input(f"New mobile [{cust.get('mobile', '')}]: ").strip() or cust.get('mobile', '')
            self.customer_dao.update_customer(cust['cust_id'], name, mobile)
            print("Customer updated successfully.")
        except Exception as e:
            print(f"Failed to update customer: {e}")
        input("Press Enter to continue...")

    def delete_customer(self):
        customers = self.customer_dao.get_all_customers()
        if not customers:
            print("No customers to delete.")
            input("Press Enter to continue...")
            return
        self.display_customers()
        try:
            num = int(input("Enter customer No to delete: ").strip())
            if num < 1 or num > len(customers):
                raise ValueError("Invalid number.")
            cust = customers[num-1]
            # Clear cart first to avoid foreign key violation
            self.cart_dao.clear_cart(cust['cust_id'])
            self.customer_dao.delete_customer(cust['cust_id'])
            print("Customer and related cart items deleted successfully.")
        except Exception as e:
            print(f"Failed to delete customer: {e}")
        input("Press Enter to continue...")
