# Design Document: Voice Room Stage Management

## Overview

The Voice Room Stage Management feature extends the existing voice room functionality with a structured stage-based participation system. This design implements role-based access control (Host, Moderator, Stage Participant, Visitor), dynamic stage slot management, and granular permission controls for whiteboard access.

The system builds on the existing Flask/SocketIO architecture and MySQL database, adding new database tables for moderator roles and whiteboard permissions, along with enhanced real-time event handling for stage management operations.

Key design principles:
- Real-time synchronization using SocketIO for all stage operations
- Role-based permission enforcement at both backend and frontend
- Optimistic UI updates with server validation
- Graceful degradation for network issues
- Clear visual feedback for all role transitions

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer (Browser)                   │
├─────────────────────────────────────────────────────────────┤
│  • Voice Room UI (HTML/CSS/JavaScript)                      │
│  • WebRTC Media Handling                                     │
│  • SocketIO Client                                           │
│  • Stage Grid Renderer                                       │
│  • Permission-based UI Controls                              │
└─────────────────────────────────────────────────────────────┘
                            ↕ SocketIO Events
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer (Flask)                  │
├─────────────────────────────────────────────────────────────┤
│  • Voice Room Routes (HTTP)                                  │
│  • SocketIO Event Handlers                                   │
│  • Permission Validator                                      │
│  • Stage Manager                                             │
│  • Role Manager                                              │
└─────────────────────────────────────────────────────────────┘
                            ↕ SQL Queries
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer (MySQL)                        │
├─────────────────────────────────────────────────────────────┤
│  • voice_rooms                                               │
│  • room_participants (extended with moderator role)         │
│  • stage_requests                                            │
│  • whiteboard_permissions (new)                              │
│  • room_messages                                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Stage Request Flow**:
   - Visitor clicks "Raise Hand" → Client emits `request_stage` event
   - Server validates request → Creates stage_request record
   - Server broadcasts `stage_request_created` to Host/Moderators
   - Host/Moderator approves → Server updates participant role
   - Server broadcasts `participant_role_changed` to all clients
   - Clients update UI to show participant on stage

2. **Direct Invitation Flow**:
   - Host/Moderator clicks "+" button → Shows visitor list
   - Selects visitor → Client emits `invite_to_stage` event
   - Server validates permission → Updates participant role
   - Server broadcasts `participant_role_changed` to all clients
   - Clients update UI immediately

3. **Permission Grant Flow**:
   - Host/Moderator grants whiteboard permission → Client emits `grant_whiteboard_permission`
   - Server validates permission → Creates whiteboard_permissions record
   - Server broadcasts `whiteboard_permission_changed` to all clients
   - Target participant's UI enables whiteboard controls

## Components and Interfaces

### Database Schema Extensions

#### New Table: whiteboard_permissions
```sql
CREATE TABLE `whiteboard_permissions` (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    room_id         INT NOT NULL,
    user_id         INT NOT NULL,
    granted_by      INT NOT NULL,
    granted_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked_at      TIMESTAMP NULL,
    FOREIGN KEY (room_id) REFERENCES voice_rooms(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (granted_by) REFERENCES users(id),
    UNIQUE KEY unique_active_permission (room_id, user_id, revoked_at)
);
```

#### Modified Table: room_participants
```sql
-- Add moderator to role enum
ALTER TABLE `room_participants` 
MODIFY COLUMN role ENUM('host', 'moderator', 'stage', 'audience') DEFAULT 'audience';
```

### Backend Components

#### 1. Permission Validator

```python
class PermissionValidator:
    """Validates user permissions for stage management operations"""
    
    def can_manage_stage(user_id, room_id, mysql):
        """Check if user can manage stage (host or moderator)"""
        # Returns: bool
        
    def can_grant_whiteboard(user_id, room_id, mysql):
        """Check if user can grant whiteboard permissions"""
        # Returns: bool
        
    def can_remove_participant(user_id, target_user_id, room_id, mysql):
        """Check if user can remove a participant from stage"""
        # Returns: bool (moderators cannot remove host)
        
    def can_end_room(user_id, room_id, mysql):
        """Check if user can end the room (host only)"""
        # Returns: bool
        
    def has_whiteboard_permission(user_id, room_id, mysql):
        """Check if user has active whiteboard permission"""
        # Returns: bool
```

