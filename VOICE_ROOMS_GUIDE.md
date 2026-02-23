# 🎙️ Voice Rooms Feature Guide

## Overview

Voice Rooms is a powerful live collaboration feature that enables students to conduct doubt-clearing sessions with video calls, shared whiteboard, and real-time chat.

---

## ✨ Key Features

### 1. Live Video Calls
- **Up to 6 people on stage** with video and audio
- **Unlimited audience members** can watch and participate via chat
- **Host controls** for managing stage participants
- **Video/audio toggle** for each participant

### 2. Shared Whiteboard
- **Real-time collaborative drawing**
- **Multiple tools**: Pen, eraser, shapes, text
- **Color picker** and size adjustment
- **Save whiteboard** as image
- **Clear board** (host only)

### 3. Live Chat & Comments
- **Real-time text chat** for all participants
- **Emoji reactions** for quick responses
- **Message history** preserved during session
- **System notifications** for joins/leaves

### 4. Stage Management
- **Request to join stage** from audience
- **Host approval system** for stage requests
- **Automatic role management** (host, stage, audience)
- **Stage participant limit** enforcement (max 6)

### 5. Screen Sharing
- **Share your screen** with all participants
- **Present slides or code** during sessions
- **Switch between camera and screen**

---

## 🚀 How to Use

### Creating a Voice Room

1. **Navigate to Voice Rooms**
   - Click "🎙️ Voice Rooms" in the navigation menu

2. **Click "Create Voice Room"**
   - Fill in room details:
     - Room Name (e.g., "Python Doubt Clearing")
     - Subject (e.g., "Python Programming")
     - Description (optional)
     - Link to Group (optional)
     - Public/Private setting

3. **Click "Create Room"**
   - You'll be automatically added as the host
   - Share the room code with others

### Joining a Voice Room

1. **Browse Active Rooms**
   - View all live voice rooms on the Voice Rooms page
   - See room details, host, and participant count

2. **Click "Join Room"**
   - You'll enter as an audience member
   - Can view video streams and participate in chat

3. **Request to Join Stage** (Optional)
   - Click "Request to Join Stage" button
   - Wait for host approval
   - Once approved, enable your video/audio

### As a Host

**Managing Participants:**
- Approve/reject stage requests
- Remove participants from stage
- End the room for everyone

**Whiteboard Controls:**
- Draw and annotate
- Clear the whiteboard
- Save whiteboard snapshots

**Room Controls:**
- End room button
- Manage stage participants
- Pin important messages

### As a Stage Participant

**Media Controls:**
- Toggle video on/off (📹)
- Toggle audio on/off (🎤)
- Share screen (🖥️)

**Whiteboard:**
- Draw collaboratively
- Use different colors and tools
- Contribute to explanations

**Chat:**
- Send messages
- React with emojis
- Ask questions

### As an Audience Member

**Viewing:**
- Watch all video streams
- See whiteboard in real-time
- Follow the discussion

**Participating:**
- Send chat messages
- Ask questions via text
- Request to join stage
- React with emojis

---

## 🎨 Interface Layout

### Main Content Area
```
┌─────────────────────────────────────────┐
│  Room Header (Name, Status, Controls)   │
├─────────────────────────────────────────┤
│                                         │
│         Video Grid (Stage)              │
│     [Video] [Video] [Video]             │
│     [Video] [Video] [Video]             │
│                                         │
├─────────────────────────────────────────┤
│         Whiteboard (Toggle)             │
│     [Drawing Canvas with Tools]         │
├─────────────────────────────────────────┤
│  Media Controls (Video, Audio, Share)   │
└─────────────────────────────────────────┘
```

### Sidebar
```
┌─────────────────────┐
│   Participants      │
│  👤 Host            │
│  👤 Stage (3)       │
│  👤 Audience (12)   │
│                     │
│  [Request Stage]    │
├─────────────────────┤
│   Chat              │
│  💬 Messages...     │
│  💬 Messages...     │
│                     │
│  [Type message...]  │
└─────────────────────┘
```

---

## 🎯 Use Cases

### 1. Doubt Clearing Sessions
- **Host**: Teacher or senior student
- **Stage**: Students with doubts (up to 6)
- **Audience**: Other students watching and learning
- **Tools**: Whiteboard for explanations, video for face-to-face

### 2. Group Study Sessions
- **Host**: Study group leader
- **Stage**: Active participants discussing
- **Audience**: Members listening and taking notes
- **Tools**: Screen sharing for presentations

### 3. Exam Preparation
- **Host**: Subject expert
- **Stage**: Students asking questions
- **Audience**: Batch mates preparing together
- **Tools**: Whiteboard for problem solving

### 4. Project Discussions
- **Host**: Project lead
- **Stage**: Team members
- **Audience**: Stakeholders or observers
- **Tools**: Screen sharing for code/designs

---

## 🔧 Technical Details

### Browser Requirements
- **Chrome** 90+ (Recommended)
- **Firefox** 88+
- **Safari** 14+
- **Edge** 90+

