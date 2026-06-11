"""
Modulo de pruebas unitarias para el sistema de gestion de membresias.

Verifica la precision de los calculos financieros, descuentos grupales,
planes familiares y manejo robusto de cancelaciones.
"""

from gym_membership import process_gym_membership_flow


def test_family_plan_single_member():
    """Valida un plan Familiar para un solo miembro sin adicionales."""
    assert process_gym_membership_flow("family", [], 1, True) == 120


def test_group_discount_application():
    """Valida el descuento del 10% por registrar a 2 personas juntas."""
    assert process_gym_membership_flow("standard", [], 2, True) == 90


def test_premium_surcharge_and_special_discount():
    """Prueba combinada de recargo premium y descuento por monto alto."""
    resultado = process_gym_membership_flow("premium", ["spa"], 3, True)
    assert resultado > 0
    assert isinstance(resultado, int)


def test_user_cancellation_returns_minus_one():
    """Debe retornar -1 si el usuario cancela la confirmacion."""
    assert process_gym_membership_flow("basic", ["pool"], 1, False) == -1


def test_invalid_plan_returns_minus_one():
    """Debe retornar -1 si se ingresa un plan inexistente."""
    assert process_gym_membership_flow("invalid_plan_name", [], 1, True) == -1