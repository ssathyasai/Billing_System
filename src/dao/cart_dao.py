from supabase import Client
from typing import List, Dict

class CartDAO:
    def __init__(self, client: Client):
        self.client = client

    def add_to_cart(self, owner_id: str, cust_id: int, item_id: int, quantity: int):
        try:
            existing = self.client.table('cart').select('*') \
                .eq('owner_id', owner_id) \
                .eq('cust_id', cust_id) \
                .eq('item_id', item_id).execute()

            if hasattr(existing, 'error') and existing.error:
                raise Exception(f"Failed to check existing cart item: {existing.error.message}")

            if existing.data and len(existing.data) > 0:
                existing_qty = existing.data[0]['quantity']
                new_qty = existing_qty + quantity
                cart_id = existing.data[0]['cart_id']
                response = self.client.table('cart').update({'quantity': new_qty}) \
                    .eq('cart_id', cart_id).execute()
            else:
                response = self.client.table('cart').insert({
                    'owner_id': owner_id,
                    'cust_id': cust_id,
                    'item_id': item_id,
                    'quantity': quantity
                }).execute()

            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to add/update cart: {response.error.message}")

        except Exception as e:
            print(f"Error adding to cart: {e}")
            raise

    def get_cart_items(self, owner_id: str, cust_id: int) -> List[Dict]:
        try:
            response = self.client.table('cart').select('cart_id, item_id, quantity') \
                .eq('owner_id', owner_id).eq('cust_id', cust_id).execute()
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to fetch cart items: {response.error.message}")
            return response.data
        except Exception as e:
            print(f"Error fetching cart items: {e}")
            return []

    def clear_cart(self, owner_id: str, cust_id: int):
        try:
            response = self.client.table('cart').delete().eq('owner_id', owner_id).eq('cust_id', cust_id).execute()
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to clear cart: {response.error.message}")
        except Exception as e:
            print(f"Error clearing cart: {e}")
            raise
