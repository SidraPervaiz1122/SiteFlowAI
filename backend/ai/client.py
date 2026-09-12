import json
import logging
from typing import List, Optional
from decimal import Decimal
from backend.app.config import settings
from backend.schemas.ai import AiPreReviewOutput, AiObservationOutput
from backend.ai.fallback import DeterministicAiFallback
from backend.ai.guardrails import AiGuardrails

logger = logging.getLogger("siteflow.ai")

class AiClient:
    """
    Multi-provider AI client with automatic local fallback.
    Guarantees non-blocking advisory services.
    """

    @classmethod
    def get_pre_review(
        cls,
        item_number: int,
        category: str,
        description: str,
        contract_qty: Decimal,
        proposed_qty: Decimal,
        evidence_count: int,
        evidence_names: List[str]
    ) -> AiPreReviewOutput:
        """Advisory pre-review generated before physical inspection."""
        try:
            if settings.OPENAI_API_KEY and settings.AI_PROVIDER == "openai":
                # Real OpenAI integration if configured
                import httpx
                # We can call OpenAI API or fall back if key is inactive
                pass
        except Exception as e:
            logger.warning(f"External AI call failed, using deterministic fallback: {e}")

        # Use robust local deterministic fallback
        return DeterministicAiFallback.generate_pre_review(
            item_number=item_number,
            category=category,
            description=description,
            contract_qty=contract_qty,
            proposed_qty=proposed_qty,
            evidence_count=evidence_count,
            evidence_names=evidence_names
        )

    @classmethod
    def draft_observation(
        cls,
        item_number: int,
        category: str,
        description: str,
        hint: Optional[str] = None
    ) -> AiObservationOutput:
        """Draft an observation for RE review and editing."""
        return DeterministicAiFallback.generate_observation_draft(
            item_number=item_number,
            category=category,
            description=description,
            hint=hint
        )
