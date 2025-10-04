from src.config.supabase_config import SupabaseConfig

class Auth:
    def __init__(self):
        config = SupabaseConfig()
        self.client = config.get_client()

    def signup(self, email: str, password: str):
        return self.client.auth.sign_up({"email": email, "password": password})

    def login(self, email: str, password: str):
        return self.client.auth.sign_in_with_password({"email": email, "password": password})

    def logout(self):
        return self.client.auth.sign_out()

    def get_current_user(self):
        user_resp = self.client.auth.get_user()
        if user_resp and user_resp.user:
            return user_resp.user
        return None

    def update_user(self, data: dict):
        return self.client.auth.update_user(data)
