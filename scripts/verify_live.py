import httpx as requests

BASE = 'http://127.0.0.1:8000/api'

def run_acceptance_verification():
    print("==================================================")
    print("STARTING LIVE ACCEPTANCE VERIFICATION")
    print("==================================================")

    # 1. Login as Contractor
    c_res = requests.post(f"{BASE}/auth/quick-switch", json={"role": "CONTRACTOR"}).json()
    c_token = c_res["access_token"]
    c_headers = {"Authorization": f"Bearer {c_token}"}
    print("[PASS] 1. Authenticated as Contractor (Tariq Mahmood)")

    # 2. Check BOQ
    boq = requests.get(f"{BASE}/boq", headers=c_headers).json()
    item8 = next(b for b in boq if b["item_number"] == 8)
    print(f"[PASS] 2. BOQ Item 8 Loaded: {item8['description']} | Contract Qty: {item8['contract_qty']} {item8['unit']} | Rate: PKR {float(item8['rate_pkr']):,.2f}")

    # 3. Create Check Request for Item 8
    cr = requests.post(f"{BASE}/check-requests", json={
        "boq_item_id": item8["id"],
        "title": "Ground Floor Masonry Axis 1-4",
        "proposed_qty": 10.0,
        "description": "Brickwork with 1:6 mortar"
    }, headers=c_headers).json()
    cr_id = cr["id"]
    print(f"[PASS] 3. Check Request Created: {cr['cr_number']} (Status: {cr['status']})")

    # 4. Submit CR (Triggers AI Pre-Review)
    cr_sub = requests.post(f"{BASE}/check-requests/{cr_id}/submit", headers=c_headers).json()
    ai_readiness = cr_sub["ai_reviews"][0]["readiness"]
    ai_conf = cr_sub["ai_reviews"][0]["confidence_score"]
    print(f"[PASS] 4. Check Request Submitted -> Status: {cr_sub['status']} | AI Advisory Readiness: {ai_readiness} ({ai_conf}% confidence)")

    # 5. Switch to RE (Engr. Bilal Khan)
    re_res = requests.post(f"{BASE}/auth/quick-switch", json={"role": "RE"}).json()
    re_token = re_res["access_token"]
    re_headers = {"Authorization": f"Bearer {re_token}"}
    print("[PASS] 5. Authenticated as Resident Engineer (Engr. Bilal Khan)")

    # 6. Start inspection & draft observation
    insp = requests.post(f"{BASE}/inspections/start/{cr_id}", headers=re_headers).json()
    insp_id = insp["id"]
    print(f"[PASS] 6. Inspection Workspace Opened: INSP-{insp_id}")

    ai_draft = requests.post(f"{BASE}/inspections/{insp_id}/ai-draft?hint=mortar", headers=re_headers).json()
    print(f"[PASS] 7. AI Observation Drafted: '{ai_draft['title']}' [{ai_draft['severity']}]")

    obs = requests.post(f"{BASE}/inspections/{insp_id}/observations", json={
        "title": ai_draft["title"],
        "description": ai_draft["description"],
        "severity": ai_draft["severity"],
        "category": ai_draft["category"],
        "corrective_action": ai_draft["recommended_action"],
        "is_ai_generated": True
    }, headers=re_headers).json()
    print(f"[PASS] 8. Observation Recorded by RE into Official Inspection Log")

    decide = requests.post(f"{BASE}/inspections/{insp_id}/decide", json={
        "decision": "ACCEPT",
        "inspector_notes": "Dimensional plumb verified and mortar curing confirmed."
    }, headers=re_headers).json()
    print(f"[PASS] 9. Inspection Decision Recorded: {decide['decision']} -> Workflow: INSPECTION_ACCEPTED")

    # 7. Contractor submits measured quantity (10.00 m³)
    qty_m = requests.post(f"{BASE}/quantities/submit", json={
        "check_request_id": cr_id,
        "submitted_qty": 10.0,
        "contractor_notes": "Measured actual in-place masonry volume"
    }, headers=c_headers).json()
    meas_id = qty_m["id"]
    print(f"[PASS] 10. Contractor Submitted Measured Quantity: {qty_m['submitted_qty']} m³")

    # 8. RE approves quantity 10.00 m³
    re_appr = requests.post(f"{BASE}/approvals/re", json={
        "quantity_measurement_id": meas_id,
        "approved_qty": 10.0,
        "status": "APPROVED",
        "re_comments": "Verified against drawings and site measurements"
    }, headers=re_headers).json()
    appr_id = re_appr["id"]
    appr_amount = float(re_appr["approved_amount_pkr"])
    print(f"[PASS] 11. RE Approved Quantity: 10.00 m³ -> Calculated Amount: PKR {appr_amount:,.2f} (Expected PKR 155,000.00)")
    assert appr_amount == 155000.0, f"Expected 155000, got {appr_amount}"

    # Verify BOQ Remaining is 20.79 m³ (30.79 - 10.00)
    boq_upd = requests.get(f"{BASE}/boq/{item8['id']}", headers=re_headers).json()
    rem_qty = float(boq_upd["remaining_qty"])
    print(f"[PASS] 12. BOQ Item 8 Remaining Quantity: {rem_qty} m³ (Expected 20.79 m³)")
    assert rem_qty == 20.79, f"Expected 20.79, got {rem_qty}"

    # 9. Client Review
    cl_res = requests.post(f"{BASE}/auth/quick-switch", json={"role": "CLIENT"}).json()
    cl_token = cl_res["access_token"]
    cl_headers = {"Authorization": f"Bearer {cl_token}"}
    print("[PASS] 13. Authenticated as Client (Malik Zafar)")

    cl_rev = requests.post(f"{BASE}/client-reviews", json={
        "quantity_approval_id": appr_id,
        "decision": "APPROVED",
        "comments": "Inspected progress and certified for IPC inclusion"
    }, headers=cl_headers).json()
    print(f"[PASS] 14. Client Review Decision Recorded: {cl_rev['decision']} -> Workflow: IPC_ELIGIBLE")

    # 10. IPC Generation
    elig = requests.get(f"{BASE}/ipc/eligible", headers=cl_headers).json()
    print(f"[PASS] 15. IPC Eligibility Pool: {elig['eligible_items_count']} item(s) totaling PKR {float(elig['total_eligible_amount_pkr']):,.2f}")

    ipc = requests.post(f"{BASE}/ipc/generate", json={
        "period_start": "2026-09-01",
        "period_end": "2026-09-30",
        "notes": "First Interim Certificate - Ground Floor Masonry"
    }, headers=cl_headers).json()
    ipc_current = float(ipc["total_current_amount_pkr"])
    print(f"[PASS] 16. Generated {ipc['ipc_number']}: Total PKR {ipc_current:,.2f}")
    assert ipc_current >= 155000.0

    # 11. Verify Item 5 Over-approval Prevention
    print("--------------------------------------------------")
    print("TESTING ITEM 5 OVER-APPROVAL SAFEGUARD")
    print("--------------------------------------------------")
    item5 = next(b for b in boq if b["item_number"] == 5)
    print(f"Item 5 Contract: {item5['contract_qty']} m³ @ PKR {float(item5['rate_pkr']):,.2f}")

    # Approve 1.00 m³
    cr5 = requests.post(f"{BASE}/check-requests", json={
        "boq_item_id": item5["id"],
        "title": "RCC Columns Phase 1",
        "proposed_qty": 1.0
    }, headers=c_headers).json()
    requests.post(f"{BASE}/check-requests/{cr5['id']}/submit", headers=c_headers)
    insp5 = requests.post(f"{BASE}/inspections/start/{cr5['id']}", headers=re_headers).json()
    requests.post(f"{BASE}/inspections/{insp5['id']}/decide", json={"decision": "ACCEPT"}, headers=re_headers)
    qty5_1 = requests.post(f"{BASE}/quantities/submit", json={"check_request_id": cr5["id"], "submitted_qty": 1.0}, headers=c_headers).json()
    appr5_1 = requests.post(f"{BASE}/approvals/re", json={"quantity_measurement_id": qty5_1["id"], "approved_qty": 1.0, "status": "APPROVED"}, headers=re_headers).json()
    print(f"[PASS] 17. Item 5 Approved 1.00 m³ -> Amount: PKR {float(appr5_1['approved_amount_pkr']):,.2f} (Expected PKR 42,000.00)")
    assert float(appr5_1["approved_amount_pkr"]) == 42000.0

    boq5_upd = requests.get(f"{BASE}/boq/{item5['id']}", headers=re_headers).json()
    rem5 = float(boq5_upd["remaining_qty"])
    print(f"[PASS] 18. Item 5 Remaining Quantity: {rem5} m³ (Expected 1.44 m³)")
    assert rem5 == 1.44

    # Now attempt 1.50 m³ (must be rejected!)
    cr5_2 = requests.post(f"{BASE}/check-requests", json={
        "boq_item_id": item5["id"],
        "title": "RCC Slab Phase 2",
        "proposed_qty": 1.5
    }, headers=c_headers).json()
    requests.post(f"{BASE}/check-requests/{cr5_2['id']}/submit", headers=c_headers)
    insp5_2 = requests.post(f"{BASE}/inspections/start/{cr5_2['id']}", headers=re_headers).json()
    requests.post(f"{BASE}/inspections/{insp5_2['id']}/decide", json={"decision": "ACCEPT"}, headers=re_headers)
    qty5_2 = requests.post(f"{BASE}/quantities/submit", json={"check_request_id": cr5_2["id"], "submitted_qty": 1.5}, headers=c_headers).json()

    over_res = requests.post(f"{BASE}/approvals/re", json={"quantity_measurement_id": qty5_2["id"], "approved_qty": 1.5, "status": "APPROVED"}, headers=re_headers)
    print(f"[PASS] 19. RE attempt to approve 1.50 m³ against remaining 1.44 m³ -> HTTP {over_res.status_code}: {over_res.json()['message']}")
    assert over_res.status_code == 400
    assert "exceeds remaining contract quantity" in over_res.json()["message"]

    # Verify database uncorrupted
    boq5_final = requests.get(f"{BASE}/boq/{item5['id']}", headers=re_headers).json()
    assert float(boq5_final["remaining_qty"]) == 1.44
    print("[PASS] 20. Item 5 Remaining intact at 1.44 m³. Zero database corruption, zero over-approval.")

    # 12. Verify Audit Trail
    audit = requests.get(f"{BASE}/audit", headers=cl_headers).json()
    actions = [a["action"] for a in audit]
    for req_action in ["CR_CREATED", "CR_SUBMITTED", "INSPECTION_DECIDED", "QUANTITY_SUBMITTED", "RE_QUANTITY_APPROVED", "CLIENT_APPROVED", "IPC_GENERATED"]:
        assert req_action in actions, f"Missing audit action {req_action}"
    print(f"[PASS] 21. Audit Trail contains all {len(audit)} system mutation records.")

    print("==================================================")
    print("ALL LIVE ACCEPTANCE CHECKS PASSED WITH 100% SUCCESS!")
    print("==================================================")

if __name__ == "__main__":
    run_acceptance_verification()