#### 2. Stage Manager

```python
class StageManager:
    """Manages stage participant operations"""
    
    def add_to_stage(room_id, user_id, mysql):
        """Move participant from audience to stage"""
        # Updates room_participants.role to 'stage'
        # Returns: success bool, error message
        
    def remove_from_stage(room_id, user_id, mysql):
        """Move participant from stage to audience"""
        # Updates room_participants.role to 'audience'
        # Revokes whiteboard permission if exists
        # Returns: success bool, error message
        
    def get_stage_participants(room_id, mysql):
        """Get all current stage participants"""
        # Returns: list of participant dicts with role, media status
        
    def get_available_slots(room_id, mysql):
        """Calculate available stage slots"""
        # Returns: int (max_stage - current_stage_count)
```

#### 3. Role Manager

```python
class RoleManager:
    """Manages participant roles and role transitions"""
    
    def assign_moderator(room_id, user_id, assigned_by, mysql):
        """Assign moderator role to stage participant"""
        # Validates: user is on stage, assigner is host
        # Updates room_participants.role to 'moderator'
        # Returns: success bool, error message
        
    def revoke_moderator(room_id, user_id, revoked_by, mysql):
        """Revoke moderator role"""
        # Updates room_participants.role to 'stage'
        # Returns: success bool, error message
        
    def get_user_role(room_id, user_id, mysql):
        """Get current role of user in room"""
        # Returns: 'host' | 'moderator' | 'stage' | 'audience' | None
```

#### 4. Whiteboard Permission Manager

```python
class WhiteboardPermissionManager:
    """Manages whiteboard access permissions"""
    
    def grant_permission(room_id, user_id, granted_by, mysql):
        """Grant whiteboard permission to stage participant"""
        # Creates whiteboard_permissions record
        # Returns: success bool, error message
        
    def revoke_permission(room_id, user_id, mysql):
        """Revoke whiteboard permission"""
        # Sets revoked_at timestamp
        # Returns: success bool, error message
        
    def get_permitted_users(room_id, mysql):
        """Get all users with active whiteboard permission"""
        # Returns: list of user_ids
        
    def auto_revoke_on_stage_leave(room_id, user_id, mysql):
        """Automatically revoke whiteboard permission when leaving stage"""
        # Called by StageManager.remove_from_stage
```

### SocketIO Event Handlers

#### Stage Management Events

```python
@socketio.on('request_stage')
def handle_request_stage(data):
    """
    Visitor requests to join stage
    Input: {room_code: str}
    Emits: 'stage_request_created' to host/moderators
    """

@socketio.on('invite_to_stage')
def handle_invite_to_stage(data):
    """
    Host/Moderator invites visitor to stage
    Input: {room_code: str, target_user_id: int}
    Validates: Caller has manage_stage permission
    Emits: 'participant_role_changed' to room
    """

@socketio.on('approve_stage_request')
def handle_approve_stage_request(data):
    """
    Host/Moderator approves stage request
    Input: {room_code: str, request_id: int}
    Validates: Caller has manage_stage permission
    Emits: 'participant_role_changed' to room
    """

@socketio.on('reject_stage_request')
def handle_reject_stage_request(data):
    """
    Host/Moderator rejects stage request
    Input: {room_code: str, request_id: int}
    Validates: Caller has manage_stage permission
    Emits: 'stage_request_rejected' to requester
    """

@socketio.on('remove_from_stage')
def handle_remove_from_stage(data):
    """
    Host/Moderator removes participant from stage
    Input: {room_code: str, target_user_id: int}
    Validates: Caller has permission, target is not host
    Emits: 'participant_role_changed' to room
    """
```

#### Role Management Events

