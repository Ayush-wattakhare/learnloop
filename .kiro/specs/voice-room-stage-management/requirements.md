# Requirements Document

## Introduction

The Voice Room Stage Management feature enables structured participation in voice rooms through a stage-based system. The host controls who can actively participate on stage, manages permissions for whiteboard access, and can delegate moderation responsibilities. This creates an organized environment for presentations, discussions, and collaborative sessions where audience members can request to join the stage while maintaining clear role hierarchies.

## Glossary

- **Host**: The user who created the voice room and has full control over all room operations
- **Moderator**: A stage participant granted elevated permissions by the host to help manage the room
- **Stage_Participant**: A user who has been approved to join the stage and can use audio/video
- **Visitor**: A user in the room who is not on stage (audience member)
- **Stage_Slot**: A position in the video grid that can be occupied by a stage participant
- **Whiteboard_Permission**: Access right that allows a stage participant to edit the whiteboard
- **Stage_Request**: A request from a visitor to join the stage (raise hand)
- **Video_Grid**: The UI component displaying all stage participants
- **Role_Badge**: Visual indicator showing a user's role (Host, Moderator)

## Requirements

### Requirement 1: Host Role and Identification

**User Story:** As a voice room creator, I want to be automatically designated as the host with clear visual identification, so that participants know who is in charge of the room.

#### Acceptance Criteria

1. WHEN a user creates a voice room, THE System SHALL assign that user the Host role
2. WHEN displaying the Host's profile, THE System SHALL show a "Host" badge alongside their name
3. THE Host SHALL have all permissions available in the room by default
4. WHEN the Host leaves the room, THE System SHALL handle host transfer or room closure according to room policies

### Requirement 2: Host Stage Management Permissions

**User Story:** As a host, I want to control who joins the stage, so that I can manage the flow of the session and maintain order.

#### Acceptance Criteria

1. WHEN the Host selects a visitor, THE System SHALL provide an option to invite them directly to the stage
2. WHEN a visitor submits a stage request, THE System SHALL present the request to the Host with approve and reject options
3. WHEN the Host approves a stage request, THE System SHALL add the visitor to the stage as a Stage_Participant
4. WHEN the Host rejects a stage request, THE System SHALL remove the request and notify the visitor
5. WHEN the Host selects a Stage_Participant, THE System SHALL provide an option to remove them from the stage
6. WHEN the Host removes a Stage_Participant, THE System SHALL move them back to visitor status

### Requirement 3: Host Whiteboard Permission Management

**User Story:** As a host, I want to grant whiteboard access to specific stage participants, so that I can enable collaboration while maintaining control.

#### Acceptance Criteria

1. WHEN a voice room is created, THE System SHALL grant Whiteboard_Permission to the Host by default
2. WHEN the Host selects a Stage_Participant, THE System SHALL provide an option to grant Whiteboard_Permission
3. WHEN the Host grants Whiteboard_Permission to a Stage_Participant, THE System SHALL enable whiteboard editing for that participant
4. WHEN the Host revokes Whiteboard_Permission from a Stage_Participant, THE System SHALL disable whiteboard editing for that participant
5. WHEN displaying a Stage_Participant profile, THE System SHALL show a visual indicator if they have Whiteboard_Permission

### Requirement 4: Host Moderator Assignment

**User Story:** As a host, I want to assign moderator roles to trusted stage participants, so that I can delegate management responsibilities.

#### Acceptance Criteria

1. WHEN the Host selects a Stage_Participant, THE System SHALL provide an option to assign the Moderator role
2. WHEN the Host assigns the Moderator role, THE System SHALL grant that participant moderator permissions
3. WHEN displaying a Moderator's profile, THE System SHALL show a "Moderator" badge alongside their name
4. WHEN the Host selects a Moderator, THE System SHALL provide an option to revoke the Moderator role
5. WHEN the Host revokes the Moderator role, THE System SHALL remove moderator permissions from that participant

### Requirement 5: Visitor Stage Request System

**User Story:** As a visitor, I want to request joining the stage by raising my hand, so that I can participate actively when the host approves.

#### Acceptance Criteria

1. WHEN a Visitor is in the room, THE System SHALL display a "Raise Hand" button
2. WHEN a Visitor clicks "Raise Hand", THE System SHALL create a Stage_Request and notify the Host and Moderators
3. WHEN a Visitor has a pending Stage_Request, THE System SHALL disable the "Raise Hand" button
4. WHEN a Stage_Request is approved, THE System SHALL add the Visitor to the stage as a Stage_Participant
5. WHEN a Stage_Request is rejected, THE System SHALL remove the request and re-enable the "Raise Hand" button

### Requirement 6: Visitor Media Controls

**User Story:** As a visitor, I want to control my own camera and microphone, so that I can prepare before joining the stage.

#### Acceptance Criteria

1. WHEN a Visitor is in the room, THE System SHALL provide camera toggle controls
2. WHEN a Visitor toggles their camera, THE System SHALL enable or disable their video feed accordingly
3. WHEN a Visitor is in the room, THE System SHALL provide microphone toggle controls
4. WHEN a Visitor toggles their microphone, THE System SHALL mute or unmute their audio accordingly
5. WHEN a Visitor joins the stage, THE System SHALL preserve their camera and microphone settings

### Requirement 7: Stage Participant Slot System

**User Story:** As a user, I want to see all stage participants in a clear video grid layout, so that I can follow who is actively participating.

#### Acceptance Criteria

1. THE System SHALL display a Video_Grid showing all Stage_Participants
2. THE System SHALL provide at least 6 Stage_Slots in the Video_Grid
3. WHEN a Stage_Slot is occupied, THE System SHALL display the participant's profile with camera feed
4. WHEN a Stage_Slot is empty and the user is Host or Moderator, THE System SHALL display a "+" button
5. WHEN a Stage_Slot is empty and the user is a Visitor, THE System SHALL display an empty slot without controls
6. THE System SHALL arrange Stage_Slots with 3 positions on the left side and 3 positions on the right side of the Video_Grid

