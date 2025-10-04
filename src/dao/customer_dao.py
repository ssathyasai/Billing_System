from supabase import Client
from typing import List, Dict
from datetime import date

class CustomerDAO:
    def __init__(self, client: Client):
        self.client = client

    def get_all_customers(self, owner_id: str) -> List[Dict]:
        try:
            response = self.client.table('customers').select('*').eq('owner_id', owner_id).execute()
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to fetch customers: {response.error.message}")
            return response.data
        except Exception as e:
            print(f"Error fetching customers: {e}")
            return []

    def add_customer(self, owner_id: str, name: str, mobile: str) -> int:
        try:
            response = self.client.table('customers').insert({
                'owner_id': owner_id,
                'cust_name': name,
                'mobile': mobile,
                'date_of_shopping': date.today().isoformat(),
                'total_amount': 0
            }).execute()
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to add customer: {response.error.message}")
            return response.data[0]['cust_id']
        except Exception as e:
            print(f"Error adding customer: {e}")
            raise

    def update_customer(self, owner_id: str, cust_id: int, name: str, mobile: str):
        try:
            response = self.client.table('customers').update({
                'cust_name': name,
                'mobile': mobile
            }).eq('cust_id', cust_id).eq('owner_id', owner_id).execute()
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to update customer: {response.error.message}")
        except Exception as e:
            print(f"Error updating customer: {e}")
            raise

    def delete_customer(self, owner_id: str, cust_id: int):
        try:
            response = self.client.table('customers').delete().eq('cust_id', cust_id).eq('owner_id', owner_id).execute()
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to delete customer: {response.error.message}")
        except Exception as e:
            print(f"Error deleting customer: {e}")
            raise

    def update_total_amount(self, owner_id: str, cust_id: int, amount: float):
        try:
            response = self.client.table('customers').update({
                'total_amount': amount
            }).eq('cust_id', cust_id).eq('owner_id', owner_id).execute()
            if hasattr(response, 'error') and response.error:
                raise Exception(f"Failed to update total amount: {response.error.message}")
        except Exception as e:
            print(f"Error updating total amount: {e}")
            raise