```python
@socketio.on('assign_moderator')
def handle_assign_moderator(data):
    """
    Host assigns moderator role
    Input: {room_code: str, target_user_id: int}
    Validates: Caller is host, target is on stage
    Emits: 'participant_role_changed' to room
    """

@socketio.on('revoke_moderator')
def handle_revoke_moderator(data):
    """
    Host revokes moderator role
    Input: {room_code: str, target_user_id: int}
    Validates: Caller is host
    Emits: 'participant_role_changed' to room
    """
```

#### Whiteboard Permission Events

```python
@socketio.on('grant_whiteboard_permission')
def handle_grant_whiteboard_permission(data):
    """
    Host/Moderator grants whiteboard permission
    Input: {room_code: str, target_user_id: int}
    Validates: Caller has grant_whiteboard permission
    Emits: 'whiteboard_permission_changed' to room
    """

@socketio.on('revoke_whiteboard_permission')
def handle_revoke_whiteboard_permission(data):
    """
    Host/Moderator revokes whiteboard permission
    Input: {room_code: str, target_user_id: int}
    Validates: Caller has grant_whiteboard permission
    Emits: 'whiteboard_permission_changed' to room
    """
```

### Frontend Components

#### 1. Stage Grid Renderer

```javascript
class StageGridRenderer {
    /**
     * Renders the stage participant grid with slots
     * Layout: 3 slots left | center content | 3 slots right
     */
    
    renderGrid(participants, maxSlots, userRole) {
        // Renders participant cards with profile, badges, media status
        // Shows "+" buttons for empty slots if user is host/moderator
    }
    
    renderParticipantCard(participant) {
        // Shows: profile picture, name, role badge, camera/mic status
        // Shows whiteboard indicator if has permission
    }
    
    renderEmptySlot(slotIndex, canInvite) {
        // Shows "+" button if canInvite is true
        // Shows empty slot otherwise
    }
}
```

#### 2. Permission-based UI Controller

```javascript
class PermissionUIController {
    /**
     * Shows/hides UI elements based on user role
     */
    
    updateUIForRole(role) {
        // Shows/hides: "+" buttons, stage request approvals, 
        // moderator assignment, whiteboard controls
    }
    
    showStageManagementControls(canManage) {
        // Shows "+" buttons and stage request panel
    }
    
    showWhiteboardControls(hasPermission) {
        // Enables/disables whiteboard editing tools
    }
    
    showModeratorControls(isHost) {
        // Shows moderator assignment buttons
    }
}
```

#### 3. Stage Request Manager

```javascript
class StageRequestManager {
    /**
     * Manages stage request UI and interactions
     */
    
    showRaiseHandButton(isVisitor) {
        // Shows "Raise Hand" button for visitors
    }
    
    renderPendingRequests(requests, canApprove) {
        // Shows pending requests with approve/reject buttons
    }
    
    requestStage() {
        // Emits 'request_stage' event
    }
    
    approveRequest(requestId) {
        // Emits 'approve_stage_request' event
    }
    
    rejectRequest(requestId) {
        // Emits 'reject_stage_request' event
    }
}
```

#### 4. Participant Invitation Modal

```javascript
class InvitationModal {
    /**
     * Modal for selecting visitors to invite to stage
     */
    
    show(availableVisitors) {
        // Displays modal with list of visitors
    }
    
    onSelectVisitor(userId) {
        // Emits 'invite_to_stage' event
        // Closes modal
    }
}
```

## Data Models

### Participant Model

```python
{
    'id': int,                    # Participant record ID
    'room_id': int,               # Voice room ID
    'user_id': int,               # User ID
    'name': str,                  # User name
    'role': str,                  # 'host' | 'moderator' | 'stage' | 'audience'
    'is_video_on': bool,          # Camera status
    'is_audio_on': bool,          # Microphone status
    'has_whiteboard_permission': bool,  # Whiteboard access
    'joined_at': datetime,        # Join timestamp
}
```

### Stage Request Model

```python
{
    'id': int,                    # Request ID
    'room_id': int,               # Voice room ID
    'user_id': int,               # Requesting user ID
    'user_name': str,             # Requesting user name
    'status': str,                # 'pending' | 'approved' | 'rejected'
    'requested_at': datetime,     # Request timestamp
    'responded_at': datetime,     # Response timestamp (nullable)
}
```

