from dataclasses import dataclass

from ECS.entity import Entity
from ECS.component import Component

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

def main () -> None:
    # We create a context 
    entity_manager = EntityManager()

    # Create the player entity and add a component
    player = entity_manager.create_entity()
    player.add_component(Transform)

    player_position = player.get_component(Transform).position
    print(f"player position: {player_position}")


if __name__ == "__main__":
    main ()