# Implementation Plan: Voice Room Stage Management

## Overview

This implementation plan breaks down the voice room stage management feature into incremental coding tasks. The approach follows a bottom-up strategy: first implementing core backend components (database schema, permission system, managers), then adding SocketIO event handlers, and finally implementing the frontend UI components. Each task builds on previous work and includes testing sub-tasks to validate functionality early.

## Tasks

- [ ] 1. Database schema updates and migrations
  - Create whiteboard_permissions table with proper foreign keys and indexes
  - Modify room_participants table to add 'moderator' to role enum
  - Add database migration script to update existing rooms
  - _Requirements: 3.1, 4.2_

- [ ]* 1.1 Write unit tests for database schema
  - Test table creation and constraints
  - Test foreign key relationships
  - Test unique constraint on whiteboard_permissions
  - _Requirements: 3.1, 4.2_

- [ ] 2. Implement Permission Validator component
  - [ ] 2.1 Create PermissionValidator class in new file permission_validator.py
    - Implement can_manage_stage(user_id, room_id, mysql) method
    - Implement can_grant_whiteboard(user_id, room_id, mysql) method
    - Implement can_remove_participant(user_id, target_user_id, room_id, mysql) method
    - Implement can_end_room(user_id, room_id, mysql) method
    - Implement has_whiteboard_permission(user_id, room_id, mysql) method
    - _Requirements: 1.3, 2.1, 2.5, 3.2, 4.1, 4.4, 11.1-11.8_

  - [ ]* 2.2 Write property test for host permissions
    - **Property 3: Host has all permissions**
    - **Validates: Requirements 1.3**

  - [ ]* 2.3 Write property test for moderator permissions
    - **Property 17: Moderator can manage stage requests**
    - **Property 18: Moderator can manage whiteboard permissions**
    - **Validates: Requirements 11.1, 11.2, 11.4, 11.5**

  - [ ]* 2.4 Write property test for moderator restrictions
    - **Property 19: Moderator cannot end room**
    - **Property 20: Moderator cannot remove host**
    - **Validates: Requirements 11.7, 11.8**

  - [ ]* 2.5 Write unit tests for permission edge cases
    - Test permission checks with invalid user_ids
    - Test permission checks with non-existent rooms
    - Test permission checks with database errors
    - _Requirements: 1.3, 11.1-11.8_

- [ ] 3. Implement Stage Manager component
  - [ ] 3.1 Create StageManager class in new file stage_manager.py
    - Implement add_to_stage(room_id, user_id, mysql) method
    - Implement remove_from_stage(room_id, user_id, mysql) method
    - Implement get_stage_participants(room_id, mysql) method
    - Implement get_available_slots(room_id, mysql) method
    - _Requirements: 2.3, 2.6, 7.1, 7.2, 8.3_

  - [ ]* 3.2 Write property test for stage transitions
    - **Property 5: Stage request approval transitions role**
    - **Property 7: Stage participant removal transitions role**
    - **Property 8: Direct invitation adds to stage**
    - **Validates: Requirements 2.3, 2.6, 8.2, 8.3**

  - [ ]* 3.3 Write unit tests for stage capacity
    - Test adding participant when stage is full
    - Test available slots calculation
    - Test stage participant retrieval
    - _Requirements: 7.2_

- [ ] 4. Implement Role Manager component
  - [ ] 4.1 Create RoleManager class in new file role_manager.py
    - Implement assign_moderator(room_id, user_id, assigned_by, mysql) method
    - Implement revoke_moderator(room_id, user_id, revoked_by, mysql) method
    - Implement get_user_role(room_id, user_id, mysql) method
    - _Requirements: 4.2, 4.5_

  - [ ]* 4.2 Write property test for moderator role transitions
    - **Property 14: Moderator assignment grants permissions**
    - **Property 16: Moderator revocation removes permissions**
    - **Validates: Requirements 4.2, 4.5**

  - [ ]* 4.3 Write unit tests for role validation
    - Test assigning moderator to audience member (should fail)
    - Test assigning moderator by non-host (should fail)
    - Test revoking moderator by non-host (should fail)
    - _Requirements: 4.2, 4.5_

