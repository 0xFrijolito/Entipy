# Entipy | Entity Component System for python

This is a lightweight Entity Component System (ECS) framework written in Python. It provides a simple and efficient way to build game entities and their behavior. It is similar to the ECS implementation used in Unity game engine.

## Installation

To use this framework, you need to have Python 3 installed on your system.

```bash
git clone https://github.com/0xFrijolito/entipy
mv Entipy/Entity <your_project_folder>
```

We are working to be able to use pip in the Entipy installation

## Usage

The ECS framework consists of three main components: Entity, Component, and System.

### Entity 

The `Entity` class represents a game entity. It is a container for components and provides a unique identifier for each entity. To create an entity, you simply need to instantiate the `Entity` to create and empty `Entity` thats mean a entity without any component

```python
from Entipy.entity_manager import EntityManager

entity_manager = EntityManager ():

player_entity = entity_manager.create_entity ()
print(player_entity.componets) # []
```

### Component

The `Component` class represents a behavior or attribute of an entity. It contains data and logic specific to that behavior or attribute. To create a component, you need to subclass the Component class and define the data and logic:

```python
from Entipy.component import Component

@dataclass
class Vector3:
    x:float
    y:float
    z:float

class Transform (Component):
    # This method is called when the components is attach to the entity
    def start (self, position:Vector3, scale:Vector3, angle:float) -> None:
        self.position = position
        self.scale = scale
        self.angle = angle

class Body (Component):
    def start (self, mass:float, velocity:Vector3, acceleration:Vector3) -> None:
        self.mass = mass
        self.velocity = velocity
        self.acceleration = acceleration

    def apply_force (self, force:Vector3) -> None:
        self.acceleration.x = force.x / self.mass
        self.acceleration.y = force.y / self.mass
        self.acceleration.z = force.z / self.mass
```

### System

The System class represents a set of behaviors that operate on a specific set of entities. It contains the logic for updating the entities and their components. To create a system, you need to subclass the System class and define the update logic:

```python
from Entipy.system import System

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
                mag_f = self.gravitational_constant * ((m1 * m2) / d + self.offset)

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
```

### Entity Manager 

The `EntityManager` class represents the game or simulation context. It contains a collection of entities, components, and systems. To create a `EntityManager`, you simply need to instantiate the `EntityManager` class:

```python
from Entipy.entity_manager import EntityManager

entity_manager = EntityManager ():

# Create a new entity in the context of the entity_manager, this means this entity only interact with other entities of the same manager
player = entity_manager.create_entity ()
```

### Adding Components and Entities and using a system.

To add a component to an entity, you can simply use the add_component method. and if you want an entity to interact with a system, you need to attach a component to a system, and if the entity has the component automatically, this entity is used in the system.

using the last examples of the component and entities 

```python
from Entipy.entity_manager import EntityManager
from Entipy.component import Component
from Entipy.system import System

def main () -> None:
    entity_manager = EntityManager ()

    # Create a entity and add components 😎
    planet1 = entity_manager.create_entity ()
    planet1.add_component(Transform, Vector3(0, 0, 0), Vector3(1, 1, 1), 0) \
           .add_component(Body, 1.989e30, Vector3(0, 0, 0), Vector3(0, 0, 0))

    planet2 = entity_manager.create_entity ()
    planet2.add_component(Transform, Vector3(150_000_000, 0, 0), Vector3(1, 1, 1), 0) \
           .add_component(Body, 5.972e24, Vector3(0, 0, 0), Vector3(0, 0, 0))

    physic_system = entity_manager.create_system(N_BodySimulation, 1)
    physic_system.attach_component(Body) \
                 .attach_component(Transform)

    # Game loop ➰
    while True:
        entity_manager.update ()

if __name__ == "__main__":
    main ()
```

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/0xFrijolito/entipy. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the Contributor Covenant code of conduct
