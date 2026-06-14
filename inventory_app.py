import time

class Product:
    """Represents an item in the store warehouse."""
    def __init__(self, product_id, name, stock, price):
        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.price = price

    def reduce_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False


class Order:
    """Represents a customer checkout request."""
    def __init__(self, order_id, customer_name, product_id, quantity):
        self.order_id = order_id
        self.customer_name = customer_name
        self.product_id = product_id
        self.quantity = quantity
        self.timestamp = time.strftime('%H:%M:%S')


class InventorySystem:
    """Manages store items using a Hash Map and processes requests using a Queue."""
    def __init__(self):
        # Hash Map / Dictionary for O(1) constant time lookups
        self.inventory = {}
        # Simple List-based Queue for First-In, First-Out (FIFO) processing
        self.order_queue = []

    def add_new_product(self, product_id, name, stock, price):
        """Inserts a new product into the inventory system."""
        new_product = Product(product_id, name, stock, price)
        self.inventory[product_id] = new_product
        print(f"📦 System: Added {name} (ID: {product_id}) to warehouse stock.")

    def place_order(self, order_id, customer, product_id, quantity):
        """Enqueues a customer order into the processing system."""
        if product_id not in self.inventory:
            print(f"❌ Error: Product ID {product_id} does not exist.")
            return

        new_order = Order(order_id, customer, product_id, quantity)
        self.order_queue.append(new_order)  # Enqueue operation
        print(f"🛒 Order {order_id}: placed by {customer} for {quantity}x item(s).")

    def process_next_order(self):
        """Dequeues and processes the oldest order in the queue."""
        if not self.order_queue:
            print("💤 System: No orders currently waiting in the queue.")
            return

        # Dequeue operation (removes the first item in line)
        current_order = self.order_queue.pop(0)
        product = self.inventory[current_order.product_id]

        print(f"\n⚡ Processing Order {current_order.order_id} [{current_order.timestamp}]...")
        
        # Check stock logic
        if product.reduce_stock(current_order.quantity):
            total_cost = product.price * current_order.quantity
            print(f"✅ Success: Dispatched {current_order.quantity}x '{product.name}' to {current_order.customer_name}.")
            print(f"💰 Total Revenue: ${total_cost:.2f} | Remaining Stock: {product.stock}")
        else:
            print(f"❌ Rejected: Insufficient stock for '{product.name}'. Requested: {current_order.quantity}, Available: {product.stock}")


# ==========================================
# SIMULATION ENGINE
# ==========================================
if __name__ == "__main__":
    print("--- Initializing Smart Inventory Management Setup ---\n")
    shop = InventorySystem()

    # 1. Stocking up the inventory system
    shop.add_new_product("P101", "Wireless Mouse", stock=15, price=25.0)
    shop.add_new_product("P102", "Mechanical Keyboard", stock=5, price=75.0)
    shop.add_new_product("P103", "Gaming Monitor", stock=2, price=299.99)
    print("-" * 50)

    # 2. Customers placing orders concurrently (Incoming Queue)
    shop.place_order(order_id=5001, customer="Amna", product_id="P101", quantity=2)
    shop.place_order(order_id=5002, customer="Ali", product_id="P103", quantity=3)  # Over-purchasing stock
    shop.place_order(order_id=5003, customer="Zainab", product_id="P102", quantity=1)
    print("-" * 50)

    # 3. Processing warehouse queue handling orders sequentially
    shop.process_next_order()  # Processes Amna's order
    shop.process_next_order()  # Processes Ali's order (will fail gracefully due to stock limits)
    shop.process_next_order()  # Processes Zainab's order
    shop.process_next_order()  # Empty line check