### Requirement 8: Stage Invitation Interface

**User Story:** As a host or moderator, I want to click the "+" button to invite specific users to the stage, so that I can quickly add participants.

#### Acceptance Criteria

1. WHEN a Host or Moderator clicks a "+" button in an empty Stage_Slot, THE System SHALL display a list of available Visitors
2. WHEN a Host or Moderator selects a Visitor from the list, THE System SHALL send a stage invitation to that Visitor
3. WHEN a Visitor receives a stage invitation, THE System SHALL add them to the stage as a Stage_Participant
4. WHEN a Stage_Slot becomes occupied, THE System SHALL remove the "+" button from that slot

### Requirement 9: Stage Participant Profile Display

**User Story:** As a user, I want to see detailed information about each stage participant, so that I can identify them and understand their status.

#### Acceptance Criteria

1. WHEN displaying a Stage_Participant in the Video_Grid, THE System SHALL show their profile picture
2. WHEN displaying a Stage_Participant in the Video_Grid, THE System SHALL show their name
3. WHEN displaying a Stage_Participant in the Video_Grid, THE System SHALL show their Role_Badge if they are Host or Moderator
4. WHEN displaying a Stage_Participant in the Video_Grid, THE System SHALL show their camera status (on/off)
5. WHEN displaying a Stage_Participant in the Video_Grid, THE System SHALL show their microphone status (muted/unmuted)
6. WHEN a Stage_Participant has Whiteboard_Permission, THE System SHALL display a whiteboard indicator on their profile

### Requirement 10: Whiteboard Access Control

**User Story:** As a stage participant, I want to know if I can edit the whiteboard, so that I understand my collaboration capabilities.

#### Acceptance Criteria

1. WHEN a Stage_Participant has Whiteboard_Permission, THE System SHALL enable whiteboard editing controls for that participant
2. WHEN a Stage_Participant does not have Whiteboard_Permission, THE System SHALL display the whiteboard in read-only mode
3. WHEN a Visitor views the whiteboard, THE System SHALL display it in read-only mode
4. WHEN Whiteboard_Permission is granted to a Stage_Participant, THE System SHALL immediately enable their whiteboard controls
5. WHEN Whiteboard_Permission is revoked from a Stage_Participant, THE System SHALL immediately disable their whiteboard controls

### Requirement 11: Moderator Permissions

**User Story:** As a moderator, I want to have most host permissions to help manage the room, so that I can assist with room operations.

#### Acceptance Criteria

1. WHEN a user has the Moderator role, THE System SHALL allow them to approve Stage_Requests
2. WHEN a user has the Moderator role, THE System SHALL allow them to reject Stage_Requests
3. WHEN a user has the Moderator role, THE System SHALL allow them to invite Visitors to the stage
4. WHEN a user has the Moderator role, THE System SHALL allow them to grant Whiteboard_Permission to Stage_Participants
5. WHEN a user has the Moderator role, THE System SHALL allow them to revoke Whiteboard_Permission from Stage_Participants
6. WHEN a user has the Moderator role, THE System SHALL allow them to remove Stage_Participants from the stage
7. WHEN a user has the Moderator role, THE System SHALL prevent them from ending the room
8. WHEN a user has the Moderator role, THE System SHALL prevent them from removing the Host from the stage

### Requirement 12: Stage Request Management Interface

**User Story:** As a host or moderator, I want to see pending stage requests with clear approve/reject options, so that I can efficiently manage who joins the stage.

#### Acceptance Criteria

1. WHEN a Stage_Request is pending, THE System SHALL display it to the Host and all Moderators
2. WHEN displaying a Stage_Request, THE System SHALL show the requesting Visitor's name and profile
3. WHEN displaying a Stage_Request, THE System SHALL provide an "Approve" button
4. WHEN displaying a Stage_Request, THE System SHALL provide a "Reject" button
5. WHEN a Host or Moderator approves a Stage_Request, THE System SHALL remove it from the pending list for all Host and Moderators
6. WHEN a Host or Moderator rejects a Stage_Request, THE System SHALL remove it from the pending list for all Host and Moderators

### Requirement 13: Stage Participant Media Controls

**User Story:** As a stage participant, I want to control my camera and microphone while on stage, so that I can manage my presence during the session.

#### Acceptance Criteria

1. WHEN a Stage_Participant is on stage, THE System SHALL provide camera toggle controls
2. WHEN a Stage_Participant toggles their camera, THE System SHALL enable or disable their video feed accordingly
3. WHEN a Stage_Participant is on stage, THE System SHALL provide microphone toggle controls
4. WHEN a Stage_Participant toggles their microphone, THE System SHALL mute or unmute their audio accordingly
5. WHEN a Stage_Participant's camera or microphone status changes, THE System SHALL update their profile display in real-time

### Requirement 14: UI Layout and Organization

**User Story:** As a user, I want a clear and organized interface layout, so that I can easily navigate the voice room features.

#### Acceptance Criteria

1. THE System SHALL display the Video_Grid in the center of the interface
2. THE System SHALL display 3 "+" buttons vertically on the left side of the Video_Grid for Host and Moderators
3. THE System SHALL display 3 "+" buttons vertically on the right side of the Video_Grid for Host and Moderators
4. THE System SHALL display whiteboard and video control buttons in the bottom control bar
5. WHEN a user is a Visitor, THE System SHALL display a "Raise Hand" button in the control bar
6. THE System SHALL maintain consistent spacing and alignment for all Stage_Slots in the Video_Grid
