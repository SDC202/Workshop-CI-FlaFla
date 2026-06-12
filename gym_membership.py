"""
Modulo para la gestion y calculo de costos de membresias de gimnasio.

Este modulo maneja la disponibilidad de planes, caracteristicas adicionales,
recargos por elementos premium y descuentos grupales o por volumen.
"""

from typing import List, Dict

# Catálogo oficial de Planes
BASE_COSTS: Dict[str, int] = {
    "basic": 30,
    "standard": 50,
    "premium": 80,
    "family": 120
}

# Catálogo de características adicionales
FEATURE_COSTS: Dict[str, int] = {
    "pool": 15,
    "trainer": 25,
    "spa": 20,
    "group_classes": 10
}

# Elementos considerados Premium
PREMIUM_ITEMS = {"premium", "spa", "exclusive_facilities", "specialized_training"}


def validate_membership_availability(plan: str, features: List[str]) -> bool:
    """
    Valida si el plan y las caracteristicas adicionales estan disponibles.

    Muestra un mensaje de error explicativo en consola si algun elemento
    no existe en el catalogo oficial.
    """
    if plan not in BASE_COSTS:
        print(f"Error: El plan '{plan}' no existe en nuestro catalogo.")
        return False

    for feature in features:
        if feature not in FEATURE_COSTS:
            print(f"Error: La caracteristica '{feature}' no esta disponible.")
            return False

    return True


def calculate_membership_costs(plan: str, features: List[str], num_members: int) -> dict:
    """
    Calcula subtotales, recargos premium y descuentos aplicables.

    Aplica un 10% de descuento por registro de 2 o mas personas juntas.
    """
    base_cost = BASE_COSTS.get(plan, 0)
    features_cost = sum(FEATURE_COSTS.get(f, 0) for f in features)
    subtotal_por_persona = base_cost + features_cost

    total_acumulado = subtotal_por_persona * num_members

    group_discount = 0
    if num_members >= 2:
        group_discount = total_acumulado * 0.10
        total_acumulado -= group_discount

    has_premium = plan == "premium" or any(f in PREMIUM_ITEMS for f in features)
    premium_surcharge = 0
    if has_premium:
        premium_surcharge = total_acumulado * 0.15
        total_acumulado += premium_surcharge

    special_discount = 0
    if total_acumulado > 400:
        special_discount = 50
    elif total_acumulado > 200:
        special_discount = 20

    total_final = total_acumulado - special_discount

    return {
        "group_discount": int(group_discount),
        "premium_surcharge": int(premium_surcharge),
        "special_discount": int(special_discount),
        "total_final": int(total_final)
    }


def process_gym_membership_flow(
    plan: str, features: List[str], num_members: int, user_confirmed: bool
) -> int:
    """
    Orquesta el flujo completo de la aplicacion de membresias del gimnasio.

    Maneja excepciones y retorna el costo final o -1 ante errores o cancelacion.
    """
    try:
        if num_members <= 0:
            print("Error: El numero de miembros debe ser al menos 1.")
            return -1

        if not validate_membership_availability(plan, features):
            return -1

        resumen = calculate_membership_costs(plan, features, num_members)

        if not user_confirmed:
            print("Operacion Cancelada por el usuario.")
            return -1

        return resumen["total_final"]

    except TypeError:
        print("Error de calculo: Formato invalido en datos de entrada.")
        return -1
