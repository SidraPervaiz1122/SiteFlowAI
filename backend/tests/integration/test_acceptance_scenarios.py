import io
from decimal import Decimal
from backend.core.money import to_decimal

def test_acceptance_scenario_item_8_full_lifecycle(client, contractor_token, re_token, client_token):
    """
    Acceptance Test 1: Full end-to-end lifecycle for BOQ Item 8 (Brick/block masonry).
    Contractor -> Check Request -> Evidence -> AI Pre-review -> RE Inspection ->
    Observation -> Accept -> Submit Qty 10 m³ -> RE Approve -> Client Approve -> IPC Generation.
    """
    contractor_headers = {"Authorization": f"Bearer {contractor_token}"}
    re_headers = {"Authorization": f"Bearer {re_token}"}
    client_headers = {"Authorization": f"Bearer {client_token}"}

    # 1. Contractor finds BOQ Item 8
    boq_res = client.get("/api/boq", headers=contractor_headers)
    assert boq_res.status_code == 200
    boq_items = {it["item_number"]: it for it in boq_res.json()}
    item8 = boq_items[8]
    assert item8["description"] == "Brick/block masonry"
    assert to_decimal(item8["contract_qty"]) == Decimal("30.79")
    assert to_decimal(item8["rate_pkr"]) == Decimal("15500.00")

    # 2. Contractor creates Check Request for Item 8
    cr_res = client.post("/api/check-requests", json={
        "boq_item_id": item8["id"],
        "title": "Ground Floor Masonry Works — Axis 1-4",
        "description": "Brick masonry laying in 1:6 cement sand mortar",
        "proposed_qty": 10.00
    }, headers=contractor_headers)
    assert cr_res.status_code == 200
    cr = cr_res.json()
    cr_id = cr["id"]
    assert cr["status"] == "DRAFT"

    # 3. Contractor uploads evidence photo
    dummy_file = io.BytesIO(b"fake image data for site masonry inspection")
    upload_res = client.post(
        f"/api/check-requests/{cr_id}/evidence",
        files={"file": ("site_masonry_progress.jpg", dummy_file, "image/jpeg")},
        data={"caption": "Wall alignment and mortar joints"},
        headers=contractor_headers
    )
    assert upload_res.status_code == 200

    # 4. Contractor submits Check Request (triggers AI pre-review)
    submit_res = client.post(f"/api/check-requests/{cr_id}/submit", headers=contractor_headers)
    assert submit_res.status_code == 200
    cr_submitted = submit_res.json()
    assert cr_submitted["status"] == "PENDING_INSPECTION"
    assert len(cr_submitted["ai_reviews"]) > 0
    ai_rev = cr_submitted["ai_reviews"][0]
    assert ai_rev["readiness"] in ["Ready", "Needs Attention"]

    # 5. RE opens inspection workspace
    insp_res = client.post(f"/api/inspections/start/{cr_id}", headers=re_headers)
    assert insp_res.status_code == 200
    inspection = insp_res.json()
    inspection_id = inspection["id"]

    # 6. RE generates AI draft observation
    ai_draft_res = client.post(f"/api/inspections/{inspection_id}/ai-draft?hint=mortar", headers=re_headers)
    assert ai_draft_res.status_code == 200
    ai_obs = ai_draft_res.json()
    assert "Mortar" in ai_obs["title"] or "masonry" in ai_obs["description"].lower()

    # 7. RE records observation
    obs_res = client.post(f"/api/inspections/{inspection_id}/observations", json={
        "title": ai_obs["title"],
        "description": ai_obs["description"],
        "severity": ai_obs["severity"],
        "category": ai_obs["category"],
        "corrective_action": ai_obs["recommended_action"],
        "is_ai_generated": True
    }, headers=re_headers)
    assert obs_res.status_code == 200

    # 8. RE accepts inspection
    decide_res = client.post(f"/api/inspections/{inspection_id}/decide", json={
        "decision": "ACCEPT",
        "inspector_notes": "Plumb and alignment verified. Mortar curing confirmed."
    }, headers=re_headers)
    assert decide_res.status_code == 200

    # Verify CR status is now INSPECTION_ACCEPTED
    cr_check = client.get(f"/api/check-requests/{cr_id}", headers=re_headers).json()
    assert cr_check["status"] == "INSPECTION_ACCEPTED"

    # 9. Contractor submits actual quantity (10.00 m³)
    qty_submit_res = client.post("/api/quantities/submit", json={
        "check_request_id": cr_id,
        "submitted_qty": 10.00,
        "contractor_notes": "Measured actual in-place masonry volume"
    }, headers=contractor_headers)
    assert qty_submit_res.status_code == 200
    measurement_id = qty_submit_res.json()["id"]

    # 10. RE approves quantity 10.00 m³
    re_appr_res = client.post("/api/approvals/re", json={
        "quantity_measurement_id": measurement_id,
        "approved_qty": 10.00,
        "status": "APPROVED",
        "re_comments": "Verified against site dimensions"
    }, headers=re_headers)
    assert re_appr_res.status_code == 200
    approval_data = re_appr_res.json()
    approval_id = approval_data["id"]

    # Verify Amount = PKR 155,000 (10.00 * 15,500)
    assert to_decimal(approval_data["approved_amount_pkr"]) == Decimal("155000.00")

    # Verify BOQ Remaining = 20.79 m³ (30.79 - 10.00)
    boq_item8_updated = client.get(f"/api/boq/{item8['id']}", headers=re_headers).json()
    assert to_decimal(boq_item8_updated["approved_qty"]) == Decimal("10.0000")
    assert to_decimal(boq_item8_updated["remaining_qty"]) == Decimal("20.7900")
    assert to_decimal(boq_item8_updated["approved_amount_pkr"]) == Decimal("155000.00")

    # 11. Client reviews and approves the work
    client_review_res = client.post("/api/client-reviews", json={
        "quantity_approval_id": approval_id,
        "decision": "APPROVED",
        "comments": "Inspected photos and verified RE approval"
    }, headers=client_headers)
    assert client_review_res.status_code == 200

    # 12. Check IPC eligibility
    elig_res = client.get("/api/ipc/eligible", headers=client_headers)
    assert elig_res.status_code == 200
    elig_data = elig_res.json()
    assert elig_data["eligible_items_count"] >= 1
    assert to_decimal(elig_data["total_eligible_amount_pkr"]) >= Decimal("155000.00")

    # 13. Generate IPC
    ipc_gen_res = client.post("/api/ipc/generate", json={
        "period_start": "2026-09-01",
        "period_end": "2026-09-30",
        "notes": "First interim billing for ground floor masonry"
    }, headers=client_headers)
    assert ipc_gen_res.status_code == 200
    ipc = ipc_gen_res.json()
    assert ipc["ipc_number"] == "IPC-001"
    assert to_decimal(ipc["total_current_amount_pkr"]) >= Decimal("155000.00")

    # Verify IPC item has exactly 10.00 m³ * PKR 15,500 = PKR 155,000
    ipc_masonry_item = next(it for it in ipc["items"] if it["boq_item_id"] == item8["id"])
    assert to_decimal(ipc_masonry_item["approved_qty"]) == Decimal("10.0000")
    assert to_decimal(ipc_masonry_item["contract_rate_pkr"]) == Decimal("15500.00")
    assert to_decimal(ipc_masonry_item["amount_pkr"]) == Decimal("155000.00")

    # 14. Verify Audit Trail contains all major actions
    audit_res = client.get("/api/audit", headers=client_headers)
    assert audit_res.status_code == 200
    actions = [a["action"] for a in audit_res.json()]
    assert "CR_CREATED" in actions
    assert "CR_SUBMITTED" in actions
    assert "INSPECTION_DECIDED" in actions
    assert "QUANTITY_SUBMITTED" in actions
    assert "RE_QUANTITY_APPROVED" in actions
    assert "CLIENT_APPROVED" in actions
    assert "IPC_GENERATED" in actions


