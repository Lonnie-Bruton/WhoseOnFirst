# Frontend Development Roadmap

**Status:** Ready to Build
**Backend:** 100% Complete ✅
**Mockups:** 5 pages ready
**Backend API:** 15 endpoints operational

---

## Development Strategy

Build and test each page completely before moving to the next. This ensures:
- Each component works end-to-end before adding complexity
- We can catch and fix issues early
- We build confidence with the API patterns
- Each page serves as a foundation for the next

---

## Phase 1: Team Members Page ✅ COMPLETE

**File:** `frontend/team-members.html`
**Status:** ✅ Complete (2025-11-08)
**Actual Time:** ~6 hours
**Dependencies:** None

### Why First?
- Foundation for everything else (need members to generate schedules)
- Simplest CRUD operations - good learning experience
- Tests the new rotation_order feature we just built
- Establishes patterns we'll reuse on other pages

### Tasks:

#### 1.1 Load and Display Team Members ✅
- [x] Replace static member cards with dynamic API data
- [x] Fetch from `GET /api/v1/team-members/`
- [x] Render member cards with correct data (name, phone, status, rotation_order)
- [x] Show loading state while fetching
- [x] Handle empty state (no members yet)
- [x] Color-code members (team-color-1 through team-color-7) - WCAG AA compliant
- [x] Show member initials in colored avatars
- [x] Display 1-based rotation numbers prominently

#### 1.2 Create New Team Member ✅
- [x] Wire up "Add Team Member" modal form
- [x] Validate phone number format (E.164: +1XXXXXXXXXX)
- [x] POST to `/api/v1/team-members/`
- [x] Show success/error messages
- [x] Reload member list after creation
- [x] Clear form after successful creation
- [x] Handle duplicate phone error gracefully (temporarily disabled for testing)

#### 1.3 Edit Existing Team Member ✅
- [x] Wire up edit button to load member data into modal
- [x] Pre-populate edit form with existing values
- [x] PUT to `/api/v1/team-members/{id}`
- [x] Update UI after successful edit
- [x] Validate changes before submission

#### 1.4 Activate/Deactivate Members ✅
- [x] Wire up deactivate button
- [x] DELETE to `/api/v1/team-members/{id}` (soft delete)
- [x] Wire up activate button
- [x] POST to `/api/v1/team-members/{id}/activate`
- [x] Update member card status visually
- [x] Show confirmation dialog before deactivating
- [x] Auto-clear rotation_order on deactivate
- [x] Auto-assign rotation_order on activate

