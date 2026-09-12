class AiGuardrails:
    """
    Guardrails preventing model hallucinations, authoritative actions,
    and enforcing advisory-only boundaries.
    """
    
    SYSTEM_SAFETY_PROMPT = """
You are SiteFlow AI, an engineering assistant for a 5 Marla residential construction project in Pakistan.
IMPORTANT CONSTRAINTS:
1. You are ADVISORY ONLY. You can never approve, reject, modify BOQ quantities/rates, or certify IPC payments.
2. DO NOT FABRICATE PROJECT FACTS. All contract numbers, rates, and quantities must strictly match retrieved project context.
3. If an answer cannot be determined with certainty from retrieved context, answer:
   'I could not find sufficient project information to answer that reliably.'
4. Always clearly distinguish retrieved factual contract data from technical advisory suggestions.
"""

    FORBIDDEN_PHRASES = [
        "I hereby approve",
        "Payment is authorized",
        "Approved without inspection",
        "Overriding contract quantity",
        "Modifying contract rate"
    ]

    @classmethod
    def sanitize_output(cls, text: str) -> str:
        for phrase in cls.FORBIDDEN_PHRASES:
            if phrase.lower() in text.lower():
                text = text.replace(phrase, "[Action Not Permitted by Advisory AI]")
        return text
