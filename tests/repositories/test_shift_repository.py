"""
Tests for ShiftRepository.

Tests shift configuration management including weekend shifts,
duration queries, and shift number validation.
"""

import pytest
from src.repositories import ShiftRepository


class TestShiftRepositoryCRUD:
    """Tests for basic CRUD operations on shifts."""

    def test_create_shift(self, shift_repo, sample_shift_data):
        """Test creating a shift."""
        shift = shift_repo.create(sample_shift_data)

        assert shift.id is not None
        assert shift.shift_number == 1
        assert shift.day_of_week == "Monday"
        assert shift.duration_hours == 24

    def test_get_by_id(self, shift_repo, sample_shift_data):
        """Test retrieving shift by ID."""
        created = shift_repo.create(sample_shift_data)
        retrieved = shift_repo.get_by_id(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id

    def test_update_shift(self, shift_repo, sample_shift_data):
        """Test updating shift."""
        shift = shift_repo.create(sample_shift_data)
        updated = shift_repo.update(shift.id, {"duration_hours": 48})

        assert updated.duration_hours == 48

    def test_delete_shift(self, shift_repo, sample_shift_data):
        """Test deleting shift."""
        shift = shift_repo.create(sample_shift_data)
        result = shift_repo.delete(shift.id)

        assert result is True
        assert shift_repo.get_by_id(shift.id) is None


class TestShiftRepositoryQueries:
    """Tests for shift-specific query methods."""

    def test_get_by_shift_number(self, shift_repo, populated_shifts):
        """Test retrieving shift by shift number."""
        shift = shift_repo.get_by_shift_number(3)

        assert shift is not None
        assert shift.shift_number == 3
        assert shift.day_of_week == "Thursday"

    def test_get_all_ordered(self, shift_repo, populated_shifts):
        """Test retrieving all shifts in order."""
        shifts = shift_repo.get_all_ordered()

        assert len(shifts) == 6
        # Verify ordering
        for i, shift in enumerate(shifts, start=1):
            assert shift.shift_number == i

    def test_get_weekend_shifts(self, shift_repo, populated_shifts):
        """Test retrieving weekend shifts."""
        weekend_shifts = shift_repo.get_weekend_shifts()

        assert len(weekend_shifts) == 2
        days = [s.day_of_week for s in weekend_shifts]
        assert any("Saturday" in day for day in days)
        assert any("Sunday" in day for day in days)

    def test_get_by_duration_24h(self, shift_repo, populated_shifts):
        """Test retrieving 24-hour shifts."""
        shifts_24h = shift_repo.get_by_duration(24)

        assert len(shifts_24h) == 5
        assert all(s.duration_hours == 24 for s in shifts_24h)

    def test_get_by_duration_48h(self, shift_repo, populated_shifts):
        """Test retrieving 48-hour shifts."""
        shifts_48h = shift_repo.get_by_duration(48)

        assert len(shifts_48h) == 1
        assert shifts_48h[0].day_of_week == "Tuesday-Wednesday"

    def test_get_by_day_of_week(self, shift_repo, populated_shifts):
        """Test retrieving shifts by day."""
        monday_shifts = shift_repo.get_by_day_of_week("Monday")

        assert len(monday_shifts) == 1
        assert monday_shifts[0].shift_number == 1

    def test_get_max_shift_number(self, shift_repo, populated_shifts):
        """Test getting maximum shift number."""
        max_num = shift_repo.get_max_shift_number()

        assert max_num == 6

    def test_get_max_shift_number_empty(self, shift_repo):
        """Test getting max shift number with no shifts returns 0."""
        max_num = shift_repo.get_max_shift_number()
        assert max_num == 0


class TestShiftRepositoryValidation:
    """Tests for shift number validation."""

    def test_shift_number_exists_true(self, shift_repo, populated_shifts):
        """Test shift_number_exists returns True for existing number."""
        exists = shift_repo.shift_number_exists(3)
        assert exists is True

    def test_shift_number_exists_false(self, shift_repo, populated_shifts):
        """Test shift_number_exists returns False for non-existent number."""
        exists = shift_repo.shift_number_exists(99)
        assert exists is False

    def test_shift_number_exists_with_exclusion(self, shift_repo, populated_shifts):
        """Test shift_number_exists with ID exclusion for updates."""
        shift = shift_repo.get_by_shift_number(1)

        # Should return False when excluding the shift's own ID
        exists = shift_repo.shift_number_exists(1, exclude_id=shift.id)
        assert exists is False

        # Should return True for other shift numbers
        exists = shift_repo.shift_number_exists(2, exclude_id=shift.id)
        assert exists is True
