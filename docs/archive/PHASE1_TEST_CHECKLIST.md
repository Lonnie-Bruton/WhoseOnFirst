# Phase 1: Team Members - Test Checklist

**Date:** 2025-11-08
**Status:** Ready for Testing

## Setup

1. **Start Backend Server:**
   ```bash
   cd /Volumes/DATA/GitHub/WhoseOnFirst
   source venv/bin/activate
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open Frontend:**
   ```
   Open: frontend/team-members.html in your browser
   ```

---

## Test Scenarios

### ✅ 1. Load Empty State
- [ ] Open page with no members
- [ ] **Expected:** See empty state with "No team members yet" message
- [ ] **Expected:** See "Add Team Member" button

### ✅ 2. Create First Team Member
- [ ] Click "Add Team Member"
- [ ] Enter name: "Alice Smith"
- [ ] Enter phone: "+19185551111"
- [ ] Click "Add Member"
- [ ] **Expected:** Success message appears
- [ ] **Expected:** Member card appears with:
  - Name: Alice Smith
  - Phone: +19185551111
  - Badge: Active
  - Order: Not set (or a number if migration set it)

### ✅ 3. Create Second Team Member
- [ ] Click "Add Team Member"
- [ ] Enter name: "Bob Jones"
- [ ] Enter phone: "+19185552222"
- [ ] Click "Add Member"
- [ ] **Expected:** Success message
- [ ] **Expected:** Two member cards displayed

### ✅ 4. Validation - Duplicate Phone
- [ ] Try to create member with phone "+19185551111" (Alice's number)
- [ ] **Expected:** Error message about duplicate phone

### ✅ 5. Validation - Invalid Phone Format
- [ ] Try phone: "+1918555" (too short)
- [ ] **Expected:** HTML5 validation error or API error
- [ ] Try phone: "9185551234" (missing +1)
- [ ] **Expected:** HTML5 validation error

### ✅ 6. Edit Member
- [ ] Click "Edit" on Alice's card
- [ ] **Expected:** Modal opens with pre-filled data
- [ ] Change name to "Alice Johnson"
- [ ] Click "Save Changes"
- [ ] **Expected:** Success message
- [ ] **Expected:** Card updates to show "Alice Johnson"

### ✅ 7. Deactivate Member
- [ ] Click "Deactivate" on Bob
- [ ] **Expected:** Confirmation dialog
- [ ] Click OK
- [ ] **Expected:** Success message
- [ ] **Expected:** Badge changes to "Inactive" (gray)
- [ ] **Expected:** Button changes to "Activate"

### ✅ 8. Activate Member
- [ ] Click "Activate" on Bob
- [ ] **Expected:** Confirmation dialog
- [ ] Click OK
- [ ] **Expected:** Success message
- [ ] **Expected:** Badge changes to "Active" (green)
- [ ] **Expected:** Button changes to "Deactivate"

### ✅ 9. Filter - Active Only
- [ ] Deactivate Bob again
- [ ] Select "Active Only" from filter dropdown
- [ ] **Expected:** Only Alice shows
- [ ] **Expected:** Bob is hidden

### ✅ 10. Filter - Inactive Only
- [ ] Select "Inactive Only"
- [ ] **Expected:** Only Bob shows
- [ ] **Expected:** Alice is hidden

### ✅ 11. Filter - All Members
- [ ] Select "All Members"
- [ ] **Expected:** Both Alice and Bob show

### ✅ 12. Drag-and-Drop Reordering
- [ ] Create a third member "Charlie Davis" "+19185553333"
- [ ] **Expected:** Drag-and-drop hint appears
- [ ] Drag Charlie to the top position
- [ ] **Expected:** "Save Rotation Order" button appears (bottom-right)
- [ ] **Expected:** Cards visually reorder

### ✅ 13. Save Rotation Order
- [ ] Click "Save Rotation Order"
- [ ] **Expected:** Button shows "Saving..." spinner
- [ ] **Expected:** Success message
- [ ] **Expected:** Button disappears
- [ ] **Expected:** rotation_order values update on cards

### ✅ 14. Rotation Order Persists
- [ ] Reload page (F5)
- [ ] **Expected:** Members appear in same order as saved
- [ ] **Expected:** rotation_order values match

### ✅ 15. Loading State
- [ ] Clear browser cache and reload
- [ ] **Expected:** Brief loading spinner appears
- [ ] **Expected:** Members load after spinner

### ✅ 16. Error Handling - Server Down
- [ ] Stop backend server
- [ ] Reload page
- [ ] **Expected:** Error message about backend not running
- [ ] Restart server
- [ ] Reload page
- [ ] **Expected:** Members load successfully

---

## Visual Checks

- [ ] Member cards have different colors (team-color-1 through team-color-7)
- [ ] Drag icon (grip-vertical) visible on avatar
- [ ] Cards have hover effect (slight lift)
- [ ] Buttons have appropriate icons
- [ ] Loading states show spinners
- [ ] Empty state is centered and attractive

---

## Backend API Verification

Check these endpoints are working:

1. **GET** `/api/v1/team-members/` - List all members
2. **POST** `/api/v1/team-members/` - Create member
3. **PUT** `/api/v1/team-members/{id}` - Update member
4. **DELETE** `/api/v1/team-members/{id}` - Deactivate member
5. **POST** `/api/v1/team-members/{id}/activate` - Activate member
6. **PUT** `/api/v1/team-members/reorder` - Update rotation order

You can verify via Swagger UI: http://localhost:8000/docs

---

## Success Criteria

All boxes checked = Phase 1 Complete! ✅

**Sign-off:** _______________
**Date:** _______________
