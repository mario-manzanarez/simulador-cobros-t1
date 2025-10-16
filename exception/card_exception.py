class InvalidCardNumberException(Exception):
    def __init__(self):
        self.message = "El número de tarjeta no es valido"
        super().__init__(self.message)
