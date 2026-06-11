from typing import List, Dict

# Catálogo oficial de Planes (Se incluye Basic, Premium y Family de forma explícita)
BASE_COSTS: Dict[str, int] = {
    "basic": 30,
    "standard": 50,
    "premium": 80,
    "family": 120  # Agregado según el requerimiento 1 del documento
}

# Catálogo de características adicionales con sus costos individuales
FEATURE_COSTS: Dict[str, int] = {
    "pool": 15,
    "trainer": 25,
    "spa": 20,
    "group_classes": 10
}

# Definición de elementos considerados "Premium" para el recargo posterior
PREMIUM_ITEMS = {"premium", "spa", "exclusive_facilities", "specialized_training"}


def validate_membership_availability(plan: str, features: List[str]) -> bool:
    if plan not in BASE_COSTS:
        print(f"Error: El plan de membresía '{plan}' no existe en nuestro catálogo.")
        return False
        
    for feature in features:
        if feature not in FEATURE_COSTS:
            print(f"Error: La característica adicional '{feature}' no está disponible.")
            return False
            
    return True