- [ ] 5. Implement Whiteboard Permission Manager component
  - [ ] 5.1 Create WhiteboardPermissionManager class in new file whiteboard_permission_manager.py
    - Implement grant_permission(room_id, user_id, granted_by, mysql) method
    - Implement revoke_permission(room_id, user_id, mysql) method
    - Implement get_permitted_users(room_id, mysql) method
    - Implement auto_revoke_on_stage_leave(room_id, user_id, mysql) method
    - _Requirements: 3.3, 3.4, 10.1_

  - [ ]* 5.2 Write property test for whiteboard permissions
    - **Property 9: Host has default whiteboard permission**
    - **Property 10: Whiteboard permission grant enables editing**
    - **Property 11: Whiteboard permission revocation disables editing**
    - **Property 13: Auto-revoke whiteboard on stage leave**
    - **Validates: Requirements 3.1, 3.3, 3.4**

  - [ ]* 5.3 Write unit tests for whiteboard permission edge cases
    - Test granting permission to audience member (should fail)
    - Test duplicate permission grants
    - Test revoking non-existent permission
    - _Requirements: 3.3, 3.4_

- [ ] 6. Checkpoint - Ensure all backend component tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Update voice room creation to assign host role and whiteboard permission
  - [ ] 7.1 Modify create_voice_room route in voice_room_routes.py
    - Ensure host is added to room_participants with role='host'
    - Create initial whiteboard_permissions record for host
    - _Requirements: 1.1, 3.1_

  - [ ]* 7.2 Write property test for room creation
    - **Property 1: Host role assignment on room creation**
    - **Validates: Requirements 1.1**

  - [ ]* 7.3 Write integration test for room creation flow
    - Test complete room creation with host setup
    - Verify host has all permissions after creation
    - _Requirements: 1.1, 1.3, 3.1_

- [ ] 8. Implement stage request SocketIO event handlers
  - [ ] 8.1 Add stage request handlers to voice_room_routes.py
    - Implement handle_request_stage(data) - creates stage_request record
    - Implement handle_approve_stage_request(data) - uses StageManager.add_to_stage
    - Implement handle_reject_stage_request(data) - updates stage_request status
    - Add permission validation using PermissionValidator
    - Emit appropriate events to room participants
    - _Requirements: 2.2, 2.3, 2.4, 5.2, 12.1_

  - [ ]* 8.2 Write property test for stage request flow
    - **Property 4: Stage request creation and visibility**
    - **Property 6: Stage request rejection removes request**
    - **Validates: Requirements 2.2, 2.4, 5.2, 5.5, 12.1**

  - [ ]* 8.3 Write unit tests for stage request validation
    - Test duplicate stage requests
    - Test approving non-existent request
    - Test unauthorized approval attempts
    - _Requirements: 2.2, 2.3, 2.4_

- [ ] 9. Implement direct stage invitation SocketIO event handlers
  - [ ] 9.1 Add invitation handlers to voice_room_routes.py
    - Implement handle_invite_to_stage(data) - uses StageManager.add_to_stage
    - Add permission validation using PermissionValidator
    - Emit participant_role_changed event to room
    - _Requirements: 2.1, 8.1, 8.2_

  - [ ]* 9.2 Write integration test for invitation flow
    - Test host inviting visitor to stage
    - Test moderator inviting visitor to stage
    - Test visitor attempting to invite (should fail)
    - _Requirements: 2.1, 8.1, 8.2_

- [ ] 10. Implement stage removal SocketIO event handler
  - [ ] 10.1 Add removal handler to voice_room_routes.py
    - Implement handle_remove_from_stage(data) - uses StageManager.remove_from_stage
    - Add permission validation (prevent removing host)
    - Auto-revoke whiteboard permission using WhiteboardPermissionManager
    - Emit participant_role_changed event to room
    - _Requirements: 2.5, 2.6, 11.6_

  - [ ]* 10.2 Write unit tests for removal restrictions
    - Test moderator attempting to remove host (should fail)
    - Test removing participant with whiteboard permission (should auto-revoke)
    - Test unauthorized removal attempts
    - _Requirements: 2.5, 2.6, 11.8_