def test_acceptance_scenario_item_5_over_approval_prevention(client, contractor_token, re_token):
    """
    Acceptance Test 2: BOQ Item 5 (RCC works).
    Contract = 2.44 m³ @ PKR 42,000.
    Approve 1.00 m³ -> Amount = PKR 42,000, Remaining = 1.44 m³.
    Attempt 1.50 m³ -> REJECTED by backend (exceeds remaining 1.44 m³).
    """
    contractor_headers = {"Authorization": f"Bearer {contractor_token}"}
    re_headers = {"Authorization": f"Bearer {re_token}"}

    # Find Item 5
    boq_items = {it["item_number"]: it for it in client.get("/api/boq", headers=re_headers).json()}
    item5 = boq_items[5]
    assert to_decimal(item5["contract_qty"]) == Decimal("2.44")
    assert to_decimal(item5["rate_pkr"]) == Decimal("42000.00")

    # Step A: First request for 1.00 m³
    cr1 = client.post("/api/check-requests", json={
        "boq_item_id": item5["id"],
        "title": "RCC Columns Pouring — Phase 1",
        "proposed_qty": 1.00
    }, headers=contractor_headers).json()

    client.post(f"/api/check-requests/{cr1['id']}/submit", headers=contractor_headers)
    insp1 = client.post(f"/api/inspections/start/{cr1['id']}", headers=re_headers).json()
    client.post(f"/api/inspections/{insp1['id']}/decide", json={"decision": "ACCEPT"}, headers=re_headers)

    qty_m1 = client.post("/api/quantities/submit", json={
        "check_request_id": cr1["id"],
        "submitted_qty": 1.00
    }, headers=contractor_headers).json()

    appr1 = client.post("/api/approvals/re", json={
        "quantity_measurement_id": qty_m1["id"],
        "approved_qty": 1.00,
        "status": "APPROVED"
    }, headers=re_headers).json()

    assert to_decimal(appr1["approved_amount_pkr"]) == Decimal("42000.00")

    # Verify remaining is exactly 1.44 m³
    item5_after = client.get(f"/api/boq/{item5['id']}", headers=re_headers).json()
    assert to_decimal(item5_after["approved_qty"]) == Decimal("1.0000")
    assert to_decimal(item5_after["remaining_qty"]) == Decimal("1.4400")

    # Step B: Second request for 1.50 m³ (which exceeds 1.44 m³)
    cr2 = client.post("/api/check-requests", json={
        "boq_item_id": item5["id"],
        "title": "RCC Slab Pouring — Phase 2",
        "proposed_qty": 1.50
    }, headers=contractor_headers).json()

    client.post(f"/api/check-requests/{cr2['id']}/submit", headers=contractor_headers)
    insp2 = client.post(f"/api/inspections/start/{cr2['id']}", headers=re_headers).json()
    client.post(f"/api/inspections/{insp2['id']}/decide", json={"decision": "ACCEPT"}, headers=re_headers)

    qty_m2 = client.post("/api/quantities/submit", json={
        "check_request_id": cr2["id"],
        "submitted_qty": 1.50
    }, headers=contractor_headers).json()

    # Step C: RE attempts to approve 1.50 m³ -> MUST BE REJECTED!
    over_approval_res = client.post("/api/approvals/re", json={
        "quantity_measurement_id": qty_m2["id"],
        "approved_qty": 1.50,
        "status": "APPROVED"
    }, headers=re_headers)

    assert over_approval_res.status_code == 400
    err_body = over_approval_res.json()
    assert "exceeds remaining contract quantity" in err_body.get("message", "")

    # Step D: Confirm database remains uncorrupted: remaining is still 1.44 m³!
    item5_final = client.get(f"/api/boq/{item5['id']}", headers=re_headers).json()
    assert to_decimal(item5_final["approved_qty"]) == Decimal("1.0000")
    assert to_decimal(item5_final["remaining_qty"]) == Decimal("1.4400")
