class UserRegisteredListener:
    def handle_event(self, data):
        print(f"User {data['username']} registered.")


class OrganizationCreatedListener:
    def handle_event(self, data):
        print(f"Organization {data['name']} created.")
