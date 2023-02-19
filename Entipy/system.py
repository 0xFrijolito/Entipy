from ECS import get_component_type_id

class System:
    def __init__(self, context:object, priority:int):
        self.component_ids = []
        
        self.context = context
        self.priority = priority

    def start (self) -> None:
        pass

    def is_participant (self, entity:'Entity') -> bool:
        for component_id in self.component_ids:
            if entity.components[component_id] is None:
                return False
        return True

    def get_participats (self) -> list['Entity']:
        for entity in self.context.entities:
            if self.is_participant(entity):
                yield entity

    def attach_component (self, ComponentType:callable) -> None:
        self.component_ids.append(get_component_type_id(ComponentType))
        return self

    def dettach_component (self, ComponentType:callable) -> None:
        self.component_ids.remove(get_component_type_id(ComponentType))
        return self

    def update (self) -> None:
        raise NotImplemented

# Create the script system
class ScriptSystem (System):
    def start (self):
        pass

    def update (self) -> None:
        for entity in self.get_participats():
            for component_id in self.component_ids:
                entity.components[component_id].update()