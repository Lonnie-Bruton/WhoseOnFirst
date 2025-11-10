"""
Settings service for business logic.

Manages application settings with type-safe accessors.
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from ..repositories.settings_repository import SettingsRepository
from ..models.settings import Settings


# Setting key constants
AUTO_RENEW_ENABLED = "auto_renew_enabled"
AUTO_RENEW_THRESHOLD_WEEKS = "auto_renew_threshold_weeks"
AUTO_RENEW_WEEKS = "auto_renew_weeks"


class SettingsService:
    """
    Service for managing application settings.

    Provides business logic for settings management with
    type-safe accessors and defaults.

    Attributes:
        db: Database session
        repository: Settings repository instance
    """

    def __init__(self, db: Session):
        """
        Initialize SettingsService.

        Args:
            db: Database session
        """
        self.db = db
        self.repository = SettingsRepository(db)

    def get_setting(self, key: str) -> Optional[Settings]:
        """
        Get a setting by key.

        Args:
            key: Setting key

        Returns:
            Settings instance or None
        """
        return self.repository.get_by_key(key)

    def get_all_settings(self) -> Dict[str, Any]:
        """
        Get all settings as a dictionary.

        Returns:
            Dictionary of all settings with typed values
        """
        all_settings = self.repository.get_all()
        return {
            setting.key: setting.get_typed_value()
            for setting in all_settings
        }

    def set_setting(self, key: str, value: Any, value_type: str = None, description: str = None) -> Settings:
        """
        Set a setting value.

        Args:
            key: Setting key
            value: Setting value (will be converted to string)
            value_type: Optional type override (auto-detected if None)
            description: Optional description

        Returns:
            Settings instance
        """
        # Auto-detect type if not provided
        if value_type is None:
            if isinstance(value, bool):
                value_type = "bool"
            elif isinstance(value, int):
                value_type = "int"
            elif isinstance(value, float):
                value_type = "float"
            else:
                value_type = "str"

        # Convert value to string for storage
        str_value = str(value).lower() if isinstance(value, bool) else str(value)

        return self.repository.set_value(key, str_value, value_type, description)

    def delete_setting(self, key: str) -> bool:
        """
        Delete a setting.

        Args:
            key: Setting key

        Returns:
            True if deleted, False if not found
        """
        return self.repository.delete_by_key(key)

    # Auto-renewal specific methods
    def is_auto_renew_enabled(self) -> bool:
        """
        Check if auto-renewal is enabled.

        Returns:
            True if enabled, False otherwise (default: True)
        """
        return self.repository.get_value(AUTO_RENEW_ENABLED, default=True)

    def set_auto_renew_enabled(self, enabled: bool) -> Settings:
        """
        Enable or disable auto-renewal.

        Args:
            enabled: True to enable, False to disable

        Returns:
            Settings instance
        """
        return self.set_setting(
            AUTO_RENEW_ENABLED,
            enabled,
            "bool",
            "Automatically renew schedule when running low"
        )

    def get_auto_renew_threshold_weeks(self) -> int:
        """
        Get the threshold in weeks to trigger auto-renewal.

        Returns:
            Number of weeks (default: 4)
        """
        return self.repository.get_value(AUTO_RENEW_THRESHOLD_WEEKS, default=4)

    def set_auto_renew_threshold_weeks(self, weeks: int) -> Settings:
        """
        Set the auto-renewal threshold.

        Args:
            weeks: Number of weeks

        Returns:
            Settings instance
        """
        return self.set_setting(
            AUTO_RENEW_THRESHOLD_WEEKS,
            weeks,
            "int",
            "Trigger auto-renewal when less than this many weeks remain"
        )

    def get_auto_renew_weeks(self) -> int:
        """
        Get the number of weeks to generate during auto-renewal.

        Returns:
            Number of weeks (default: 52)
        """
        return self.repository.get_value(AUTO_RENEW_WEEKS, default=52)

    def set_auto_renew_weeks(self, weeks: int) -> Settings:
        """
        Set the number of weeks to generate during auto-renewal.

        Args:
            weeks: Number of weeks

        Returns:
            Settings instance
        """
        return self.set_setting(
            AUTO_RENEW_WEEKS,
            weeks,
            "int",
            "Number of weeks to generate during auto-renewal"
        )

    def get_auto_renew_config(self) -> Dict[str, Any]:
        """
        Get all auto-renewal configuration.

        Returns:
            Dictionary with auto-renewal settings
        """
        return {
            "enabled": self.is_auto_renew_enabled(),
            "threshold_weeks": self.get_auto_renew_threshold_weeks(),
            "renew_weeks": self.get_auto_renew_weeks()
        }

    def update_auto_renew_config(self, config: Dict[str, Any]) -> Dict[str, Settings]:
        """
        Update auto-renewal configuration.

        Args:
            config: Dictionary with enabled, threshold_weeks, and/or renew_weeks

        Returns:
            Dictionary of updated Settings instances
        """
        updated = {}

        if "enabled" in config:
            updated["enabled"] = self.set_auto_renew_enabled(config["enabled"])

        if "threshold_weeks" in config:
            updated["threshold_weeks"] = self.set_auto_renew_threshold_weeks(config["threshold_weeks"])

        if "renew_weeks" in config:
            updated["renew_weeks"] = self.set_auto_renew_weeks(config["renew_weeks"])

        return updated