- [ ] 11. Implement moderator role SocketIO event handlers
  - [ ] 11.1 Add moderator role handlers to voice_room_routes.py
    - Implement handle_assign_moderator(data) - uses RoleManager.assign_moderator
    - Implement handle_revoke_moderator(data) - uses RoleManager.revoke_moderator
    - Add permission validation (host only)
    - Emit participant_role_changed event to room
    - _Requirements: 4.1, 4.2, 4.4, 4.5_

  - [ ]* 11.2 Write integration test for moderator role management
    - Test host assigning moderator to stage participant
    - Test host revoking moderator role
    - Test non-host attempting to assign moderator (should fail)
    - _Requirements: 4.1, 4.2, 4.4, 4.5_

- [ ] 12. Implement whiteboard permission SocketIO event handlers
  - [ ] 12.1 Add whiteboard permission handlers to voice_room_routes.py
    - Implement handle_grant_whiteboard_permission(data) - uses WhiteboardPermissionManager
    - Implement handle_revoke_whiteboard_permission(data) - uses WhiteboardPermissionManager
    - Add permission validation (host or moderator)
    - Emit whiteboard_permission_changed event to room
    - _Requirements: 3.2, 3.3, 3.4, 11.4, 11.5_

  - [ ]* 12.2 Write integration test for whiteboard permission flow
    - Test host granting permission to stage participant
    - Test moderator granting permission
    - Test granting permission to audience member (should fail)
    - _Requirements: 3.2, 3.3, 3.4_

- [ ] 13. Update existing SocketIO handlers for role-based behavior
  - [ ] 13.1 Modify whiteboard event handlers
    - Update handle_whiteboard_draw to check has_whiteboard_permission
    - Update handle_whiteboard_clear to check has_whiteboard_permission
    - Update handle_whiteboard_text to check has_whiteboard_permission
    - Reject events from users without permission
    - _Requirements: 10.1, 10.2, 10.3_

  - [ ]* 13.2 Write property test for whiteboard access control
    - **Property 33: Whiteboard read-only for unpermitted users**
    - **Validates: Requirements 10.2, 10.3**

- [ ] 14. Checkpoint - Ensure all backend integration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 15. Create frontend Stage Grid Renderer component
  - [ ] 15.1 Create StageGridRenderer class in static/js/stage_grid.js
    - Implement renderGrid(participants, maxSlots, userRole) method
    - Implement renderParticipantCard(participant) method
    - Implement renderEmptySlot(slotIndex, canInvite) method
    - Layout: 3 slots left, center content, 3 slots right
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 14.2, 14.3_

  - [ ]* 15.2 Write property test for grid rendering
    - **Property 24: Stage grid displays all stage participants**
    - **Property 25: Minimum stage slots available**
    - **Property 34: Invitation button layout**
    - **Validates: Requirements 7.1, 7.2, 14.2, 14.3**

  - [ ]* 15.3 Write unit tests for participant card rendering
    - Test card with all elements present
    - Test card with missing optional elements
    - Test card with different roles
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 16. Create frontend Permission UI Controller component
  - [ ] 16.1 Create PermissionUIController class in static/js/permission_ui.js
    - Implement updateUIForRole(role) method
    - Implement showStageManagementControls(canManage) method
    - Implement showWhiteboardControls(hasPermission) method
    - Implement showModeratorControls(isHost) method
    - _Requirements: 2.1, 2.5, 3.2, 4.1, 4.4, 5.1, 7.4, 7.5_

  - [ ]* 16.2 Write property test for UI control visibility
    - **Property 28: Empty slot controls for managers**
    - **Property 31: Raise hand button visibility**
    - **Validates: Requirements 5.1, 7.4, 7.5**

- [ ] 17. Create frontend Stage Request Manager component
  - [ ] 17.1 Create StageRequestManager class in static/js/stage_requests.js
    - Implement showRaiseHandButton(isVisitor) method
    - Implement renderPendingRequests(requests, canApprove) method
    - Implement requestStage() method - emits 'request_stage' event
    - Implement approveRequest(requestId) method - emits 'approve_stage_request' event
    - Implement rejectRequest(requestId) method - emits 'reject_stage_request' event
    - _Requirements: 5.1, 5.2, 12.1, 12.2, 12.3, 12.4_

  - [ ]* 17.2 Write property test for stage request UI
    - **Property 29: Stage request display completeness**
    - **Property 32: Raise hand button disabled when pending**
    - **Validates: Requirements 5.3, 12.2, 12.3, 12.4**

