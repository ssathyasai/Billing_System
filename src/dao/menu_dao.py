from supabase import Client
from typing import List, Dict

class MenuDAO:
    def __init__(self, client: Client):
        self.client = client

    def get_all_items(self) -> List[Dict]:
        try:
            response = self.client.table('menu').select('*').execute()
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to fetch menu: {response.error.message}")
            return response.data
        except Exception as e:
            print(f"Error fetching menu items: {e}")
            return []

    def add_item(self, name: str, price: float):
        try:
            response = self.client.table('menu').insert({'item_name': name, 'item_price': price}).execute()
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to add menu item: {response.error.message}")
        except Exception as e:
            print(f"Error adding menu item: {e}")
            raise

    def update_item(self, item_id: int, name: str, price: float):
        try:
            response = self.client.table('menu').update({'item_name': name, 'item_price': price}).eq('item_id', item_id).execute()
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to update menu item: {response.error.message}")
        except Exception as e:
            print(f"Error updating menu item: {e}")
            raise

    def delete_item(self, item_id: int):
        try:
            response = self.client.table('menu').delete().eq('item_id', item_id).execute()
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to delete menu item: {response.error.message}")
        except Exception as e:
            print(f"Error deleting menu item: {e}")
            raise
