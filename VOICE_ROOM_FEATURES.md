# Voice Room New Features

## Features Added

### 1. Room Type Selection
- **Video Rooms**: Full video + audio support (default)
- **Audio-Only Rooms**: Voice chat only, no video
- Benefits:
  - Audio-only uses less bandwidth
  - Better for pure discussion sessions
  - Reduces data usage for mobile users

### 2. Edit Voice Room
- Host can edit room settings after creation
- Editable fields:
  - Room name
  - Subject
  - Description
  - Room type (video/audio)
  - Public visibility
- Access: Click "✏️ Edit" button in room header (host only)

### 3. Delete Voice Room
- Host can permanently delete a voice room
- Deletes all associated data:
  - Messages
  - Participants
  - Whiteboard snapshots
  - Stage requests
- Access: Edit room page → Danger Zone → Delete button
- Confirmation required before deletion

## How to Use

### Creating a Room with Type Selection
1. Go to Voice Rooms page
2. Click "Create Voice Room"
3. Fill in room details
4. Select Room Type:
   - 🎥 Video Room (Video + Audio)
   - 🎤 Audio Only (Voice Chat)
5. Click "Create Room"

### Editing a Room
1. Join your room (must be host)
2. Click "✏️ Edit" button in header
3. Update any settings
4. Click "Save Changes"

### Deleting a Room
1. Click "✏️ Edit" on your room
2. Scroll to "Danger Zone"
3. Click "Delete Room"
4. Confirm deletion

## Database Changes

Added `room_type` column to `voice_rooms` table:
```sql
ALTER TABLE voice_rooms 
ADD COLUMN room_type ENUM('video', 'audio') DEFAULT 'video' AFTER is_public;
```

## Files Modified

1. **voice_room_routes.py**
   - Added `edit_voice_room` route
   - Added `delete_voice_room` route
   - Updated `create_voice_room` to handle room_type

2. **templates/create_voice_room.html**
   - Added room type dropdown

3. **templates/edit_voice_room.html** (NEW)
   - Edit form for room settings
   - Delete button in danger zone

4. **templates/voice_room.html**
   - Added Edit button for host
   - Added room type badge
   - Updated JavaScript to disable video in audio-only rooms

5. **templates/voice_rooms.html**
   - Added room type icon display

## Technical Details

### Room Type Handling
- Video rooms: Request both video and audio from getUserMedia
- Audio-only rooms: Request only audio, hide video controls
- Room type is enforced on client-side and displayed in UI

### Delete Cascade
Deletion removes records in this order:
1. room_messages
2. room_participants
3. whiteboard_snapshots
4. stage_requests
5. voice_rooms (main table)

### Security
- Only room host can edit/delete
- Demo mode users cannot edit/delete
- Confirmation required for deletion
- Session validation on all routes
