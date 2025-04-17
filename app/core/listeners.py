class UserRegisteredListener:
    def handle_event(self, data):
        print(f"User {data['username']} registered.")
        # Hoş geldin e-posta gönderme vb. işlemler


class OrganizationCreatedListener:
    def handle_event(self, data):
        print(f"Organization {data['name']} created.")
        # Ekstra işlemler: veri tabanı provisioning veya diğer operasyonlar