- [ ] 18. Create frontend Participant Invitation Modal component
  - [ ] 18.1 Create InvitationModal class in static/js/invitation_modal.js
    - Implement show(availableVisitors) method
    - Implement onSelectVisitor(userId) method - emits 'invite_to_stage' event
    - Add modal HTML template to voice_room.html
    - Style modal with CSS
    - _Requirements: 8.1, 8.2_

  - [ ]* 18.2 Write unit tests for invitation modal
    - Test modal displays visitor list
    - Test visitor selection emits correct event
    - Test modal closes after selection
    - _Requirements: 8.1, 8.2_

- [ ] 19. Update voice room template with stage management UI
  - [ ] 19.1 Modify templates/voice_room.html
    - Add stage grid container with left/right slot areas
    - Add stage request panel for host/moderators
    - Add raise hand button for visitors
    - Add participant context menu for host/moderators (invite, remove, grant whiteboard, assign moderator)
    - Update participant cards to show role badges and whiteboard indicators
    - _Requirements: 1.2, 3.5, 4.3, 5.1, 7.1, 7.4, 9.1-9.6, 12.2-12.4, 14.1-14.5_

  - [ ]* 19.2 Write property test for badge display
    - **Property 2: Host badge display**
    - **Property 15: Moderator badge display**
    - **Property 12: Whiteboard indicator display**
    - **Validates: Requirements 1.2, 3.5, 4.3**

  - [ ]* 19.3 Write property test for participant profile completeness
    - **Property 26: Participant profile completeness**
    - **Property 27: Role badge conditional display**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5**

- [ ] 20. Implement frontend SocketIO event listeners
  - [ ] 20.1 Add event listeners in static/js/voice_room.js
    - Listen for 'participant_role_changed' - update participant role in UI
    - Listen for 'stage_request_created' - add request to pending list
    - Listen for 'stage_request_rejected' - remove request from list
    - Listen for 'whiteboard_permission_changed' - update participant UI
    - Update stage grid when participants change
    - Update permission controls when user role changes
    - _Requirements: 2.3, 2.4, 2.6, 3.3, 3.4, 4.2, 4.5, 8.3, 12.5, 12.6_

  - [ ]* 20.2 Write property test for real-time synchronization
    - **Property 30: Stage request synchronization**
    - **Validates: Requirements 12.5, 12.6**

  - [ ]* 20.3 Write integration tests for event handling
    - Test participant role change updates UI
    - Test stage request creation shows in pending list
    - Test whiteboard permission change updates controls
    - _Requirements: 2.3, 2.4, 3.3, 3.4_

- [ ] 21. Implement media control state preservation
  - [ ] 21.1 Update stage transition handlers
    - Preserve is_video_on and is_audio_on when moving to stage
    - Preserve media state when removing from stage
    - Update UI to reflect preserved state
    - _Requirements: 6.5_

  - [ ]* 21.2 Write property test for media state preservation
    - **Property 23: Media state preserved on stage transition**
    - **Validates: Requirements 6.5**

- [ ] 22. Add CSS styling for stage management UI
  - [ ] 22.1 Create static/css/stage_management.css
    - Style stage grid layout (3 left + center + 3 right)
    - Style participant cards with badges and indicators
    - Style "+" buttons for empty slots
    - Style stage request panel
    - Style invitation modal
    - Style role badges (Host, Moderator)
    - Style whiteboard permission indicator
    - Ensure responsive design for mobile
    - _Requirements: 1.2, 3.5, 4.3, 7.6, 14.1-14.6_

  - [ ]* 22.2 Write visual regression tests
    - Test stage grid layout with various participant counts
    - Test participant card appearance with different roles
    - Test responsive behavior on mobile screens
    - _Requirements: 7.6, 14.1-14.6_

- [ ] 23. Implement error handling and user feedback
  - [ ] 23.1 Add error handlers to SocketIO events
    - Handle permission denied errors with user-friendly messages
    - Handle stage capacity errors
    - Handle invalid state transition errors
    - Handle database errors with retry logic
    - _Requirements: All requirements (error handling)_

  - [ ]* 23.2 Write unit tests for error scenarios
    - Test unauthorized action attempts
    - Test invalid state transitions
    - Test database failure handling
    - _Requirements: All requirements (error handling)_

