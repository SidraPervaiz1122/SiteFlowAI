import re
from decimal import Decimal
from typing import List, Dict, Any
from backend.schemas.ai import AiPreReviewOutput, AiObservationOutput

class DeterministicAiFallback:
    """
    Deterministic engineering rule engine ensuring 100% offline hackathon availability
    with authentic, context-aware construction engineering outputs.
    """

    @classmethod
    def generate_pre_review(
        cls,
        item_number: int,
        category: str,
        description: str,
        contract_qty: Decimal,
        proposed_qty: Decimal,
        evidence_count: int,
        evidence_names: List[str]
    ) -> AiPreReviewOutput:
        missing = []
        issues = []
        checks = []
        questions = []
        confidence = 90
        readiness = "Ready"

        cat_lower = category.lower()

        # Evidence checks
        if evidence_count == 0:
            missing.append("Site progress photographs showing current execution phase")
            missing.append("Material inspection ticket / delivery challan")
            issues.append("Zero supporting photographic or document evidence attached")
            readiness = "Needs Attention"
            confidence = 65
        elif evidence_count < 2:
            missing.append("Additional panoramic site verification photo")
            readiness = "Ready"
            confidence = 82

        # Category-specific engineering checks
        if "concrete" in cat_lower:
            checks.append("Verify slump test results (target 75mm-100mm)")
            checks.append("Verify formwork alignment, plumb, and shutter oil application")
            checks.append("Inspect reinforcement cover blocks (min 25mm)")
            questions.append("Has 7-day cube compression test been logged for previous batch?")
            if evidence_count < 2:
                missing.append("Concrete batching slip / mix proportion record")
        elif "reinforcement" in cat_lower or "steel" in cat_lower:
            checks.append("Verify rebar spacing against structural BBS (Bar Bending Schedule)")
            checks.append("Verify lap lengths (min 50d) and stagger positions")
            checks.append("Ensure binding wire is tied at every intersection")
            questions.append("Has mill test certificate been verified for Grade 60 tensile yield?")
        elif "masonry" in cat_lower or "brick" in cat_lower:
            checks.append("Verify mortar ratio (1:6 cement-sand) and joint thickness (10mm max)")
            checks.append("Check verticality/plumb of wall with plumb bob at corners")
            checks.append("Verify English bond racking back and frog positioning facing upwards")
            questions.append("Were bricks properly soaked in clean water for at least 2 hours prior to laying?")
        elif "earthwork" in cat_lower:
            checks.append("Verify foundation trench depth against architectural benchmark")
            checks.append("Check compaction layer thickness (max 150mm lifts)")
            checks.append("Verify soil bearing stratum is free of loose debris or organic matter")
            questions.append("Has field density test (FDT) been scheduled for compacted subgrade?")
        else:
            checks.append("Verify compliance with architectural layout and drawings")
            checks.append("Inspect workmanship quality and alignment")
            questions.append("Are approved submittals on file for materials used?")

        # Quantity reasonableness
        if proposed_qty > contract_qty:
            issues.append(f"Proposed quantity ({proposed_qty}) exceeds contractual total ({contract_qty})")
            readiness = "High Risk"
            confidence = 50
        elif proposed_qty > (contract_qty * Decimal("0.80")) and contract_qty > Decimal("1.0"):
            issues.append("High single-batch claim (>80% of total contract volume)")

        return AiPreReviewOutput(
            readiness=readiness,
            confidence_score=confidence,
            missing_evidence=missing,
            potential_issues=issues,
            suggested_checks=checks,
            recommended_questions=questions
        )

    @classmethod
    def generate_observation_draft(
        cls,
        item_number: int,
        category: str,
        description: str,
        hint: str = None
    ) -> AiObservationOutput:
        cat_lower = category.lower()
        hint_lower = (hint or "").lower()

        if "mortar" in hint_lower or "masonry" in cat_lower or "brick" in cat_lower:
            title = "Mortar Joint Thickness and Soaking Non-Conformance"
            desc = "Observed horizontal mortar bed joints exceeding 12mm thickness in localized masonry panels. Inadequate pre-soaking of clay bricks observed during laying."
            severity = "MEDIUM"
            category_type = "WORKMANSHIP"
            action = "Rake out fresh defective joints to 15mm depth, ensure proper water curing for 7 days, and mandate strict 10mm joint control for subsequent courses."
        elif "honeycomb" in hint_lower or "concrete" in cat_lower:
            title = "Minor Surface Honeycombing and Cover Deficiency"
            desc = "Surface segregation and minor honeycombing observed at column-beam junction due to inadequate needle vibrator compaction."
            severity = "HIGH"
            category_type = "QUALITY"
            action = "Chop out loose aggregate down to sound concrete, clean with wire brush, apply bonding agent, and pressure-pack with approved non-shrink structural repair mortar."
        elif "safety" in hint_lower or "ppe" in hint_lower:
            title = "Scaffolding Safety and Edge Protection Defect"
            desc = "Working platform lacks double guardrails and toe-boards at heights exceeding 2.0 meters. Workers observed without safety harnesses."
            severity = "CRITICAL"
            category_type = "SAFETY"
            action = "Halt all work at elevated platform immediately. Erect complete tubular scaffolding with rigid handrails and issue mandatory PPE warning."
        else:
            title = "Specification Deviation on Surface Preparation"
            desc = f"Observed minor workmanship inconsistency with approved project specifications for {description}."
            severity = "LOW"
            category_type = "SPECIFICATION"
            action = "Contractor to remediate surface preparation and re-invite Resident Engineer for verification prior to next activity."

        return AiObservationOutput(
            title=title,
            description=desc,
            severity=severity,
            category=category_type,
            recommended_action=action
        )
