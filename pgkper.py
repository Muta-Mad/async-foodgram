# test_generics.py
def test1() -> int[str]:  # ← Должна быть ошибка с disallow_any_generics
    return 42

def test2() -> list[str]:  # ← OK
    return ["hello"]

def test3() -> dict[str, int]:  # ← OK
    return {"a": 1}   