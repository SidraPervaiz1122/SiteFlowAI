class SiteFlowException(Exception):
    """Base exception for SiteFlow domain errors."""
    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

class UnauthorizedException(SiteFlowException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)

class ForbiddenException(SiteFlowException):
    def __init__(self, message: str = "Forbidden for this role"):
        super().__init__(message, status_code=403)

class NotFoundException(SiteFlowException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class WorkflowTransitionError(SiteFlowException):
    def __init__(self, current_state: str, attempted_action: str, reason: str = ""):
        message = f"Invalid workflow transition from '{current_state}' via '{attempted_action}'. {reason}".strip()
        super().__init__(message, status_code=422, details={"current_state": current_state, "attempted_action": attempted_action, "reason": reason})

class QuantityOverApprovalError(SiteFlowException):
    def __init__(self, submitted_qty, remaining_qty, boq_item_id=None):
        message = (
            f"Quantity over-approval rejected: Requested approval of {submitted_qty} "
            f"exceeds remaining contract quantity of {remaining_qty}."
        )
        super().__init__(message, status_code=400, details={
            "submitted_qty": str(submitted_qty),
            "remaining_qty": str(remaining_qty),
            "boq_item_id": boq_item_id
        })

class ContractImmutabilityError(SiteFlowException):
    def __init__(self, message: str = "Contractual BOQ items are strictly immutable in the MVP"):
        super().__init__(message, status_code=403)

class IntegrityValidationError(SiteFlowException):
    def __init__(self, message: str = "Contractual integrity validation failed"):
        super().__init__(message, status_code=500)
