from typing import List, Dict
from decimal import Decimal, ROUND_HALF_UP
from src.dao.cart_dao import CartDAO
from src.dao.menu_dao import MenuDAO
from src.dao.customer_dao import CustomerDAO

class BillingService:
    GST_RATE = Decimal('0.05')

    def __init__(self, menu_dao: MenuDAO, cart_dao: CartDAO, customer_dao: CustomerDAO):
        self.menu_dao = menu_dao
        self.cart_dao = cart_dao
        self.customer_dao = customer_dao

    def calculate_bill(self, cust_id: int) -> Dict:
        cart_items = self.cart_dao.get_cart_items(cust_id)
        if not cart_items:
            raise Exception("Cart is empty for selected customer.")

        menu_items = {item['item_id']: item for item in self.menu_dao.get_all_items()}
        
        items_detail = []
        subtotal = Decimal('0')
        
        for ci in cart_items:
            item = menu_items.get(ci['item_id'])
            if not item:
                continue
            qty = ci['quantity']
            price = Decimal(str(item['item_price']))
            total_price = (price * qty).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            items_detail.append({
                'item_name': item['item_name'],
                'qty': qty,
                'price_per_item': price,
                'total_price': total_price
            })
            subtotal += total_price

        gst = (subtotal * self.GST_RATE).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        total = (subtotal + gst).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

        self.customer_dao.update_total_amount(cust_id, float(total))

        return {
            'items': items_detail,
            'subtotal': subtotal,
            'gst': gst,
            'total': total
        }

    def clear_customer_cart(self, cust_id: int):
        self.cart_dao.clear_cart(cust_id)
