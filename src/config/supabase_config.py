import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class SupabaseConfig:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        if not self.url or not self.key:
            raise ValueError("Supabase URL/Key missing in environment variables")
        self.client: Client = create_client(self.url, self.key)

    def get_client(self):
        return self.client