- [ ] 24. Update join_voice_room route to include role and permission data
  - [ ] 24.1 Modify join_voice_room route in voice_room_routes.py
    - Include user's role in room context
    - Include whiteboard permission status
    - Include list of pending stage requests (if host/moderator)
    - Include list of available visitors (if host/moderator)
    - _Requirements: 1.3, 3.1, 5.1, 12.1_

  - [ ]* 24.2 Write integration test for room join with permissions
    - Test host joins with all permissions
    - Test moderator joins with correct permissions
    - Test visitor joins with limited permissions
    - _Requirements: 1.3, 11.1-11.8_

- [ ] 25. Checkpoint - Ensure all frontend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 26. Add demo mode support for stage management
  - [ ] 26.1 Update demo data in app.py
    - Add demo moderator participants
    - Add demo stage requests
    - Add demo whiteboard permissions
    - _Requirements: All requirements (demo mode)_

  - [ ]* 26.2 Write unit tests for demo mode
    - Test demo mode shows stage management UI
    - Test demo mode prevents write operations
    - Test demo mode shows appropriate warnings
    - _Requirements: All requirements (demo mode)_

- [ ] 27. Write end-to-end integration tests
  - [ ]* 27.1 Test complete stage request flow
    - Visitor raises hand → Host approves → Visitor joins stage → Host removes
    - _Requirements: 2.2, 2.3, 2.6, 5.2_

  - [ ]* 27.2 Test complete moderator flow
    - Host assigns moderator → Moderator manages stage → Host revokes moderator
    - _Requirements: 4.2, 4.5, 11.1-11.6_

  - [ ]* 27.3 Test complete whiteboard permission flow
    - Host grants permission → Participant edits whiteboard → Host revokes permission
    - _Requirements: 3.3, 3.4, 10.1-10.5_

  - [ ]* 27.4 Test multi-user synchronization
    - Multiple users see same stage state
    - Stage requests appear for all hosts/moderators
    - Role changes propagate to all participants
    - _Requirements: 12.5, 12.6_

- [ ] 28. Performance optimization and testing
  - [ ]* 28.1 Optimize database queries
    - Add indexes for permission checks
    - Optimize participant list queries
    - Cache frequently accessed data
    - _Requirements: All requirements (performance)_

  - [ ]* 28.2 Test with maximum stage participants
    - Test with 6+ stage participants
    - Test with 10+ pending stage requests
    - Measure SocketIO event latency
    - Measure UI rendering performance
    - _Requirements: 7.2_

- [ ] 29. Security audit and testing
  - [ ]* 29.1 Verify server-side permission enforcement
    - Test all SocketIO events validate permissions
    - Test SQL injection prevention
    - Test XSS prevention in user content
    - Test CSRF protection
    - _Requirements: All requirements (security)_

  - [ ]* 29.2 Add rate limiting
    - Limit stage request frequency per user
    - Limit permission change frequency
    - Limit role assignment frequency
    - _Requirements: All requirements (security)_

- [ ] 30. Documentation and deployment
  - [ ] 30.1 Update project documentation
    - Document new database tables and schema
    - Document new API endpoints and SocketIO events
    - Document permission system architecture
    - Add usage guide for stage management features
    - _Requirements: All requirements (documentation)_

  - [ ] 30.2 Create database migration guide
    - Document steps to update existing databases
    - Provide rollback procedures
    - Test migration on staging environment
    - _Requirements: All requirements (deployment)_

- [ ] 31. Final checkpoint - Complete system test
  - Run all unit tests, property tests, and integration tests
  - Verify all requirements are met
  - Test on multiple browsers (Chrome, Firefox, Safari)
  - Test on mobile devices
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional testing tasks and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties across all inputs
- Unit tests validate specific examples, edge cases, and error conditions
- Integration tests validate component interactions and end-to-end flows
- The implementation follows a bottom-up approach: backend components → SocketIO handlers → frontend components → integration
- All permission checks must be enforced server-side for security
- Real-time synchronization is critical for multi-user experience
- Demo mode support ensures feature can be previewed without database
