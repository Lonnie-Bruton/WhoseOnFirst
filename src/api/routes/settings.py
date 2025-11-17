"""
Settings API Routes

FastAPI router for application settings management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import re

from src.api.dependencies import get_db
from src.api.schemas.settings import (
    AutoRenewConfigResponse,
    AutoRenewConfigRequest,
    SMSTemplateResponse,
    SMSTemplateRequest,
    EscalationConfigResponse,
    EscalationConfigRequest
)
from src.services import SettingsService
from src.api.routes.auth import require_auth, require_admin


router = APIRouter()


@router.get("/auto-renew", response_model=AutoRenewConfigResponse)
def get_auto_renew_config(
    db: Session = Depends(get_db),
    current_user = Depends(require_auth)
):
    """
    Get auto-renewal configuration.

    Returns current settings for automatic schedule renewal.

    Args:
        db: Database session (injected)

    Returns:
        Auto-renewal configuration

    Example:
        GET /api/v1/settings/auto-renew
    """
    service = SettingsService(db)
    config = service.get_auto_renew_config()
    return config


@router.put("/auto-renew", response_model=AutoRenewConfigResponse)
def update_auto_renew_config(
    request: AutoRenewConfigRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """
    Update auto-renewal configuration.

    Updates settings for automatic schedule renewal.
    Only administrators can update these settings.

    Args:
        request: Auto-renewal configuration update
        db: Database session (injected)

    Returns:
        Updated auto-renewal configuration

    Example:
        PUT /api/v1/settings/auto-renew
        {
            "enabled": true,
            "threshold_weeks": 4,
            "renew_weeks": 52
        }
    """
    service = SettingsService(db)

    # Build update dict from request (only include non-None values)
    update_dict = {}
    if request.enabled is not None:
        update_dict["enabled"] = request.enabled
    if request.threshold_weeks is not None:
        update_dict["threshold_weeks"] = request.threshold_weeks
    if request.renew_weeks is not None:
        update_dict["renew_weeks"] = request.renew_weeks

    # Update settings
    service.update_auto_renew_config(update_dict)

    # Return updated config
    config = service.get_auto_renew_config()
    return config


@router.get("/sms-template", response_model=SMSTemplateResponse)
def get_sms_template(
    db: Session = Depends(get_db),
    current_user = Depends(require_auth)
):
    """
    Get the SMS notification template.

    Returns the current SMS template used for on-call notifications.
    Template includes variables: {name}, {start_time}, {end_time}, {duration}

    Args:
        db: Database session (injected)
        current_user: Authenticated user (injected)

    Returns:
        SMS template with metadata

    Example:
        GET /api/v1/settings/sms-template
    """
    service = SettingsService(db)
    template = service.get_sms_template()

    # Extract variables from template
    variables = re.findall(r'\{(\w+)\}', template)

    # Get last updated timestamp
    setting = service.get_setting("sms_template")
    last_updated = setting.updated_at if setting else None

    # Calculate character count and SMS segments
    char_count = len(template)
    sms_count = max(1, (char_count + 159) // 160)  # Ceiling division

    return SMSTemplateResponse(
        template=template,
        last_updated=last_updated,
        character_count=char_count,
        sms_count=sms_count,
        variables=variables
    )


@router.put("/sms-template", response_model=SMSTemplateResponse)
def update_sms_template(
    request: SMSTemplateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """
    Update the SMS notification template.

    Updates the template used for on-call notifications.
    Only administrators can update the template.

    **Template Variables:**
    - {name}: Team member name
    - {start_time}: Shift start time (e.g., "Mon 08:00 AM")
    - {end_time}: Shift end time (e.g., "Tue 08:00 AM")
    - {duration}: Shift duration (e.g., "24h")

    **Validation Rules:**
    - Must contain at least one variable
    - Maximum 320 characters (2 SMS segments)
    - Cannot be empty or whitespace only

    Args:
        request: SMS template update request
        db: Database session (injected)
        current_user: Authenticated admin user (injected)

    Returns:
        Updated SMS template with metadata

    Raises:
        HTTPException 400: If template is invalid

    Example:
        PUT /api/v1/settings/sms-template
        {
            "template": "Hi {name}, you're on-call from {start_time} to {end_time}."
        }
    """
    template = request.template.strip()

    # Validation 1: Check for empty template
    if not template:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SMS template cannot be empty"
        )

    # Validation 2: Check for at least one variable
    variables = re.findall(r'\{(\w+)\}', template)
    if not variables:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Template must contain at least one variable: {name}, {start_time}, {end_time}, or {duration}"
        )

    # Validation 3: Check for valid variables only
    valid_variables = {"name", "start_time", "end_time", "duration"}
    invalid_variables = set(variables) - valid_variables
    if invalid_variables:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid template variables: {', '.join(invalid_variables)}. Valid variables: {', '.join(valid_variables)}"
        )

    # Validation 4: Check character limit (320 = 2 SMS segments)
    if len(template) > 320:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Template too long: {len(template)} characters (max 320)"
        )

    # Save template
    service = SettingsService(db)
    try:
        service.set_sms_template(template)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    # Return updated template with metadata
    setting = service.get_setting("sms_template")
    char_count = len(template)
    sms_count = max(1, (char_count + 159) // 160)

    return SMSTemplateResponse(
        template=template,
        last_updated=setting.updated_at if setting else None,
        character_count=char_count,
        sms_count=sms_count,
        variables=variables
    )


@router.get("/escalation", response_model=EscalationConfigResponse)
def get_escalation_config(
    db: Session = Depends(get_db),
    current_user = Depends(require_auth)
):
    """
    Get escalation contact configuration.

    Returns the current escalation contact settings for dashboard display.
    Escalation contacts are fixed (non-rotating) and displayed on the dashboard
    alongside rotating Primary/Backup on-call assignments.

    Args:
        db: Database session (injected)
        current_user: Authenticated user (injected)

    Returns:
        Escalation contact configuration

    Example:
        GET /api/v1/settings/escalation
    """
    service = SettingsService(db)
    config = service.get_escalation_config()
    return config


@router.put("/escalation", response_model=EscalationConfigResponse)
def update_escalation_config(
    request: EscalationConfigRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """
    Update escalation contact configuration.

    Updates the fixed escalation contacts displayed on the dashboard.
    Only administrators can update these settings.

    **Escalation Contacts:**
    - Primary Escalation (1st): First level of escalation
    - Secondary Escalation (2nd): Second level of escalation

    **Phone Format:**
    - Must be E.164 format: +1XXXXXXXXXX
    - Example: +19187019714

    **Note:** Escalation contacts are display-only and do NOT receive
    automated notifications. They are not part of the rotation schedule.

    Args:
        request: Escalation configuration update
        db: Database session (injected)
        current_user: Authenticated admin user (injected)

    Returns:
        Updated escalation configuration

    Raises:
        HTTPException 400: If phone format is invalid

    Example:
        PUT /api/v1/settings/escalation
        {
            "enabled": true,
            "primary_name": "Ken U",
            "primary_phone": "+19187019714",
            "secondary_name": "Steve N",
            "secondary_phone": "+19185551234"
        }
    """
    service = SettingsService(db)

    # Update escalation configuration
    # Pydantic schema already validates phone format (E.164)
    try:
        service.set_escalation_config(
            enabled=request.enabled,
            primary_name=request.primary_name,
            primary_phone=request.primary_phone,
            secondary_name=request.secondary_name,
            secondary_phone=request.secondary_phone
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    # Return updated config
    config = service.get_escalation_config()
    return config
