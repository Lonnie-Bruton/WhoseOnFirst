"""
Settings model for application configuration.

Stores key-value pairs for runtime configuration that can be
changed without restarting the application.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from .database import Base


class Settings(Base):
    """
    Application settings model.

    Stores configuration values as key-value pairs with optional
    metadata for description and type information.

    Attributes:
        id: Primary key
        key: Unique setting key (e.g., 'auto_renew_enabled')
        value: Setting value (stored as string, cast as needed)
        value_type: Type hint for parsing (bool, int, str, etc.)
        description: Human-readable description of setting
        updated_at: Last modification timestamp
    """

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(String(500), nullable=False)
    value_type = Column(String(20), default="str")  # bool, int, str, float
    description = Column(String(500))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def get_typed_value(self):
        """
        Get the value cast to its proper type.

        Returns:
            Value cast to the type specified in value_type
        """
        if self.value_type == "bool":
            return self.value.lower() in ("true", "1", "yes", "on")
        elif self.value_type == "int":
            return int(self.value)
        elif self.value_type == "float":
            return float(self.value)
        else:
            return self.value

    def __repr__(self):
        return f"<Settings(key={self.key}, value={self.value}, type={self.value_type})>"
