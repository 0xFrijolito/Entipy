from dataclasses import dataclass

from ECS.entity_manager import EntityManager
from ECS.component import Component
from ECS.system import System

@dataclass
class Vector3:
    x:float
    y:float
    z:float

class Transform (Component):
    def start (self, position:Vector3, scale:Vector3) -> None:
        self.position = position
        self.scale = scale

class Body (Component):
    def start (self, mass:float, velocity:Vector3, acceleration:Vector3) -> None:
        self.mass = mass
        self.velocity = velocity
        self.acceleration = acceleration

    def apply_force (self, force:Vector3) -> None:
        self.acceleration.x = force.x / self.mass
        self.acceleration.y = force.y / self.mass
        self.acceleration.z = force.z / self.mass

class PhysicSystem (System):
    def start (self) -> None:
        self.gravitational_constant = 6.67e-11
        self.offset = 0.001             

    def update (self) -> None:
        entities = list(self.get_participats())

        for entity1 in entities:
            for entity2 in entities:
                # Check if the 2 entities are the same 
                if entity1 == entity2:
                    continue

                # Obtain the positions
                p1 = entity1.get_component(Transform).position
                p2 = entity2.get_component(Transform).position

                # Obtain the masses
                m1 = entity1.get_component(Body).mass
                m2 = entity1.get_component(Body).mass

                # calculate the distances
                dx = p1.x - p2.x
                dy = p1.y - p2.y
                dz = p1.z - p2.z

                d = dx**2 + dy**2 + dz**2

                # Calcule the magnitude of the force what entity1 apply over entity2 
                mag_f = self.gravitational_constant * ((m1 * m2) / d**2 + self.offset)

                # Using trigonometric to obtain the force vector
                fx = mag_f * (dx / d)
                fy = mag_f * (dy / d)
                fz = mag_f * (dz / d)

                force = Vector3(fx, fy, fz)

                # Apply the force to the entity1
                entity2.get_component(Body).apply_force(force)

        for entity in entities:
            # Obtain the positions
            position = entity.get_component(Transform).position
            velocity = entity.get_component(Body).velocity
            acceleration = entity.get_component(Body).acceleration

            # Calculate the new velocity
            velocity.x += acceleration.x
            velocity.y += acceleration.y
            velocity.z += acceleration.z

            # Calculate the new positions
            position.x += velocity.x
            position.y += velocity.y
            position.z += velocity.z
        

def main () -> None:
    entity_manager = EntityManager()

    planet1 = entity_manager.create_entity()
    planet1.add_component(Transform, Vector3(0, 0, 0), Vector3(1, 1, 1)) \
           .add_component(Body, 1.989e30, Vector3(0, 0, 0), Vector3(0, 0, 0))

    planet2 = entity_manager.create_entity()
    planet2.add_component(Transform, Vector3(150_000_000, 0, 0), Vector3(1, 1, 1)) \
           .add_component(Body, 5.972e24, Vector3(0, 0, 0), Vector3(0, 0, 0))

    physic_system = entity_manager.create_system(PhysicSystem, 1)
    physic_system.attach_component(Body) \
                 .attach_component(Transform)

    print(entity_manager.systems)
                    
    while True:
        entity_manager.update()

        print(planet1.get_component(Transform).position)
        print(planet2.get_component(Transform).position)

if __name__ == "__main__":
    main ()