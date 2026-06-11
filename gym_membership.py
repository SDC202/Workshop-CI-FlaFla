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

def calculate_membership_costs(plan: str, features: List[str], num_members: int) -> dict:
    """
    [Requerimientos 3, 4] Calcula subtotales, recargos y descuentos aplicables.
    Maneja el descuento del 10% si se registran 2 o más personas juntas en el mismo plan.
    """
    # 1. Costo Base y Adicionales por cada miembro individual
    base_cost = BASE_COSTS.get(plan, 0)
    features_cost = sum(FEATURE_COSTS.get(f, 0) for f in features)
    subtotal_por_persona = base_cost + features_cost
    
    # Costo acumulado por el total de miembros inscritos juntos
    total_acumulado = subtotal_por_persona * num_members
    
    # ---- [Requerimiento 4: Discounts for Group Memberships] ----
    group_discount = 0
    if num_members >= 2:
        print(f"¡Aviso de Ahorro! Se ha aplicado un 10% de descuento por registro grupal ({num_members} miembros).")
        group_discount = total_acumulado * 0.10
        total_acumulado -= group_discount

    # ---- [Requerimiento 4-Premium: Premium Membership Features] ----
    # Se aplica el 15% de recargo si el plan es premium o contiene un adicional premium
    has_premium_feature = plan == "premium" or any(f in PREMIUM_ITEMS for f in features)
    premium_surcharge = 0
    if has_premium_feature:
        premium_surcharge = total_acumulado * 0.15
        total_acumulado += premium_surcharge

    # ---- [Requerimiento 3: Special Offer Discounts] ----
    special_discount = 0
    if total_acumulado > 400:
        special_discount = 50
    elif total_acumulado > 200:
        special_discount = 20
        
    total_final = total_acumulado - special_discount
    
    # Retornamos un desglose para que el Integrante 3 pueda mostrar la confirmación
    return {
        "subtotal": int(subtotal_por_persona * num_members),
        "group_discount": int(group_discount),
        "premium_surcharge": int(premium_surcharge),
        "special_discount": int(special_discount),
        "total_final": int(total_final)
    }


# Importa las funciones del Integrante 1 e Integrante 2

def process_gym_membership_flow(plan: str, features: List[str], num_members: int, user_confirmed: bool) -> int:
    """
    [Requerimientos 6, 7 y 8] Orquesta el flujo completo de la aplicación.
    Maneja errores con robustez y retorna el formato entero solicitado o -1.
    """
    # ---- [Requerimiento 8: Error Handling] ----
    try:
        # Validación de parámetros básicos de entrada
        if num_members <= 0:
            print("Error: El número de miembros inscritos debe ser al menos 1.")
            return -1

        # ---- [Requerimiento 5: Membership Availability] ----
        if not validate_membership_availability(plan, features):
            return -1

        # Realizar los cálculos matemáticos
        resumen = calculate_membership_costs(plan, features, num_members)
        
        # ---- [Requerimiento 6: User Confirmation] ----
        print("\n==============================================")
        print("          RESUMEN DE COTIZACIÓN GYM           ")
        print("==============================================")
        print(f"Plan base seleccionado: {plan.upper()}")
        print(f"Miembros registrados: {num_members}")
        print(f"Características Extra: {', '.join(features) if features else 'Ninguna'}")
        print(f"Descuento de Grupo (10%): -${resumen['group_discount']}")
        print(f"Recargo de Elementos Premium (15%): +${resumen['premium_surcharge']}")
        print(f"Descuento Oferta Especial: -${resumen['special_discount']}")
        print("----------------------------------------------")
        print(f"COSTO TOTAL ESTIMADO: ${resumen['total_final']}")
        print("==============================================\n")

        # Evaluar la decisión o estado de confirmación del cliente
        if not user_confirmed:
            print("Operación Cancelada: El usuario rechazó los términos o decidió cambiar su selección.")
            return -1

        # ---- [Requerimiento 7: Output] ----
        print("¡Membresía registrada con éxito!")
        return resumen["total_final"]

    except TypeError:
        print("Error de cálculo: Se detectó un formato inválido en los datos de entrada.")
        return -1
    except Exception as e:
        print(f"Error inesperado en el sistema: {str(e)}")
        return -1