### Whiteboard Permission Model

```python
{
    'id': int,                    # Permission ID
    'room_id': int,               # Voice room ID
    'user_id': int,               # User with permission
    'granted_by': int,            # User who granted permission
    'granted_at': datetime,       # Grant timestamp
    'revoked_at': datetime,       # Revoke timestamp (nullable)
}
```

### Room State Model (Client-side)

```javascript
{
    roomCode: string,
    hostId: number,
    currentUserId: number,
    currentUserRole: 'host' | 'moderator' | 'stage' | 'audience',
    maxStageSlots: number,
    participants: Participant[],
    stageParticipants: Participant[],
    audienceParticipants: Participant[],
    pendingStageRequests: StageRequest[],
    whiteboardPermittedUsers: Set<number>,
}
```


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Role Assignment and Identification Properties

Property 1: Host role assignment on room creation
*For any* voice room creation, the creating user should be assigned the 'host' role in the room_participants table.
**Validates: Requirements 1.1**

Property 2: Host badge display
*For any* host user profile rendering, the output should contain a "Host" badge indicator.
**Validates: Requirements 1.2**

Property 3: Host has all permissions
*For any* host user in a room, all permission check functions (can_manage_stage, can_grant_whiteboard, can_end_room) should return true.
**Validates: Requirements 1.3**

### Stage Management Properties

Property 4: Stage request creation and visibility
*For any* visitor raising their hand, a stage_request record should be created with status 'pending' and should be visible to the host and all moderators.
**Validates: Requirements 2.2, 5.2, 12.1**

Property 5: Stage request approval transitions role
*For any* pending stage request, when approved by host or moderator, the requesting user's role should transition from 'audience' to 'stage'.
**Validates: Requirements 2.3**

Property 6: Stage request rejection removes request
*For any* pending stage request, when rejected by host or moderator, the request should be removed from the pending list and the visitor's raise hand button should be re-enabled.
**Validates: Requirements 2.4, 5.5**

Property 7: Stage participant removal transitions role
*For any* stage participant (excluding host), when removed by host or moderator, their role should transition from 'stage' to 'audience'.
**Validates: Requirements 2.6**

Property 8: Direct invitation adds to stage
*For any* visitor, when invited to stage by host or moderator, their role should transition from 'audience' to 'stage'.
**Validates: Requirements 8.2, 8.3**

### Whiteboard Permission Properties

Property 9: Host has default whiteboard permission
*For any* newly created voice room, the host should have an active whiteboard_permissions record.
**Validates: Requirements 3.1**

Property 10: Whiteboard permission grant enables editing
*For any* stage participant, when granted whiteboard permission by host or moderator, a whiteboard_permissions record should be created and their UI should show enabled whiteboard controls.
**Validates: Requirements 3.3**

Property 11: Whiteboard permission revocation disables editing
*For any* stage participant with whiteboard permission, when permission is revoked, the whiteboard_permissions record should be marked as revoked and their UI should show disabled whiteboard controls.
**Validates: Requirements 3.4**

Property 12: Whiteboard indicator display
*For any* stage participant profile rendering, if the participant has active whiteboard permission, the output should contain a whiteboard indicator.
**Validates: Requirements 3.5**

Property 13: Auto-revoke whiteboard on stage leave
*For any* stage participant with whiteboard permission, when they are removed from stage, their whiteboard permission should be automatically revoked.
**Validates: Requirements 3.4** (implicit requirement)

### Moderator Role Properties

Property 14: Moderator assignment grants permissions
*For any* stage participant, when assigned moderator role by host, their role should transition to 'moderator' and they should have manage_stage and grant_whiteboard permissions.
**Validates: Requirements 4.2**

Property 15: Moderator badge display
*For any* moderator user profile rendering, the output should contain a "Moderator" badge indicator.
**Validates: Requirements 4.3**

Property 16: Moderator revocation removes permissions
*For any* moderator, when their moderator role is revoked by host, their role should transition to 'stage' and they should lose manage_stage permissions.
**Validates: Requirements 4.5**

