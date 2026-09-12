def test_contractor_cannot_approve(client, contractor_token):
    headers = {"Authorization": f"Bearer {contractor_token}"}
    # Attempt RE approval
    res1 = client.post("/api/approvals/re", json={"quantity_measurement_id": 1, "approved_qty": 5.0}, headers=headers)
    assert res1.status_code == 403

    # Attempt Client review
    res2 = client.post("/api/client-reviews", json={"quantity_approval_id": 1, "decision": "APPROVED"}, headers=headers)
    assert res2.status_code == 403

def test_re_cannot_client_approve(client, re_token):
    headers = {"Authorization": f"Bearer {re_token}"}
    # Critical business rule: RE MUST NEVER be able to perform Client approval!
    res = client.post("/api/client-reviews", json={"quantity_approval_id": 1, "decision": "APPROVED"}, headers=headers)
    assert res.status_code == 403

def test_client_cannot_re_approve_or_act_as_contractor(client, client_token):
    headers = {"Authorization": f"Bearer {client_token}"}
    # Attempt RE approval
    res1 = client.post("/api/approvals/re", json={"quantity_measurement_id": 1, "approved_qty": 5.0}, headers=headers)
    assert res1.status_code == 403

    # Attempt Contractor CR creation
    res2 = client.post("/api/check-requests", json={"boq_item_id": 1, "title": "Unauthorized CR", "proposed_qty": 1.0}, headers=headers)
    assert res2.status_code == 403
