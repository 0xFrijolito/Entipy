MAX_SYSTEMS = 512
MAX_COMPONENTS = 512
MAX_ENTITIES = 8192

current_id = 0
priority_list = {}
component_id_table = {}

def get_component_type_id (ComponentType:callable):
    global current_id

    if component_id_table.get(ComponentType) is None:
        # Creamos un id para el component_type si es que no lo tenia antes
        component_id_table[ComponentType] = current_id
        current_id += 1 
    
    return component_id_table[ComponentType]