Property 17: Moderator can manage stage requests
*For any* moderator in a room, they should be able to successfully approve and reject stage requests.
**Validates: Requirements 11.1, 11.2**

Property 18: Moderator can manage whiteboard permissions
*For any* moderator in a room, they should be able to successfully grant and revoke whiteboard permissions to stage participants.
**Validates: Requirements 11.4, 11.5**

Property 19: Moderator cannot end room
*For any* moderator in a room, the can_end_room permission check should return false.
**Validates: Requirements 11.7**

Property 20: Moderator cannot remove host
*For any* moderator attempting to remove the host from stage, the operation should be rejected.
**Validates: Requirements 11.8**

### Media Control Properties

Property 21: All participants have media controls
*For any* participant (visitor, stage participant, moderator, host), camera and microphone toggle controls should be available in their UI.
**Validates: Requirements 6.1, 6.3, 13.1, 13.3**

Property 22: Media toggle updates state
*For any* participant toggling their camera or microphone, the is_video_on or is_audio_on field should be updated accordingly and reflected in real-time in all participants' UIs.
**Validates: Requirements 6.2, 6.4, 13.2, 13.4, 13.5**

Property 23: Media state preserved on stage transition
*For any* visitor with specific camera and microphone settings, when they transition to stage, their is_video_on and is_audio_on values should remain unchanged.
**Validates: Requirements 6.5**

### UI Layout and Display Properties

Property 24: Stage grid displays all stage participants
*For any* voice room, the video grid should contain exactly the set of participants with role 'host', 'moderator', or 'stage'.
**Validates: Requirements 7.1**

Property 25: Minimum stage slots available
*For any* voice room, the video grid should provide at least 6 stage slots.
**Validates: Requirements 7.2**

Property 26: Participant profile completeness
*For any* stage participant card rendering, the output should contain their profile picture, name, camera status, and microphone status.
**Validates: Requirements 9.1, 9.2, 9.4, 9.5**

Property 27: Role badge conditional display
*For any* stage participant card rendering, if the participant is host or moderator, the output should contain their role badge.
**Validates: Requirements 9.3**

Property 28: Empty slot controls for managers
*For any* empty stage slot, if the current user is host or moderator, a "+" button should be displayed; otherwise, no controls should be shown.
**Validates: Requirements 7.4, 7.5**

Property 29: Stage request display completeness
*For any* pending stage request rendering, the output should contain the requester's name, profile, and both approve and reject buttons.
**Validates: Requirements 12.2, 12.3, 12.4**

Property 30: Stage request synchronization
*For any* stage request that is approved or rejected, the request should be removed from the pending list for all hosts and moderators in the room.
**Validates: Requirements 12.5, 12.6**

Property 31: Raise hand button visibility
*For any* visitor (audience member), a "Raise Hand" button should be displayed in the control bar.
**Validates: Requirements 5.1**

Property 32: Raise hand button disabled when pending
*For any* visitor with a pending stage request, the "Raise Hand" button should be disabled.
**Validates: Requirements 5.3**

Property 33: Whiteboard read-only for unpermitted users
*For any* stage participant without whiteboard permission or any visitor, the whiteboard should be displayed in read-only mode with editing controls disabled.
**Validates: Requirements 10.2, 10.3**

Property 34: Invitation button layout
*For any* voice room UI when viewed by host or moderator, there should be 3 "+" buttons displayed vertically on the left side and 3 "+" buttons displayed vertically on the right side of the video grid.
**Validates: Requirements 14.2, 14.3**

## Error Handling

### Permission Validation Errors

**Unauthorized Stage Management**:
- Scenario: Non-host/non-moderator attempts to invite, approve, or remove participants
- Handling: Return 403 Forbidden error, emit error event to client, log attempt
- User Feedback: "You don't have permission to manage the stage"

**Unauthorized Moderator Assignment**:
- Scenario: Non-host attempts to assign or revoke moderator role
- Handling: Return 403 Forbidden error, emit error event to client
- User Feedback: "Only the host can assign moderators"

