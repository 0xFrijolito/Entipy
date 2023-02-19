from ECS import MAX_ENTITIES, MAX_COMPONENTS, MAX_SYSTEMS
from ECS.entity import Entity
from ECS.component import Component
from ECS.system import System, ScriptSystem

class EntityManager:
    def __init__(self, start_component:callable=None, start_component_args:tuple=None) -> None:
        self.entities = []
        self.systems = []

        # Custom components start, most probably a position component
        self.start_component = start_component
        self.start_component_args = start_component_args

        self.script_system = self.create_system(ScriptSystem, 100)

    def create_entity (self) -> Entity:
        if len(self.entities) >= MAX_ENTITIES:
            print('Warning: max amount of entities')

        # We create a empty entity
        new_entity = Entity(context=self) 
        if not self.start_component is None:
            new_entity.add_component(self.start_component, self.start_component_args)

        self.entities.append(new_entity)
                
        return new_entity

    def insert_system (self, new_system:'System') -> None:
        size = len(self.systems)
        if size == 0:
            self.systems.append(new_system)
            return 

        for index, system in enumerate(self.systems):
            if new_system.priority <= system.priority:
                self.systems = self.systems[:index] + [new_system] + self.systems[index:]
                return

        self.systems.append(new_system)

    def create_system (self, system:callable, priority:int) -> Entity:
        if len(self.systems) >= MAX_SYSTEMS:
            print('Warning: max amount of systems')
        
        # Create new system and append to the list 
        new_system = system(self, priority)
        new_system.start()
        self.insert_system(new_system)
         
        return new_system
 
    def update (self) -> None:
        # Process each system component 
        for system in self.systems:
            system.update()

        # Call each component script 
        # for entity in self.entities:
        #     for component in entity.components:
        #         if component.is_calleable:
        #             component.update ()

