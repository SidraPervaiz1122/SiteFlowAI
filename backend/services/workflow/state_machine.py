from typing import Optional, List
from backend.core.enums import WorkflowState, UserRole
from backend.core.exceptions import WorkflowTransitionError, ForbiddenException

class WorkflowStateMachine:
    """
    Centralized state machine enforcing valid workflow transitions,
    actor roles, and required conditions across the construction lifecycle.
    """

    # Allowed transitions mapping: Current State -> Set of Allowed Next States
    VALID_TRANSITIONS = {
        WorkflowState.DRAFT: {WorkflowState.SUBMITTED},
        WorkflowState.SUBMITTED: {WorkflowState.AI_PRE_REVIEW, WorkflowState.PENDING_INSPECTION},
        WorkflowState.AI_PRE_REVIEW: {WorkflowState.PENDING_INSPECTION},
        WorkflowState.PENDING_INSPECTION: {WorkflowState.INSPECTION_IN_PROGRESS},
        WorkflowState.INSPECTION_IN_PROGRESS: {WorkflowState.INSPECTION_ACCEPTED, WorkflowState.INSPECTION_REJECTED},
        WorkflowState.INSPECTION_REJECTED: {WorkflowState.DRAFT, WorkflowState.SUBMITTED}, # Resubmit after fixing
        WorkflowState.INSPECTION_ACCEPTED: {WorkflowState.QUANTITY_SUBMITTED},
        WorkflowState.QUANTITY_SUBMITTED: {WorkflowState.RE_APPROVED, WorkflowState.RE_REJECTED},
        WorkflowState.RE_REJECTED: {WorkflowState.QUANTITY_SUBMITTED}, # Resubmit corrected quantity
        WorkflowState.RE_APPROVED: {WorkflowState.CLIENT_REVIEW},
        WorkflowState.CLIENT_REVIEW: {WorkflowState.CLIENT_APPROVED, WorkflowState.CLIENT_REJECTED},
        WorkflowState.CLIENT_REJECTED: {WorkflowState.QUANTITY_SUBMITTED, WorkflowState.RE_APPROVED},
        WorkflowState.CLIENT_APPROVED: {WorkflowState.IPC_ELIGIBLE},
        WorkflowState.IPC_ELIGIBLE: {WorkflowState.IPC_INCLUDED},
        WorkflowState.IPC_INCLUDED: set() # Terminal for this particular measurement cycle
    }

    # Role constraints for initiating each target state
    ROLE_REQUIREMENTS = {
        WorkflowState.SUBMITTED: [UserRole.CONTRACTOR],
        WorkflowState.AI_PRE_REVIEW: [UserRole.CONTRACTOR, UserRole.RE], # Can be auto or RE triggered
        WorkflowState.PENDING_INSPECTION: [UserRole.CONTRACTOR, UserRole.RE],
        WorkflowState.INSPECTION_IN_PROGRESS: [UserRole.RE],
        WorkflowState.INSPECTION_ACCEPTED: [UserRole.RE],
        WorkflowState.INSPECTION_REJECTED: [UserRole.RE],
        WorkflowState.QUANTITY_SUBMITTED: [UserRole.CONTRACTOR],
        WorkflowState.RE_APPROVED: [UserRole.RE],
        WorkflowState.RE_REJECTED: [UserRole.RE],
        WorkflowState.CLIENT_REVIEW: [UserRole.RE, UserRole.CLIENT],
        WorkflowState.CLIENT_APPROVED: [UserRole.CLIENT], # STRICT: RE can NEVER approve client review!
        WorkflowState.CLIENT_REJECTED: [UserRole.CLIENT], # STRICT: RE can NEVER reject client review!
        WorkflowState.IPC_ELIGIBLE: [UserRole.CLIENT, UserRole.RE],
        WorkflowState.IPC_INCLUDED: [UserRole.CLIENT, UserRole.RE]
    }

    @classmethod
    def validate_transition(
        cls,
        current_state: str,
        target_state: str,
        actor_role: str,
        context: Optional[dict] = None
    ) -> bool:
        """
        Validate whether the given actor role can transition from current_state to target_state.
        Throws WorkflowTransitionError or ForbiddenException if invalid.
        """
        try:
            curr = WorkflowState(current_state)
            target = WorkflowState(target_state)
        except ValueError as e:
            raise WorkflowTransitionError(current_state, target_state, f"Unknown workflow state: {e}")

        # Check state transition graph
        if target not in cls.VALID_TRANSITIONS.get(curr, set()):
            raise WorkflowTransitionError(
                curr.value,
                target.value,
                f"Transition from '{curr.value}' to '{target.value}' is not allowed in the workflow graph."
            )

        # Check role permission
        allowed_roles = cls.ROLE_REQUIREMENTS.get(target, [])
        if allowed_roles and actor_role not in [r.value for r in allowed_roles]:
            allowed_role_names = [r.value for r in allowed_roles]
            raise ForbiddenException(
                f"Role '{actor_role}' is not authorized to transition state to '{target.value}'. "
                f"Required role: {allowed_role_names}"
            )

        # Critical Business Rule: RE must NEVER perform client approval
        if target == WorkflowState.CLIENT_APPROVED and actor_role == UserRole.RE.value:
            raise ForbiddenException("CRITICAL VIOLATION: Resident Engineer (RE) is strictly forbidden from performing Client Approval.")

        # Critical Business Rule: Contractor cannot perform any approvals
        if target in [WorkflowState.INSPECTION_ACCEPTED, WorkflowState.RE_APPROVED, WorkflowState.CLIENT_APPROVED] and actor_role == UserRole.CONTRACTOR.value:
            raise ForbiddenException("Contractor cannot perform approvals on their own work.")

        return True

    @classmethod
    def can_transition(cls, current_state: str, target_state: str, actor_role: str) -> bool:
        try:
            cls.validate_transition(current_state, target_state, actor_role)
            return True
        except Exception:
            return False