**Unauthorized Whiteboard Permission**:
- Scenario: Non-host/non-moderator attempts to grant/revoke whiteboard permission
- Handling: Return 403 Forbidden error, emit error event to client
- User Feedback: "You don't have permission to manage whiteboard access"

**Moderator Attempting to Remove Host**:
- Scenario: Moderator attempts to remove host from stage
- Handling: Return 403 Forbidden error, emit error event to client
- User Feedback: "Moderators cannot remove the host"

**Moderator Attempting to End Room**:
- Scenario: Moderator attempts to end the room
- Handling: Return 403 Forbidden error, emit error event to client
- User Feedback: "Only the host can end the room"

### State Validation Errors

**Stage Capacity Exceeded**:
- Scenario: Attempt to add participant when stage is full
- Handling: Return 400 Bad Request, emit error event to client
- User Feedback: "Stage is full (maximum {max_stage} participants)"

**Invalid Role Transition**:
- Scenario: Attempt to assign moderator to audience member (must be on stage first)
- Handling: Return 400 Bad Request, emit error event to client
- User Feedback: "User must be on stage before becoming a moderator"

**Duplicate Stage Request**:
- Scenario: Visitor attempts to raise hand when they already have a pending request
- Handling: Return 400 Bad Request, emit error event to client
- User Feedback: "You already have a pending stage request"

**Invalid Whiteboard Permission Target**:
- Scenario: Attempt to grant whiteboard permission to audience member
- Handling: Return 400 Bad Request, emit error event to client
- User Feedback: "Only stage participants can receive whiteboard permission"

**Stage Request Not Found**:
- Scenario: Attempt to approve/reject non-existent or already-processed request
- Handling: Return 404 Not Found, emit error event to client
- User Feedback: "Stage request not found or already processed"

### Database Errors

**Connection Failure**:
- Scenario: Database connection lost during operation
- Handling: Return 503 Service Unavailable, log error, attempt reconnection
- User Feedback: "Service temporarily unavailable. Please try again."

**Transaction Failure**:
- Scenario: Database transaction fails during multi-step operation
- Handling: Rollback transaction, return 500 Internal Server Error, log error
- User Feedback: "Operation failed. Please try again."

**Constraint Violation**:
- Scenario: Foreign key or unique constraint violated
- Handling: Return 400 Bad Request, log error
- User Feedback: "Invalid operation. Please refresh and try again."

### Real-time Communication Errors

**SocketIO Disconnection**:
- Scenario: Client loses WebSocket connection
- Handling: Client attempts automatic reconnection, shows connection status indicator
- User Feedback: "Connection lost. Reconnecting..."

**Event Emission Failure**:
- Scenario: SocketIO event fails to emit to room
- Handling: Log error, retry emission once, fall back to HTTP polling if persistent
- User Feedback: No immediate feedback (background retry)

**Stale State**:
- Scenario: Client receives event for outdated room state
- Handling: Client requests full state refresh from server
- User Feedback: "Refreshing room state..."

### WebRTC Errors

**Media Permission Denied**:
- Scenario: User denies camera/microphone access
- Handling: Disable media controls, show permission request prompt
- User Feedback: "Camera/microphone access denied. Please enable in browser settings."

**Media Device Not Found**:
- Scenario: No camera or microphone detected
- Handling: Disable unavailable media controls, allow joining without media
- User Feedback: "No camera/microphone detected. You can still join as audio-only."

**Peer Connection Failure**:
- Scenario: WebRTC peer connection fails to establish
- Handling: Attempt ICE restart, fall back to audio-only if video fails
- User Feedback: "Video connection issues. Trying audio-only..."

### Graceful Degradation

**Demo Mode Restrictions**:
- Scenario: User in demo mode attempts write operations
- Handling: Return 403 Forbidden, show upgrade prompt
- User Feedback: "Demo mode: This feature requires a full account. Sign up to continue."

**Browser Compatibility**:
- Scenario: Browser doesn't support WebRTC or SocketIO
- Handling: Show compatibility warning, offer fallback to text chat only
- User Feedback: "Your browser doesn't support video calls. Please use Chrome, Firefox, or Safari."

## Testing Strategy

### Dual Testing Approach