### Permissions Required
- **Camera access** (for video)
- **Microphone access** (for audio)
- **Screen sharing** (optional)

### Network Requirements
- **Stable internet connection**
- **Minimum 1 Mbps** upload/download
- **Recommended 5 Mbps** for HD video

### Supported Features by Browser

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Video Calls | ✅ | ✅ | ✅ | ✅ |
| Screen Share | ✅ | ✅ | ✅ | ✅ |
| Whiteboard | ✅ | ✅ | ✅ | ✅ |
| Chat | ✅ | ✅ | ✅ | ✅ |

---

## 📊 Room Roles & Permissions

### Host
- ✅ Create and end room
- ✅ Approve stage requests
- ✅ Remove participants from stage
- ✅ Clear whiteboard
- ✅ Pin messages
- ✅ Full video/audio/screen share
- ✅ Whiteboard access

### Stage Participant
- ✅ Video/audio enabled
- ✅ Screen sharing
- ✅ Whiteboard access
- ✅ Chat messaging
- ❌ Cannot remove others
- ❌ Cannot end room

### Audience
- ✅ View all streams
- ✅ Chat messaging
- ✅ Request stage access
- ❌ No video/audio (until on stage)
- ❌ No whiteboard access
- ❌ Cannot manage room

---

## 🎓 Best Practices

### For Hosts

1. **Prepare in Advance**
   - Test your camera and microphone
   - Prepare topics to cover
   - Have materials ready to share

2. **Manage Stage Effectively**
   - Limit stage to active participants
   - Rotate participants if many requests
   - Keep stage organized (max 6)

3. **Use Whiteboard Wisely**
   - Draw clear diagrams
   - Use different colors for clarity
   - Save important snapshots

4. **Engage Audience**
   - Monitor chat for questions
   - Acknowledge comments
   - Invite participation

### For Participants

1. **Be Prepared**
   - Test your equipment before joining
   - Have questions ready
   - Take notes during session

2. **Respect Others**
   - Mute when not speaking
   - Don't interrupt
   - Use chat for quick questions

3. **Participate Actively**
   - Ask questions
   - Share insights
   - Help others in chat

---

## 🐛 Troubleshooting

### Video/Audio Not Working

**Problem**: Camera or microphone not detected

**Solutions**:
1. Check browser permissions
2. Ensure no other app is using camera/mic
3. Refresh the page
4. Try a different browser

### Can't Join Stage

**Problem**: Request not approved

**Solutions**:
1. Wait for host approval
2. Send a chat message to host
3. Check if stage is full (6 max)

### Whiteboard Not Syncing

**Problem**: Drawings not appearing for others

**Solutions**:
1. Check internet connection
2. Refresh the page
3. Try drawing again
4. Contact host to clear and restart

### Poor Video Quality

**Problem**: Laggy or pixelated video

**Solutions**:
1. Check internet speed
2. Close other bandwidth-heavy apps
3. Disable video and use audio only
4. Move closer to WiFi router

---

## 📱 Mobile Support

Voice Rooms work on mobile devices with some limitations:

**Supported**:
- ✅ Joining rooms
- ✅ Viewing video streams
- ✅ Chat messaging
- ✅ Audio participation

**Limited**:
- ⚠️ Whiteboard (view only, drawing difficult)
- ⚠️ Screen sharing (not all browsers)
- ⚠️ Multiple videos (may be laggy)

**Recommended**: Use desktop/laptop for best experience

---

## 🔒 Privacy & Security

### Data Protection
- Video/audio streams are peer-to-peer
- Chat messages stored in database
- Whiteboard snapshots saved optionally
- Room codes are unique and secure

### Privacy Controls
- Public/private room options
- Group-specific rooms
- Host controls for participants
- End room anytime

---

## 📈 Future Enhancements

### Planned Features
- [ ] Session recording
- [ ] Breakout rooms
- [ ] Polls and quizzes
- [ ] Hand raise queue
- [ ] AI-powered transcription
- [ ] Virtual backgrounds
- [ ] Noise cancellation
- [ ] Picture-in-picture mode

---

## 💡 Tips & Tricks

1. **Use Keyboard Shortcuts**
   - Space: Toggle mute
   - V: Toggle video
   - Enter: Send chat message

2. **Optimize Performance**
   - Close unnecessary tabs
   - Use wired internet if possible
   - Disable HD video if laggy

3. **Better Collaboration**
   - Use whiteboard for visual explanations
   - Share screen for code/documents
   - Pin important messages

4. **Effective Sessions**
   - Set clear agenda
   - Time-box discussions
   - Summarize key points
   - Save whiteboard snapshots

---

## 📞 Support

If you encounter issues:

1. Check this guide first
2. Try troubleshooting steps
3. Refresh the page
4. Contact support with:
   - Browser and version
   - Error messages
   - Steps to reproduce

---

**Happy Learning! 🎓✨**

*Voice Rooms - Bringing students together for collaborative learning*