#### 1.5 Drag-and-Drop Reordering ✅
- [x] Add SortableJS library (https://sortablejs.github.io/Sortable/)
- [x] Make member list sortable via drag-and-drop
- [x] Show "Save Order" button when order changes
- [x] PUT to `/api/v1/team-members/reorder` with new order mapping
- [x] Update rotation_order display after save
- [x] Show visual feedback during drag operations
- [x] Fix route ordering issue (moved `/reorder` before `/{member_id}`)

#### 1.6 Filter by Active/Inactive ✅
- [x] Add filter toggle/dropdown
- [x] Use `GET /api/v1/team-members/?active_only=true`
- [x] Update displayed members based on filter
- [x] Simplified to Active/Inactive only (removed "All Members")
- [x] Disable drag-and-drop for inactive view

#### 1.7 Permanent Delete (BONUS FEATURE!) ✅
- [x] Add `DELETE /api/v1/team-members/{id}/permanent` endpoint
- [x] Shift+Click on Deactivate triggers permanent delete
- [x] Confirmation modal with name verification
- [x] Red warning UI to prevent accidental deletion

### Acceptance Criteria:
- ✅ Can create new team member with valid phone
- ✅ Cannot create member with invalid phone format
- ✅ Cannot create member with duplicate phone (temporarily disabled)
- ✅ Can edit member name and phone
- ✅ Can deactivate active member
- ✅ Can reactivate inactive member
- ✅ Can drag-and-drop to reorder members
- ✅ Rotation order persists after page reload
- ✅ Filter works correctly for active/inactive
- ✅ Error messages are clear and helpful
- ✅ Loading states prevent user confusion
- ✅ Permanent delete requires name confirmation
- ✅ WCAG AA accessibility standards met

### Testing Checklist:
```
[ ] Create member: "Alice Smith", "+19185551111"
[ ] Create member: "Bob Jones", "+19185552222"
[ ] Try to create duplicate phone → should fail
[ ] Try to create invalid phone "+1918555" → should fail
[ ] Edit Alice's name to "Alice Johnson"
[ ] Drag Bob above Alice in the list
[ ] Save reorder → verify rotation_order updated
[ ] Deactivate Bob
[ ] Filter to "Active Only" → should only show Alice
[ ] Reactivate Bob
[ ] Reload page → order should persist
```

---

## Phase 2: Shifts Page (MEDIUM PRIORITY)

**File:** `frontend/shifts.html`
**Estimated Time:** 3-4 hours
**Dependencies:** None (independent of team members)

### Why Second?
- Need shifts configured before generating schedules
- Simpler than schedule generation
- Similar CRUD patterns to team members (reinforces learning)

### Tasks:

#### 2.1 Load and Display Shifts
- [ ] Fetch from `GET /api/v1/shifts/`
- [ ] Render shifts table with all fields
- [ ] Show shift number, day(s), duration badge (24h/48h), start time
- [ ] Handle empty state
- [ ] Sort by shift_number

#### 2.2 Create New Shift
- [ ] Wire up "Add Shift" modal form
- [ ] Validate shift number (1-7)
- [ ] Validate duration (24 or 48 hours)
- [ ] POST to `/api/v1/shifts/`
- [ ] Show duplicate shift_number error if applicable
- [ ] Reload shifts list after creation

#### 2.3 Edit Existing Shift
- [ ] Load shift data into edit modal
- [ ] PUT to `/api/v1/shifts/{id}`
- [ ] Update table after successful edit
- [ ] Handle validation errors

#### 2.4 Delete Shift
- [ ] Show confirmation dialog (warn about cascade delete)
- [ ] DELETE to `/api/v1/shifts/{id}`
- [ ] Remove from table after deletion
- [ ] Handle error if shift has schedules assigned

### Acceptance Criteria:
- ✅ Can create standard 6-shift weekly rotation
- ✅ Can create 48-hour double shift (Tuesday-Wednesday)
- ✅ Cannot create duplicate shift numbers
- ✅ Can edit shift details (day, duration, start time)
- ✅ Can delete shift with confirmation
- ✅ Shifts display correctly in table
- ✅ Visual indicator for 48h shifts (purple badge)

### Testing Checklist:
```
[ ] Create Shift 1: Monday, 24h, 08:00
[ ] Create Shift 2: Tuesday-Wednesday, 48h, 08:00
[ ] Create Shift 3: Thursday, 24h, 08:00
[ ] Try to create duplicate Shift 1 → should fail
[ ] Edit Shift 3 start time to 09:00
[ ] Delete Shift 3 with confirmation
[ ] Verify 6-shift setup matches example pattern
```

---

## Phase 3: Schedule Generation Page (HIGH PRIORITY)

**File:** `frontend/schedule.html`
**Estimated Time:** 6-8 hours
**Dependencies:** Team Members + Shifts must exist

### Why Third?
- Core functionality - generates the actual rotation schedules
- Most complex page (date handling, multi-week generation)
- Tests the rotation algorithm with real data
- Depends on team members and shifts being set up

### Tasks:

#### 3.1 Display Current Team Order
- [ ] Fetch from `GET /api/v1/team-members/?active_only=true`
- [ ] Show numbered list of members in rotation order
- [ ] Display rotation_order value for each member
- [ ] Update list when members are reordered on team-members page

#### 3.2 Schedule Generation Form
- [ ] Set default start date to next Monday
- [ ] Wire up weeks dropdown (1, 2, 4, 8, 12 weeks)
- [ ] Wire up force regenerate checkbox
- [ ] Validate start date is not in the past
- [ ] POST to `/api/v1/schedules/generate`
- [ ] Show loading spinner during generation
- [ ] Display success message with count of schedules created

#### 3.3 Display Schedule Status
- [ ] Fetch from `GET /api/v1/schedules/upcoming?weeks=4`
- [ ] Show coverage period (X weeks)
- [ ] Show date range (start - end)
- [ ] Show total assignments count
- [ ] Update after generation

#### 3.4 Display Quick Stats
- [ ] Fetch active members count
- [ ] Fetch shifts count from `GET /api/v1/shifts/`
- [ ] Show upcoming schedules count

#### 3.5 Error Handling
- [ ] Handle "no team members" error
- [ ] Handle "no shifts configured" error
- [ ] Handle "schedules already exist" error (without force)
- [ ] Clear error messages

### Acceptance Criteria:
- ✅ Can generate schedules for 4 weeks
- ✅ Team order list reflects actual rotation order
- ✅ Cannot generate without team members
- ✅ Cannot generate without shifts
- ✅ Force regenerate works correctly
- ✅ Schedule status updates after generation
- ✅ Error messages guide user to fix issues
- ✅ Start date validation works

### Testing Checklist:
```
[ ] Try to generate without team members → should fail with helpful error
[ ] Try to generate without shifts → should fail with helpful error
[ ] Add 3 team members and 6 shifts
[ ] Generate 4 weeks starting next Monday
[ ] Verify schedule status shows 24 assignments (6 shifts × 4 weeks)
[ ] Try to generate again without force → should fail
[ ] Generate with force checkbox → should succeed
[ ] Verify date range is correct
[ ] Check that rotation order matches team order list
```

---

## Phase 4: Dashboard Page (POLISH)

**File:** `frontend/index.html`
**Estimated Time:** 5-6 hours
**Dependencies:** All other pages complete

### Why Fourth?
- Aggregates data from all other components
- Calendar view is complex and needs real schedule data
- Stats require schedules, members, and notifications to exist
- This is the "wow" page - save the polish for last

### Tasks:

#### 4.1 Stats Cards
- [ ] Fetch active members count
- [ ] Fetch current on-call person from `GET /api/v1/schedules/current`
- [ ] Calculate SMS count this month from notification logs
- [ ] Calculate delivery rate from notification logs
- [ ] Update stats every 30 seconds (optional)

#### 4.2 Calendar View
- [ ] Fetch current month schedules
- [ ] Parse schedule data and populate calendar grid
- [ ] Color-code by team member (using team-color-X classes)
- [ ] Show member name in calendar day
- [ ] Highlight 48h shifts (show on both days)
- [ ] Navigate to previous/next month

#### 4.3 Team Legend
- [ ] Fetch all team members
- [ ] Generate color-coded legend dynamically
- [ ] Match colors with calendar display

#### 4.4 Recent Notifications Table
- [ ] Fetch recent notifications from notification log
- [ ] Display timestamp, member, phone (sanitized), status
- [ ] Show Twilio SID
- [ ] Link to full notification history page

#### 4.5 Quick Actions
- [ ] Wire up "Generate Schedule" button → redirect to schedule page
- [ ] Wire up "Send Test SMS" button → POST to `/api/v1/schedules/notifications/trigger`
- [ ] Show success/error toasts

### Acceptance Criteria:
- ✅ Stats cards show real data
- ✅ Calendar displays current month schedules correctly
- ✅ Colors match between calendar and legend
- ✅ Can navigate months
- ✅ Recent notifications show correctly
- ✅ Quick actions work
- ✅ Page looks polished and professional

### Testing Checklist:
```
[ ] Generate schedules for current month
[ ] Verify calendar shows all assignments
[ ] Check that colors are consistent
[ ] Click "Send Test SMS" → verify notification sent
[ ] Check recent notifications table updates
[ ] Navigate to next month → verify calendar updates
[ ] Verify stats cards show correct counts
```

---

## Phase 5: Notifications Page (MONITORING)

**File:** `frontend/notifications.html`
**Estimated Time:** 4-5 hours
**Dependencies:** Schedules must be generated and notifications sent

### Why Last?
- Administrative/monitoring feature
- Less critical for core functionality
- Depends on having notification data (from SMS sends)
- Good final polish

### Tasks:

#### 5.1 Stats Cards
- [ ] Calculate total sent (all time)
- [ ] Calculate this month count
- [ ] Calculate delivery rate percentage
- [ ] Count failed notifications

#### 5.2 SMS Template Display
- [ ] Show current SMS message template
- [ ] Display send time (8:00 AM CST)
- [ ] Show active/inactive status

#### 5.3 Notification Schedule Display
- [ ] Show daily shift start notification (8:00 AM)
- [ ] Show enabled/disabled badges
- [ ] (Reminder and weekly summary are future features)

#### 5.4 Notification History Table
- [ ] Fetch notification logs
- [ ] Display timestamp, recipient, phone, status
- [ ] Show Twilio SID
- [ ] Color-code by status (green=delivered, red=failed)
- [ ] Add pagination (show 10-20 per page)
- [ ] Add date filters

#### 5.5 Twilio Configuration Status
- [ ] Display account SID (masked)
- [ ] Show from phone number
- [ ] Show connection status
- [ ] (Balance and last test are nice-to-haves)

#### 5.6 Send Test SMS
- [ ] Wire up "Send Test SMS" button
- [ ] POST to `/api/v1/schedules/notifications/trigger`
- [ ] Show result (count sent, any errors)
- [ ] Refresh notification history after send

### Acceptance Criteria:
- ✅ Notification history shows all sent messages
- ✅ Stats reflect actual data
- ✅ Can send test SMS manually
- ✅ Filters work correctly
- ✅ Pagination works
- ✅ Status badges are accurate

### Testing Checklist:
```
[ ] Send test SMS from dashboard
[ ] Verify notification appears in history
[ ] Check status badge (delivered/failed)
[ ] Verify stats update correctly
[ ] Test date filter
[ ] Test pagination
[ ] Verify Twilio SID displays correctly
```

---

## Development Best Practices

### 1. Error Handling Pattern
```javascript
try {
    const response = await fetch(`${API_BASE}/endpoint`);
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Operation failed');
    }
    const data = await response.json();
    // Success handling
} catch (error) {
    console.error('Error:', error);
    alert(`❌ ${error.message}`);
}
```

### 2. Loading States
```javascript
button.disabled = true;
button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
// ... perform operation ...
button.disabled = false;
button.innerHTML = originalText;
```

### 3. Form Validation
- Always validate on client side first (UX)
- Let server validation catch edge cases
- Show specific error messages from API

### 4. Testing Approach
- Test each CRUD operation manually
- Test error cases (duplicate, invalid data, not found)
- Test with empty database
- Test with populated database
- Test navigation between pages

---

## Libraries to Add

### SortableJS (for drag-and-drop)
```html
<script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
```

### Optional: Toastr (for better notifications)
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>
```

---

## Estimated Total Time

| Phase | Page | Hours |
|-------|------|-------|
| 1 | Team Members | 4-6h |
| 2 | Shifts | 3-4h |
| 3 | Schedule | 6-8h |
| 4 | Dashboard | 5-6h |
| 5 | Notifications | 4-5h |
| **Total** | | **22-29h** |

Spread over 3-4 focused sessions.

---

## Ready to Start?

**Recommendation:** Start with Phase 1 (Team Members) today!

It's the perfect first page because:
- ✅ No dependencies
- ✅ Tests the rotation_order feature we just built
- ✅ Establishes patterns for other pages
- ✅ Quick wins build momentum

Would you like me to help you start implementing Phase 1 now?