This feature requires both unit testing and property-based testing for comprehensive coverage:

**Unit Tests**: Focus on specific examples, edge cases, and integration points
- Specific permission scenarios (host removes moderator, moderator tries to remove host)
- Edge cases (stage at capacity, duplicate requests, invalid state transitions)
- Error conditions (database failures, invalid inputs, unauthorized access)
- Integration between components (SocketIO event handling, database updates)

**Property-Based Tests**: Verify universal properties across all inputs
- Role transitions work correctly for any valid participant
- Permission checks return correct results for any user/role combination
- UI rendering includes required elements for any participant state
- State synchronization works for any sequence of operations

Together, unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across the entire input space.

### Property-Based Testing Configuration

**Framework**: Use `pytest` with `hypothesis` library for Python backend testing

**Test Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Each property test must reference its design document property
- Tag format: `# Feature: voice-room-stage-management, Property {number}: {property_text}`

**Example Property Test Structure**:
```python
from hypothesis import given, strategies as st
import pytest

@given(
    room_id=st.integers(min_value=1),
    user_id=st.integers(min_value=1)
)
@pytest.mark.property_test
def test_host_role_assignment_on_creation(room_id, user_id):
    """
    Feature: voice-room-stage-management
    Property 1: Host role assignment on room creation
    
    For any voice room creation, the creating user should be 
    assigned the 'host' role in the room_participants table.
    """
    # Test implementation
    pass
```

### Frontend Testing

**Framework**: Use Jest with `fast-check` library for JavaScript/TypeScript frontend testing

**Test Configuration**:
- Minimum 100 iterations per property test
- Mock SocketIO events and responses
- Test UI rendering with various participant states

**Example Frontend Property Test**:
```javascript
import fc from 'fast-check';

describe('Feature: voice-room-stage-management', () => {
  it('Property 26: Participant profile completeness', () => {
    fc.assert(
      fc.property(
        fc.record({
          id: fc.integer(),
          name: fc.string(),
          role: fc.constantFrom('host', 'moderator', 'stage', 'audience'),
          is_video_on: fc.boolean(),
          is_audio_on: fc.boolean()
        }),
        (participant) => {
          const rendered = renderParticipantCard(participant);
          expect(rendered).toContain(participant.name);
          expect(rendered).toContainProfilePicture();
          expect(rendered).toContainCameraStatus();
          expect(rendered).toContainMicrophoneStatus();
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

### Integration Testing

**Test Scenarios**:
1. Complete stage request flow (raise hand → approve → join stage → remove)
2. Moderator assignment and permission verification
3. Whiteboard permission grant/revoke cycle
4. Multiple simultaneous stage requests
5. Host leaving room (host transfer or room closure)
6. Real-time synchronization across multiple clients

### End-to-End Testing

**Framework**: Use Playwright or Cypress for browser automation

**Test Scenarios**:
1. Multi-user stage management (simulate host, moderator, and visitors)
2. WebRTC media stream handling
3. SocketIO real-time event propagation
4. UI responsiveness to role changes
5. Error handling and recovery

### Performance Testing

**Metrics to Monitor**:
- SocketIO event latency (target: <100ms)
- Database query performance (target: <50ms for permission checks)
- UI rendering time for stage grid (target: <16ms for 60fps)
- Memory usage with maximum stage participants

**Load Testing**:
- Test with maximum stage participants (6+)
- Test with multiple pending stage requests (10+)
- Test with rapid role transitions
- Test with high-frequency whiteboard updates

### Security Testing

**Test Cases**:
1. Verify all permission checks are enforced server-side
2. Test SQL injection prevention in all queries
3. Test XSS prevention in user-generated content (names, messages)
4. Verify CSRF protection on all state-changing operations
5. Test rate limiting on stage requests and permission changes
6. Verify session validation on all SocketIO events

### Regression Testing

**Critical Paths to Protect**:
1. Basic voice room creation and joining
2. Existing WebRTC functionality
3. Existing whiteboard functionality
4. Existing chat functionality
5. User authentication and session management

Each property test should run as part of the CI/CD pipeline to catch regressions early.
