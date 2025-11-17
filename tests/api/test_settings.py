"""
Tests for settings API endpoints.

Tests cover auto-renewal configuration and SMS template management.
"""

import pytest
from fastapi.testclient import TestClient


class TestAutoRenewEndpoints:
    """Tests for auto-renewal configuration endpoints."""

    def test_get_auto_renew_config(self, client: TestClient):
        """Test retrieving auto-renewal configuration."""
        response = client.get("/api/v1/settings/auto-renew")

        assert response.status_code == 200
        data = response.json()
        assert "enabled" in data
        assert "threshold_weeks" in data
        assert "renew_weeks" in data
        assert isinstance(data["enabled"], bool)
        assert isinstance(data["threshold_weeks"], int)
        assert isinstance(data["renew_weeks"], int)

    def test_update_auto_renew_config(self, client: TestClient):
        """Test updating auto-renewal configuration."""
        update_data = {
            "enabled": False,
            "threshold_weeks": 6,
            "renew_weeks": 26
        }

        response = client.put("/api/v1/settings/auto-renew", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["enabled"] is False
        assert data["threshold_weeks"] == 6
        assert data["renew_weeks"] == 26

    def test_update_auto_renew_partial(self, client: TestClient):
        """Test partial update of auto-renewal configuration."""
        # Only update enabled flag
        update_data = {"enabled": True}

        response = client.put("/api/v1/settings/auto-renew", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["enabled"] is True


class TestSMSTemplateEndpoints:
    """Tests for SMS template management endpoints."""

    def test_get_sms_template_default(self, client: TestClient):
        """Test retrieving default SMS template on first access."""
        response = client.get("/api/v1/settings/sms-template")

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "template" in data
        assert "last_updated" in data
        assert "character_count" in data
        assert "sms_count" in data
        assert "variables" in data

        # Verify template content
        template = data["template"]
        assert len(template) > 0
        assert "{name}" in template
        assert "{start_time}" in template
        assert "{end_time}" in template
        assert "{duration}" in template

        # Verify metadata
        assert data["character_count"] == len(template)
        assert data["sms_count"] >= 1
        assert isinstance(data["variables"], list)
        assert "name" in data["variables"]
        assert "start_time" in data["variables"]
        assert "end_time" in data["variables"]
        assert "duration" in data["variables"]

    def test_update_sms_template_valid(self, client: TestClient):
        """Test updating SMS template with valid content."""
        new_template = "Hi {name}, on-call from {start_time} to {end_time} ({duration})."

        response = client.put("/api/v1/settings/sms-template", json={
            "template": new_template
        })

        assert response.status_code == 200
        data = response.json()
        assert data["template"] == new_template
        assert data["character_count"] == len(new_template)
        assert data["sms_count"] == 1  # Should fit in 1 SMS
        assert sorted(data["variables"]) == ["duration", "end_time", "name", "start_time"]

    def test_update_sms_template_empty(self, client: TestClient):
        """Test that empty template is rejected."""
        response = client.put("/api/v1/settings/sms-template", json={
            "template": ""
        })

        # Pydantic validation catches this before endpoint logic (422 vs 400)
        assert response.status_code == 422
        detail = response.json()["detail"]
        assert isinstance(detail, list) or "String should have at least 1 character" in str(detail)

    def test_update_sms_template_whitespace_only(self, client: TestClient):
        """Test that whitespace-only template is rejected."""
        response = client.put("/api/v1/settings/sms-template", json={
            "template": "   \n   "
        })

        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]

    def test_update_sms_template_no_variables(self, client: TestClient):
        """Test that template without variables is rejected."""
        response = client.put("/api/v1/settings/sms-template", json={
            "template": "This is a static message with no variables."
        })

        assert response.status_code == 400
        assert "must contain at least one variable" in response.json()["detail"]

    def test_update_sms_template_invalid_variables(self, client: TestClient):
        """Test that template with invalid variables is rejected."""
        response = client.put("/api/v1/settings/sms-template", json={
            "template": "Hi {name}, your shift is {invalid_var}."
        })

        assert response.status_code == 400
        detail = response.json()["detail"]
        assert "Invalid template variables" in detail
        assert "invalid_var" in detail

    def test_update_sms_template_too_long(self, client: TestClient):
        """Test that template exceeding character limit is rejected."""
        # Create a template > 320 characters
        long_template = "Hi {name}, " + "x" * 350

        response = client.put("/api/v1/settings/sms-template", json={
            "template": long_template
        })

        # Pydantic validation catches this before endpoint logic (422 vs 400)
        assert response.status_code == 422
        detail = response.json()["detail"]
        assert isinstance(detail, list) or "320" in str(detail)

    def test_update_sms_template_max_length(self, client: TestClient):
        """Test template at exactly 320 characters (2 SMS segments)."""
        # Create a template at exactly 320 chars
        template = "Hi {name}, " + "x" * 298 + " {duration}"
        assert len(template) == 320

        response = client.put("/api/v1/settings/sms-template", json={
            "template": template
        })

        assert response.status_code == 200
        data = response.json()
        assert data["character_count"] == 320
        assert data["sms_count"] == 2

    def test_sms_count_calculation(self, client: TestClient):
        """Test SMS segment count calculation for various lengths."""
        test_cases = [
            ("Hi {name}!", 1),  # 10 chars = 1 SMS
            ("Hi {name}, " + "x" * 148, 1),  # 159 chars = 1 SMS
            ("Hi {name}, " + "x" * 149, 1),  # 160 chars = 1 SMS (exactly fills one segment)
            ("Hi {name}, " + "x" * 150, 2),  # 161 chars = 2 SMS (spills to second segment)
            ("Hi {name}, " + "x" * 309, 2),  # 320 chars = 2 SMS (max allowed)
        ]

        for template, expected_sms_count in test_cases:
            response = client.put("/api/v1/settings/sms-template", json={
                "template": template
            })

            assert response.status_code == 200, f"Template length {len(template)} failed: {response.json()}"
            data = response.json()
            assert data["sms_count"] == expected_sms_count, \
                f"Template of {len(template)} chars should be {expected_sms_count} SMS, got {data['sms_count']}"

    def test_template_persistence(self, client: TestClient):
        """Test that template changes persist across requests."""
        # Update template
        new_template = "Test {name} {duration}"
        response = client.put("/api/v1/settings/sms-template", json={
            "template": new_template
        })
        assert response.status_code == 200

        # Retrieve template
        response = client.get("/api/v1/settings/sms-template")
        assert response.status_code == 200
        data = response.json()
        assert data["template"] == new_template

    def test_template_with_all_variables(self, client: TestClient):
        """Test template containing all supported variables."""
        template = "Alert: {name} on-call {start_time}-{end_time} ({duration})"

        response = client.put("/api/v1/settings/sms-template", json={
            "template": template
        })

        assert response.status_code == 200
        data = response.json()
        assert set(data["variables"]) == {"name", "start_time", "end_time", "duration"}

    def test_template_with_subset_variables(self, client: TestClient):
        """Test template with only some variables (valid)."""
        template = "Hi {name}, shift starts {start_time}"

        response = client.put("/api/v1/settings/sms-template", json={
            "template": template
        })

        assert response.status_code == 200
        data = response.json()
        assert set(data["variables"]) == {"name", "start_time"}

    def test_template_with_multiline(self, client: TestClient):
        """Test template with line breaks."""
        template = """WhoseOnFirst Alert

Hi {name}, you are on-call from {start_time} to {end_time}.

Duration: {duration}"""

        response = client.put("/api/v1/settings/sms-template", json={
            "template": template
        })

        assert response.status_code == 200
        data = response.json()
        assert data["template"] == template
        assert "\n" in data["template"]

    def test_variable_extraction_regex(self, client: TestClient):
        """Test that variable extraction correctly identifies all placeholders."""
        template = "{name} {name} {start_time} {end_time} {duration} {name}"

        response = client.put("/api/v1/settings/sms-template", json={
            "template": template
        })

        assert response.status_code == 200
        data = response.json()
        # Variables list may include duplicates from regex findall
        assert "name" in data["variables"]
        assert "start_time" in data["variables"]
        assert "end_time" in data["variables"]
        assert "duration" in data["variables"]
