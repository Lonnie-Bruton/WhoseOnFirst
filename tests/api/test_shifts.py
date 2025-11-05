"""
Shifts API endpoint tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.shift import Shift


class TestListShifts:
    """Tests for GET /api/v1/shifts/"""

    def test_list_empty(self, client: TestClient):
        """Test listing shifts when database is empty."""
        response = client.get("/api/v1/shifts/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_all_shifts(self, client: TestClient, db_session: Session):
        """Test listing all shift configurations."""
        # Create test data
        shift1 = Shift(shift_number=1, day_of_week="Monday", duration_hours=24, start_time="08:00")
        shift2 = Shift(shift_number=2, day_of_week="Tuesday-Wednesday", duration_hours=48, start_time="08:00")
        db_session.add_all([shift1, shift2])
        db_session.commit()

        response = client.get("/api/v1/shifts/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["shift_number"] == 1
        assert data[1]["shift_number"] == 2


class TestGetShift:
    """Tests for GET /api/v1/shifts/{id}"""

    def test_get_existing_shift(self, client: TestClient, db_session: Session):
        """Test getting an existing shift configuration."""
        shift = Shift(shift_number=1, day_of_week="Monday", duration_hours=24, start_time="08:00")
        db_session.add(shift)
        db_session.commit()
        db_session.refresh(shift)

        response = client.get(f"/api/v1/shifts/{shift.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == shift.id
        assert data["shift_number"] == 1
        assert data["day_of_week"] == "Monday"
        assert data["duration_hours"] == 24
        assert data["start_time"] == "08:00:00"

    def test_get_nonexistent_shift(self, client: TestClient):
        """Test getting a shift that doesn't exist."""
        response = client.get("/api/v1/shifts/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestCreateShift:
    """Tests for POST /api/v1/shifts/"""

    def test_create_valid_shift_24h(self, client: TestClient):
        """Test creating a valid 24-hour shift."""
        shift_data = {
            "shift_number": 1,
            "day_of_week": "Monday",
            "duration_hours": 24,
            "start_time": "08:00:00"
        }
        response = client.post("/api/v1/shifts/", json=shift_data)
        assert response.status_code == 201
        data = response.json()
        assert data["shift_number"] == 1
        assert data["day_of_week"] == "Monday"
        assert data["duration_hours"] == 24
        assert data["start_time"] == "08:00:00"
        assert "id" in data
        assert "created_at" in data

    def test_create_valid_shift_48h(self, client: TestClient):
        """Test creating a valid 48-hour shift."""
        shift_data = {
            "shift_number": 2,
            "day_of_week": "Tuesday-Wednesday",
            "duration_hours": 48,
            "start_time": "08:00:00"
        }
        response = client.post("/api/v1/shifts/", json=shift_data)
        assert response.status_code == 201
        data = response.json()
        assert data["duration_hours"] == 48
        assert data["day_of_week"] == "Tuesday-Wednesday"

    def test_create_duplicate_shift_number(self, client: TestClient, db_session: Session):
        """Test creating shift with duplicate shift number."""
        # Create existing shift
        existing = Shift(shift_number=1, day_of_week="Monday", duration_hours=24, start_time="08:00")
        db_session.add(existing)
        db_session.commit()

        # Try to create duplicate
        shift_data = {
            "shift_number": 1,
            "day_of_week": "Tuesday",
            "duration_hours": 24,
            "start_time": "08:00:00"
        }
        response = client.post("/api/v1/shifts/", json=shift_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_create_invalid_duration(self, client: TestClient):
        """Test creating shift with invalid duration."""
        shift_data = {
            "shift_number": 1,
            "day_of_week": "Monday",
            "duration_hours": 12,  # Invalid: must be 24 or 48
            "start_time": "08:00:00"
        }
        response = client.post("/api/v1/shifts/", json=shift_data)
        assert response.status_code == 422  # Pydantic validation error

    def test_create_invalid_start_time_format(self, client: TestClient):
        """Test creating shift with invalid start time format."""
        shift_data = {
            "shift_number": 1,
            "day_of_week": "Monday",
            "duration_hours": 24,
            "start_time": "8:00"  # Invalid: must be HH:MM
        }
        response = client.post("/api/v1/shifts/", json=shift_data)
        assert response.status_code == 422  # Pydantic validation error

    def test_create_missing_required_fields(self, client: TestClient):
        """Test creating shift without required fields."""
        shift_data = {
            "shift_number": 1,
            "day_of_week": "Monday"
            # Missing duration_hours and start_time
        }
        response = client.post("/api/v1/shifts/", json=shift_data)
        assert response.status_code == 422  # Pydantic validation error

    def test_create_empty_day_of_week(self, client: TestClient):
        """Test creating shift with empty day of week."""
        shift_data = {
            "shift_number": 1,
            "day_of_week": "   ",  # Whitespace only
            "duration_hours": 24,
            "start_time": "08:00:00"
        }
        response = client.post("/api/v1/shifts/", json=shift_data)
        assert response.status_code == 422  # Pydantic validation error


class TestUpdateShift:
    """Tests for PUT /api/v1/shifts/{id}"""

    def test_update_day_of_week(self, client: TestClient, db_session: Session):
        """Test updating shift day of week."""
        shift = Shift(shift_number=1, day_of_week="Monday", duration_hours=24, start_time="08:00")
        db_session.add(shift)
        db_session.commit()
        db_session.refresh(shift)

        update_data = {"day_of_week": "Tuesday"}
        response = client.put(f"/api/v1/shifts/{shift.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["day_of_week"] == "Tuesday"
        assert data["shift_number"] == 1  # Unchanged
        assert data["duration_hours"] == 24  # Unchanged

    def test_update_duration(self, client: TestClient, db_session: Session):
        """Test updating shift duration."""
        shift = Shift(shift_number=2, day_of_week="Tuesday", duration_hours=24, start_time="08:00")
        db_session.add(shift)
        db_session.commit()
        db_session.refresh(shift)

        update_data = {"duration_hours": 48, "day_of_week": "Tuesday-Wednesday"}
        response = client.put(f"/api/v1/shifts/{shift.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["duration_hours"] == 48
        assert data["day_of_week"] == "Tuesday-Wednesday"

    def test_update_start_time(self, client: TestClient, db_session: Session):
        """Test updating shift start time."""
        shift = Shift(shift_number=1, day_of_week="Monday", duration_hours=24, start_time="08:00")
        db_session.add(shift)
        db_session.commit()
        db_session.refresh(shift)

        update_data = {"start_time": "20:00"}
        response = client.put(f"/api/v1/shifts/{shift.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["start_time"] == "20:00:00"

    def test_update_nonexistent_shift(self, client: TestClient):
        """Test updating a shift that doesn't exist."""
        update_data = {"day_of_week": "Tuesday"}
        response = client.put("/api/v1/shifts/999", json=update_data)
        assert response.status_code == 404

    def test_update_invalid_duration(self, client: TestClient, db_session: Session):
        """Test updating to invalid duration."""
        shift = Shift(shift_number=1, day_of_week="Monday", duration_hours=24, start_time="08:00")
        db_session.add(shift)
        db_session.commit()
        db_session.refresh(shift)

        update_data = {"duration_hours": 36}  # Invalid
        response = client.put(f"/api/v1/shifts/{shift.id}", json=update_data)
        assert response.status_code == 422  # Pydantic validation error

    def test_update_duplicate_shift_number(self, client: TestClient, db_session: Session):
        """Test updating to a shift number that already exists."""
        shift1 = Shift(shift_number=1, day_of_week="Monday", duration_hours=24, start_time="08:00")
        shift2 = Shift(shift_number=2, day_of_week="Tuesday", duration_hours=24, start_time="08:00")
        db_session.add_all([shift1, shift2])
        db_session.commit()
        db_session.refresh(shift1)

        # Try to update shift1 to have shift2's number
        update_data = {"shift_number": 2}
        response = client.put(f"/api/v1/shifts/{shift1.id}", json=update_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()


class TestDeleteShift:
    """Tests for DELETE /api/v1/shifts/{id}"""

    def test_delete_existing_shift(self, client: TestClient, db_session: Session):
        """Test deleting an existing shift."""
        shift = Shift(shift_number=1, day_of_week="Monday", duration_hours=24, start_time="08:00")
        db_session.add(shift)
        db_session.commit()
        db_session.refresh(shift)
        shift_id = shift.id

        response = client.delete(f"/api/v1/shifts/{shift_id}")
        assert response.status_code == 204

        # Verify shift is deleted
        deleted_shift = db_session.query(Shift).filter(Shift.id == shift_id).first()
        assert deleted_shift is None

    def test_delete_nonexistent_shift(self, client: TestClient):
        """Test deleting a shift that doesn't exist."""
        response = client.delete("/api/v1/shifts/999")
        assert response.status_code == 404


class TestShiftIntegration:
    """Integration tests for shift workflows."""

    def test_full_lifecycle(self, client: TestClient):
        """Test complete shift lifecycle: create -> update -> delete."""
        # Create
        create_data = {
            "shift_number": 1,
            "day_of_week": "Monday",
            "duration_hours": 24,
            "start_time": "08:00:00"
        }
        response = client.post("/api/v1/shifts/", json=create_data)
        assert response.status_code == 201
        shift_id = response.json()["id"]

        # Read
        response = client.get(f"/api/v1/shifts/{shift_id}")
        assert response.status_code == 200
        assert response.json()["day_of_week"] == "Monday"

        # Update
        update_data = {
            "day_of_week": "Tuesday",
            "duration_hours": 48
        }
        response = client.put(f"/api/v1/shifts/{shift_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["day_of_week"] == "Tuesday"
        assert response.json()["duration_hours"] == 48

        # Delete
        response = client.delete(f"/api/v1/shifts/{shift_id}")
        assert response.status_code == 204

        # Verify deleted
        response = client.get(f"/api/v1/shifts/{shift_id}")
        assert response.status_code == 404

    def test_create_standard_weekly_rotation(self, client: TestClient):
        """Test creating a standard 6-shift weekly rotation."""
        shifts = [
            {"shift_number": 1, "day_of_week": "Monday", "duration_hours": 24, "start_time": "08:00"},
            {"shift_number": 2, "day_of_week": "Tuesday-Wednesday", "duration_hours": 48, "start_time": "08:00"},
            {"shift_number": 3, "day_of_week": "Thursday", "duration_hours": 24, "start_time": "08:00"},
            {"shift_number": 4, "day_of_week": "Friday", "duration_hours": 24, "start_time": "08:00"},
            {"shift_number": 5, "day_of_week": "Saturday", "duration_hours": 24, "start_time": "08:00"},
            {"shift_number": 6, "day_of_week": "Sunday", "duration_hours": 24, "start_time": "08:00"},
        ]

        # Create all shifts
        for shift_data in shifts:
            response = client.post("/api/v1/shifts/", json=shift_data)
            assert response.status_code == 201

        # Verify all shifts exist
        response = client.get("/api/v1/shifts/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 6

        # Verify shift numbers are sequential
        shift_numbers = [s["shift_number"] for s in data]
        assert shift_numbers == [1, 2, 3, 4, 5, 6]
