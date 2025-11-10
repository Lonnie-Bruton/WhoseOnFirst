"""
Settings API Routes

FastAPI router for application settings management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.api.schemas.settings import (
    AutoRenewConfigResponse,
    AutoRenewConfigRequest
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
