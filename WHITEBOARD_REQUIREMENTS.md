# Whiteboard Requirements & Implementation Plan

## Current Issues
1. ❌ Whiteboard is stuck - cannot drag/move
2. ❌ Maximize button not working
3. ❌ No text tool for typing

## Required Features

### 1. Freely Movable Whiteboard
**Requirement:** User should be able to click the header and drag the whiteboard anywhere on the screen

**Implementation:**
- Remove all CSS positioning conflicts
- Use simple drag logic with offsetTop/offsetLeft
- Ensure no CSS rules override JavaScript positioning
- Test: Should move smoothly when dragging header

### 2. Working Maximize Button
**Requirement:** Click maximize to expand whiteboard to full screen, click again to restore

**Implementation:**
- Save original position before maximizing
- Set to full screen (20px margins)
- Restore original position when un-maximizing
- Update icon: ⛶ (normal) ↔ ◱ (maximized)

### 3. Text Tool (Notepad Feature)
**Requirement:** Add a text tool that allows typing text on the whiteboard

**Features Needed:**
- Text tool button in toolbar (🔤 or T icon)
- Click on canvas to place text cursor
- Type text from keyboard
- Text appears on whiteboard
- Can change text color
- Can change text size
- Text syncs to other participants

**Implementation Steps:**
1. Add text tool button to toolbar
2. On text tool click, change cursor to text cursor
3. On canvas click, show input field or capture keyboard
4. Render text on canvas at click position
5. Emit text to other users via Socket.IO

## Priority Order
1. **Fix dragging** (CRITICAL - currently broken)
2. **Fix maximize** (HIGH - user requested)
3. **Add text tool** (HIGH - user requested for teaching)

## Technical Approach

### For Dragging
Use the simplest possible approach:
```javascript
let isDragging = false;
let currentX, currentY, initialX, initialY;

header.addEventListener('mousedown', (e) => {
    isDragging = true;
    initialX = e.clientX - element.offsetLeft;
    initialY = e.clientY - element.offsetTop;
});

document.addEventListener('mousemove', (e) => {
    if (isDragging) {
        currentX = e.clientX - initialX;
        currentY = e.clientY - initialY;
        element.style.left = currentX + 'px';
        element.style.top = currentY + 'px';
    }
});

document.addEventListener('mouseup', () => {
    isDragging = false;
});
```

### For Text Tool
```javascript
let textMode = false;
let textColor = '#000000';
let textSize = 16;

canvas.addEventListener('click', (e) => {
    if (textMode) {
        const x = e.offsetX;
        const y = e.offsetY;
        const text = prompt('Enter text:');
        if (text) {
            ctx.font = `${textSize}px Arial`;
            ctx.fillStyle = textColor;
            ctx.fillText(text, x, y);
            // Emit to other users
            socket.emit('whiteboard_text', {
                room_code: roomCode,
                x, y, text, color: textColor, size: textSize
            });
        }
    }
});
```

## User Experience Goals
- **Easy to move:** Just grab and drag anywhere
- **Easy to resize:** Drag corner or use maximize
- **Easy to type:** Click text tool, click canvas, type
- **Visual feedback:** Cursor changes, buttons highlight
- **Smooth operation:** No lag or stuttering

## Testing Checklist
- [ ] Can drag whiteboard to top-left corner
- [ ] Can drag whiteboard to bottom-right corner
- [ ] Can drag whiteboard to center
- [ ] Maximize expands to full screen
- [ ] Maximize again restores original position
- [ ] Text tool button activates text mode
- [ ] Can click and type text on canvas
- [ ] Text appears in chosen color
- [ ] Text appears in chosen size
- [ ] Other users see the text

## Next Steps
1. Fix CSS positioning completely
2. Implement proven drag code
3. Test dragging thoroughly
4. Implement maximize with position save/restore
5. Add text tool to toolbar
6. Implement text input on canvas
7. Add Socket.IO text events
8. Test all features together
