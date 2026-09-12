from decimal import Decimal
from backend.core.constants import CONTRACT_BOQ_ITEM_COUNT, CONTRACT_BOQ_TOTAL_PKR
from backend.core.money import to_decimal

def test_boq_count_and_total(client, contractor_token):
    headers = {"Authorization": f"Bearer {contractor_token}"}
    res = client.get("/api/boq", headers=headers)
    assert res.status_code == 200
    items = res.json()
    assert len(items) == CONTRACT_BOQ_ITEM_COUNT, f"Expected {CONTRACT_BOQ_ITEM_COUNT} items, got {len(items)}"

    total = Decimal("0.00")
    for it in items:
        total += to_decimal(it["amount_pkr"])

    assert total == CONTRACT_BOQ_TOTAL_PKR, f"Expected PKR {CONTRACT_BOQ_TOTAL_PKR}, got {total}"

def test_specific_boq_items(client, contractor_token):
    headers = {"Authorization": f"Bearer {contractor_token}"}
    res = client.get("/api/boq", headers=headers)
    assert res.status_code == 200
    items_by_num = {it["item_number"]: it for it in res.json()}

    # Item 5: Concrete RCC
    item5 = items_by_num[5]
    assert to_decimal(item5["contract_qty"]) == Decimal("2.44")
    assert to_decimal(item5["rate_pkr"]) == Decimal("42000.00")
    assert to_decimal(item5["amount_pkr"]) == Decimal("102480.00")

    # Item 8: Masonry
    item8 = items_by_num[8]
    assert to_decimal(item8["contract_qty"]) == Decimal("30.79")
    assert to_decimal(item8["rate_pkr"]) == Decimal("15500.00")
    assert to_decimal(item8["amount_pkr"]) == Decimal("477245.00")

    # Item 6: Reinforcement
    item6 = items_by_num[6]
    assert to_decimal(item6["contract_qty"]) == Decimal("7500.00")
    assert to_decimal(item6["rate_pkr"]) == Decimal("285.00")
    assert to_decimal(item6["amount_pkr"]) == Decimal("2137500.00")

def test_boq_immutability(client, contractor_token):
    headers = {"Authorization": f"Bearer {contractor_token}"}
    # Attempting to mutate or delete BOQ items must return 403 Forbidden
    res1 = client.post("/api/boq", json={"category": "Fake"}, headers=headers)
    assert res1.status_code == 403

    res2 = client.put("/api/boq/1", json={"rate_pkr": 999999}, headers=headers)
    assert res2.status_code == 403

    res3 = client.delete("/api/boq/1", headers=headers)
    assert res3.status_code == 403
