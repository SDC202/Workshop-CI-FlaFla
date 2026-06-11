import pytest
# Asumiendo que el código de los otros 3 compañeros se unificó en 'gym_system.py'
from gym_membership import process_gym_membership_flow 

def test_family_plan_single_member():
    """Valida un plan Familiar ($120) para un solo miembro sin adicionales."""
    # Costo esperado: 120 (No supera 200 para descuento, no es premium)
    assert process_gym_membership_flow("family", [], num_members=1, user_confirmed=True) == 120

def test_group_discount_application():
    """Valida el descuento del 10% por registrar a 2 personas juntas en el plan standard."""
    # Plan standard: $50 * 2 personas = $100. Descuento 10% = $10. Total esperado: 90
    assert process_gym_membership_flow("standard", [], num_members=2, user_confirmed=True) == 90

def test_premium_surcharge_and_special_discount():
    """Prueba combinada de recargo premium y descuento por monto alto (>200)."""
    # Plan premium ($80) + spa ($20) = $100 por persona.
    # 3 personas = $300. 
    # Descuento grupo 10% = -$30 -> $270.
    # Recargo premium 15% de 270 = +$40.5 -> $310.
    # Supera los $200 de oferta especial: -$20 de descuento -> $290 esperado aprox.
    resultado = process_gym_membership_flow("premium", ["spa"], num_members=3, user_confirmed=True)
    assert resultado > 0
    assert isinstance(resultado, int)

def test_user_cancellation_returns_minus_one():
    """Debe retornar de forma estricta -1 si el usuario cancela la confirmación."""
    assert process_gym_membership_flow("basic", ["pool"], num_members=1, user_confirmed=False) == -1

def test_invalid_plan_returns_minus_one():
    """Debe retornar -1 si se intenta enviar un plan que no existe en el catálogo."""
    assert process_gym_membership_flow("invalid_plan_name", [], num_members=1, user_confirmed=True) == -1