from ECS import get_component_type_id, MAX_COMPONENTS
from ECS.component import Component, CalleableComponent

class Entity:
    def __init__ (self, context:object=None, tag:str=None, layer:int=None):
        # Iniciamos una entidad con el componente Transform por defecto
        self.components = [None] * MAX_COMPONENTS
        self.active  = True
        
        self.context = context
        self.tag = tag
        self.layer = layer

    def add_component (self, ComponentType:callable, *args:tuple) -> 'Entity':
        # Creamos el componente y le asignamos su dueno 
        new_component = ComponentType()
        new_component.start(*args)
        new_component.owner = self

        # Checkeamos si es un script, si es asi lo agregamos el sistema de scripts
        if ComponentType.__base__ == CalleableComponent:
            self.context.script_system.attach_component(ComponentType)

        # Guardamos el componente en la array de componentes
        component_id = get_component_type_id(ComponentType)
        self.components[component_id] = new_component

        return self
    
    def delete_component (self, ComponentType:callable) -> 'Entity':
        # Verificamos si existe el componente dentro de la entidad
        if not self.has_component(ComponentType):
            print(f"Current entity don't have the component {ComponentType}")

        # Eliminamos la referencia a el componente lo que lo elimina 💣
        self.components[get_component_type_id(ComponentType)] = None
        
        return self

    def has_component (self, ComponentType:callable) -> bool:
        return not self.components[get_component_type_id(ComponentType)] is None

    def get_component (self, ComponentType:callable) -> 'Component':
        if not self.has_component(ComponentType):
            print(f"Current entity don't have the component {ComponentType}")

        return self.components[get_component_type_id(ComponentType)]

    def get_component_in_children (self) -> Component: 
        raise NotImplemented
    
    def get_component_in_parent (self) -> Component: 
        raise NotImplemented