# Voice Room Feature - Requirements Document

## 1. Feature Overview

Add a Voice Room feature to StudyMate that enables live doubt-clearing sessions with video calls, whiteboard collaboration, and audience participation.

## 2. User Stories

### 2.1 As a Student (Host)
- I want to create a voice room for doubt clearing
- I want to share my screen and use a whiteboard
- I want to invite up to 6 people on stage for discussion
- I want to see comments from audience members
- I want to record sessions for later review

### 2.2 As a Student (Stage Participant)
- I want to join the stage (max 6 people)
- I want to enable my video/audio
- I want to share my screen
- I want to draw on the shared whiteboard
- I want to ask questions via voice

### 2.3 As a Student (Audience)
- I want to join voice rooms as a viewer
- I want to comment and ask questions via text
- I want to request to join the stage
- I want to see the whiteboard and video streams
- I want to react with emojis

## 3. Acceptance Criteria

### 3.1 Voice Room Creation
- Users can create a voice room with title, subject, and description
- Room creator becomes the host automatically
- Room has a unique shareable link
- Room can be public or group-specific

### 3.2 Stage Management
- Maximum 6 people on stage (including host)
- Host can approve/remove stage participants
- Stage participants have video/audio controls
- Stage participants can share screen
- Stage participants can draw on whiteboard

### 3.3 Audience Features
- Unlimited audience members can join
- Audience can view all video streams
- Audience can post text comments in real-time
- Audience can request to join stage
- Audience can react with emojis

### 3.4 Whiteboard Features
- Shared whiteboard visible to all
- Drawing tools: pen, eraser, shapes, text
- Multiple colors and sizes
- Clear board option (host only)
- Save whiteboard as image

### 3.5 Video/Audio Features
- WebRTC-based video calls
- Mute/unmute audio controls
- Enable/disable video controls
- Screen sharing capability
- Picture-in-picture mode

### 3.6 Chat/Comments
- Real-time text chat for audience
- Emoji reactions
- Pinned messages (host only)
- Chat moderation (host can delete)

## 4. Technical Requirements

### 4.1 Backend
- WebRTC signaling server
- Socket.IO for real-time communication
- Room state management
- User permissions handling

### 4.2 Frontend
- WebRTC peer connections
- Canvas-based whiteboard
- Video grid layout
- Real-time chat UI
- Responsive design

### 4.3 Database
- Voice rooms table
- Room participants table
- Chat messages table
- Whiteboard snapshots table

## 5. Constraints

- Maximum 6 people on stage
- Unlimited audience members
- WebRTC requires HTTPS in production
- Browser compatibility: Chrome, Firefox, Safari, Edge

## 6. Future Enhancements

- Session recording
- AI-powered doubt suggestions
- Breakout rooms
- Polls and quizzes
- Hand raise queue system
