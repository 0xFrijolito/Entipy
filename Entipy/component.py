class Component:
    def __init__ (self) -> None:
        self.owner = None

        self.was_called = False
        self.active = False

    def start (self) -> None:
        raise NotImplemented

class CalleableComponent (Component):
    def __init__ (self) -> None:
        # Call the component contructor 
        super().__init__()

    def update (self) -> None:
        raise NotImplemented

class PlayerControler (CalleableComponent):
    def start (self, x:float) -> None:
        self.x = x

    def update (self):
        print(self.x)