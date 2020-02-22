class Mailer:
    def send(self, email: str):
        print(f"Sending mail to {email}")


class RegisterService:
    def __init__(self):
        self.mailer = Mailer()

    def register(self, email: str):
        print(f"Registering user {email}")
        self.mailer.send(email)


register_service = RegisterService()
register_service.register("petru@pepy.tech")

import pinject


class Mailer:
    def send(self, email: str):
        print(f"Sending mail to {email}")


class RegisterService:
    def __init__(self, mailer: Mailer):
        self.mailer = mailer

    def register(self, email: str):
        print(f"Registering user {email}")
        self.mailer.send(email)


obj_graph = pinject.new_object_graph()
register_service = obj_graph.provide(RegisterService)
register_service.register("petru@pepy.tech")
