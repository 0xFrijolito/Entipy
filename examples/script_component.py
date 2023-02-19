import keyboard

from dataclasses import dataclass

from ECS.entity_manager import EntityManager
from ECS.component import Component, CalleableComponent

@dataclass
class Vector3:
    x:float
    y:float
    z:float

class Transform(Component):
    def start (self) -> None:
        self.position = Vector3(0, 0, 0)
        self.scale = Vector3(0, 0, 0)
        self.angle = 0

class PlayerControler (CalleableComponent):
    def start (self):
        pass

    def update (self):
        self.owner.get_component(Transform).position.x += 0.1

def main () -> None:
    # We create a context 
    entity_manager = EntityManager()

    # Create the player entity and add a component
    player = entity_manager.create_entity()
    player.add_component(Transform) \
          .add_component(PlayerControler)

    while True:
        entity_manager.update ()
        print(player.get_component(Transform).position)

if __name__ == "__main__":
    main ()