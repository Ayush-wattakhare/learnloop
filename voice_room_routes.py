"""
Voice Room Routes for LearnLoop
Handles voice room creation, management, and real-time features
"""

from flask import render_template, request, redirect, session, flash, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
import secrets
import string

def generate_room_code():
    """Generate unique 8-character room code"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def register_voice_room_routes(app, mysql, socketio):
    """Register all voice room routes"""
    
    # ─── CREATE VOICE ROOM ────────────────────────────────────────
    @app.route('/voice-rooms')
    def voice_rooms_list():
        """List all active voice rooms"""
        if 'user_id' not in session:
            flash('Please login first!', 'warning')
            return redirect('/login')
        
        if session.get('demo_mode'):
            # Demo data
            rooms = [
                (1, '🐍 Python Doubt Clearing', 'Python Programming', 'Live session for Python doubts', 1, 'Demo User', True, 3, 'ABC12345'),
                (2, '🗄️ DBMS Q&A Session', 'Database Management', 'SQL queries and normalization help', 2, 'Priya Singh', True, 5, 'XYZ67890'),
            ]
        else:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT vr.*, u.name as host_name,
                       (SELECT COUNT(*) FROM room_participants WHERE room_id=vr.id AND role='stage') as stage_count
                FROM voice_rooms vr
                JOIN users u ON vr.host_id = u.id
                WHERE vr.is_active = TRUE
                ORDER BY vr.created_at DESC
            """)
            rooms = cur.fetchall()
        
        return render_template('voice_rooms.html', rooms=rooms)
    
    # ─── CREATE NEW VOICE ROOM ───────────────────────────────────
    @app.route('/create-voice-room', methods=['GET', 'POST'])
    def create_voice_room():
        """Create a new voice room"""
        if 'user_id' not in session:
            flash('Please login first!', 'warning')
            return redirect('/login')
        
        if session.get('demo_mode'):
            flash('⚠️ Demo Mode: Voice room creation is disabled. Sign up to create real rooms!', 'warning')
            return redirect('/voice-rooms')
        
        if request.method == 'POST':
            try:
                room_name = request.form['room_name']
                subject = request.form['subject']
                description = request.form.get('description', '')
                room_type = request.form.get('room_type', 'video')
                is_public = request.form.get('is_public', 'false') == 'true'
                group_id = request.form.get('group_id', None)
                # Convert empty string to None for group_id
                if group_id == '' or group_id == 'None':
                    group_id = None
                
                room_code = generate_room_code()
                
                cur = mysql.connection.cursor()
                cur.execute("""
                    INSERT INTO voice_rooms (room_name, subject, description, host_id, is_public, room_type, room_code, group_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (room_name, subject, description, session['user_id'], is_public, room_type, room_code, group_id))
                mysql.connection.commit()
                room_id = cur.lastrowid
                
                # Add host as participant
                cur.execute("""
                    INSERT INTO room_participants (room_id, user_id, role, is_video_on, is_audio_on)
                    VALUES (%s, %s, 'host', TRUE, TRUE)
                """, (room_id, session['user_id']))
                mysql.connection.commit()
                
                flash('Voice room created successfully!', 'success')
                return redirect(f'/voice-room/{room_code}')
            except Exception as e:
                print(f"Error creating voice room: {e}")
                import traceback
                traceback.print_exc()
                flash(f'Error creating voice room: {str(e)}', 'danger')
                return redirect('/voice-rooms')
        
        # Get user's groups for dropdown
        if not session.get('demo_mode'):
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT g.id, g.group_name FROM `groups` g
                JOIN group_members gm ON g.id = gm.group_id
                WHERE gm.user_id = %s
            """, [session['user_id']])
            user_groups = cur.fetchall()
        else:
            user_groups = []
        
        return render_template('create_voice_room.html', user_groups=user_groups)
    
    # ─── JOIN VOICE ROOM ──────────────────────────────────────────
    @app.route('/voice-room/<room_code>')
    def join_voice_room(room_code):
        """Join a voice room"""
        if 'user_id' not in session:
            flash('Please login first!', 'warning')
            return redirect('/login')
        
        if session.get('demo_mode'):
            # Demo room data
            room = (1, '🐍 Python Doubt Clearing', 'Python Programming', 'Live session for Python doubts', 
                   999, True, True, 6, 'ABC12345', None, None)
            participants = [
                (1, 1, 999, 'host', True, True, 'Demo User'),
                (2, 1, 1, 'stage', True, True, 'Priya Singh'),
                (3, 1, 2, 'audience', False, False, 'Amit Verma'),
            ]
            messages = []
        else:
            try:
                cur = mysql.connection.cursor()
                
                # Get room details
                cur.execute("""
                    SELECT vr.*, u.name as host_name
                    FROM voice_rooms vr
                    JOIN users u ON vr.host_id = u.id
                    WHERE vr.room_code = %s AND vr.is_active = TRUE
                """, [room_code])
                room = cur.fetchone()
                
                if not room:
                    flash('Voice room not found or has ended!', 'danger')
                    return redirect('/voice-rooms')
                
                room_id = room[0]
                
                # Check if user is already a participant
                cur.execute("""
                    SELECT id FROM room_participants
                    WHERE room_id = %s AND user_id = %s AND left_at IS NULL
                """, (room_id, session['user_id']))
                
                if not cur.fetchone():
                    # Add user as audience member
                    cur.execute("""
                        INSERT INTO room_participants (room_id, user_id, role)
                        VALUES (%s, %s, 'audience')
                    """, (room_id, session['user_id']))
                    mysql.connection.commit()
                
                # Get all participants
                cur.execute("""
                    SELECT rp.*, u.name
                    FROM room_participants rp
                    JOIN users u ON rp.user_id = u.id
                    WHERE rp.room_id = %s AND rp.left_at IS NULL
                    ORDER BY 
                        CASE rp.role 
                            WHEN 'host' THEN 1 
                            WHEN 'stage' THEN 2 
                            ELSE 3 
                        END,
                        rp.joined_at ASC
                """, [room_id])
                participants = cur.fetchall()
                
                # Get recent messages
                cur.execute("""
                    SELECT rm.*, u.name as sender_name
                    FROM room_messages rm
                    JOIN users u ON rm.user_id = u.id
                    WHERE rm.room_id = %s
                    ORDER BY rm.sent_at DESC
                    LIMIT 50
                """, [room_id])
                messages = list(cur.fetchall())
                messages.reverse()
                
            except Exception as e:
                print(f"Error joining voice room: {e}")
                import traceback
                traceback.print_exc()
                flash(f'Error loading voice room: {str(e)}', 'danger')
                return redirect('/voice-rooms')
        
        return render_template('voice_room.html', 
                             room=room, 
                             participants=participants,
                             messages=messages,
                             room_code=room_code)
    
    # ─── END VOICE ROOM ───────────────────────────────────────────
    # ─── START VOICE ROOM ─────────────────────────────────────────
    @app.route('/start-voice-room/<room_code>', methods=['POST'])
    def start_voice_room(room_code):
        """Start a voice room (host only)"""
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if session.get('demo_mode'):
            return jsonify({'error': 'Demo mode'}), 403
        
        cur = mysql.connection.cursor()
        
        # Verify user is host
        cur.execute("""
            SELECT id FROM voice_rooms
            WHERE room_code = %s AND host_id = %s AND is_active = TRUE
        """, (room_code, session['user_id']))
        
        room = cur.fetchone()
        if not room:
            return jsonify({'error': 'Not authorized or room not found'}), 403
        
        # Start the room
        cur.execute("""
            UPDATE voice_rooms
            SET started_at = NOW(), host_online = TRUE
            WHERE room_code = %s
        """, [room_code])
        
        mysql.connection.commit()
        
        # Notify all participants
        socketio.emit('room_started', {
            'message': 'Host has started the session!'
        }, room=room_code)
        
        return jsonify({'success': True})
    
    # ─── END VOICE ROOM ───────────────────────────────────────────
    @app.route('/end-voice-room/<room_code>', methods=['POST'])
    def end_voice_room(room_code):
        """End a voice room (host only)"""
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if session.get('demo_mode'):
            return jsonify({'error': 'Demo mode'}), 403
        
        cur = mysql.connection.cursor()
        
        # Verify user is host
        cur.execute("""
            SELECT id FROM voice_rooms
            WHERE room_code = %s AND host_id = %s AND is_active = TRUE
        """, (room_code, session['user_id']))
        
        room = cur.fetchone()
        if not room:
            return jsonify({'error': 'Not authorized or room not found'}), 403
        
        # End the room
        cur.execute("""
            UPDATE voice_rooms
            SET is_active = FALSE, ended_at = NOW()
            WHERE room_code = %s
        """, [room_code])
        
        # Mark all participants as left
        cur.execute("""
            UPDATE room_participants
            SET left_at = NOW()
            WHERE room_id = %s AND left_at IS NULL
        """, [room[0]])
        
        mysql.connection.commit()
        
        return jsonify({'success': True})
    
    # ─── EDIT VOICE ROOM ──────────────────────────────────────────
    @app.route('/edit-voice-room/<room_code>', methods=['GET', 'POST'])
    def edit_voice_room(room_code):
        """Edit voice room settings (host only)"""
        if 'user_id' not in session:
            flash('Please login first!', 'warning')
            return redirect('/login')
        
        if session.get('demo_mode'):
            flash('⚠️ Demo Mode: Editing is disabled. Sign up for full access!', 'warning')
            return redirect('/voice-rooms')
        
        cur = mysql.connection.cursor()
        
        # Get room and verify host
        cur.execute("""
            SELECT * FROM voice_rooms
            WHERE room_code = %s AND host_id = %s
        """, (room_code, session['user_id']))
        
        room = cur.fetchone()
        if not room:
            flash('Room not found or you are not the host!', 'danger')
            return redirect('/voice-rooms')
        
        if request.method == 'POST':
            try:
                room_name = request.form['room_name']
                subject = request.form['subject']
                description = request.form.get('description', '')
                room_type = request.form.get('room_type', 'video')
                is_public = request.form.get('is_public', 'false') == 'true'
                
                cur.execute("""
                    UPDATE voice_rooms
                    SET room_name = %s, subject = %s, description = %s, 
                        room_type = %s, is_public = %s
                    WHERE room_code = %s
                """, (room_name, subject, description, room_type, is_public, room_code))
                mysql.connection.commit()
                
                flash('Voice room updated successfully!', 'success')
                return redirect(f'/voice-room/{room_code}')
            except Exception as e:
                print(f"Error updating voice room: {e}")
                flash(f'Error updating voice room: {str(e)}', 'danger')
        
        return render_template('edit_voice_room.html', room=room, room_code=room_code)
    
    # ─── DELETE VOICE ROOM ────────────────────────────────────────
    @app.route('/delete-voice-room/<room_code>', methods=['POST'])
    def delete_voice_room(room_code):
        """Delete a voice room (host only)"""
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if session.get('demo_mode'):
            return jsonify({'error': 'Demo mode'}), 403
        
        cur = mysql.connection.cursor()
        
        # Verify user is host
        cur.execute("""
            SELECT id FROM voice_rooms
            WHERE room_code = %s AND host_id = %s
        """, (room_code, session['user_id']))
        
        room = cur.fetchone()
        if not room:
            return jsonify({'error': 'Not authorized or room not found'}), 403
        
        try:
            # Delete related records first (foreign key constraints)
            cur.execute("DELETE FROM room_messages WHERE room_id = %s", [room[0]])
            cur.execute("DELETE FROM room_participants WHERE room_id = %s", [room[0]])
            cur.execute("DELETE FROM whiteboard_snapshots WHERE room_id = %s", [room[0]])
            cur.execute("DELETE FROM stage_requests WHERE room_id = %s", [room[0]])
            
            # Delete the room
            cur.execute("DELETE FROM voice_rooms WHERE id = %s", [room[0]])
            
            mysql.connection.commit()
            
            return jsonify({'success': True})
        except Exception as e:
            print(f"Error deleting voice room: {e}")
            return jsonify({'error': str(e)}), 500
    
    # ─── SOCKET.IO EVENTS ─────────────────────────────────────────
    
    @socketio.on('join_room')
    def handle_join_room(data):
        """Handle user joining a room"""
        room_code = data['room_code']
        username = session.get('user_name', 'Anonymous')
        user_id = session.get('user_id')
        
        join_room(room_code)
        
        # Check if user is host and update host_online status
        if not session.get('demo_mode'):
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT id, host_id FROM voice_rooms
                WHERE room_code = %s AND is_active = TRUE
            """, [room_code])
            room = cur.fetchone()
            
            if room and room[1] == user_id:
                # Host joined - mark as online
                cur.execute("""
                    UPDATE voice_rooms
                    SET host_online = TRUE
                    WHERE room_code = %s
                """, [room_code])
                mysql.connection.commit()
                
                # Notify all participants
                emit('host_status_changed', {
                    'is_online': True,
                    'message': 'Host is now online'
                }, room=room_code)
        
        emit('user_joined', {
            'user_id': user_id,
            'username': username,
            'message': f'{username} joined the room'
        }, room=room_code)
    
    @socketio.on('leave_room')
    def handle_leave_room(data):
        """Handle user leaving a room"""
        room_code = data['room_code']
        username = session.get('user_name', 'Anonymous')
        user_id = session.get('user_id')
        
        # Check if user is host and update host_online status
        if not session.get('demo_mode'):
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT id, host_id FROM voice_rooms
                WHERE room_code = %s AND is_active = TRUE
            """, [room_code])
            room = cur.fetchone()
            
            if room and room[1] == user_id:
                # Host left - mark as offline
                cur.execute("""
                    UPDATE voice_rooms
                    SET host_online = FALSE
                    WHERE room_code = %s
                """, [room_code])
                mysql.connection.commit()
                
                # Notify all participants
                emit('host_status_changed', {
                    'is_online': False,
                    'message': 'Host is offline. Waiting for host...'
                }, room=room_code)
        
        leave_room(room_code)
        emit('user_left', {
            'user_id': user_id,
            'username': username,
            'message': f'{username} left the room'
        }, room=room_code)
    
    @socketio.on('send_message')
    def handle_send_message(data):
        """Handle chat message"""
        room_code = data['room_code']
        message = data['message']
        username = session.get('user_name', 'Anonymous')
        user_id = session.get('user_id')
        
        # Save to database if not demo mode
        if not session.get('demo_mode'):
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM voice_rooms WHERE room_code = %s", [room_code])
            room = cur.fetchone()
            if room:
                cur.execute("""
                    INSERT INTO room_messages (room_id, user_id, message)
                    VALUES (%s, %s, %s)
                """, (room[0], user_id, message))
                mysql.connection.commit()
        
        emit('new_message', {
            'user_id': user_id,
            'username': username,
            'message': message,
            'timestamp': 'Just now'
        }, room=room_code)
    
    @socketio.on('request_stage')
    def handle_stage_request(data):
        """Handle request to join stage"""
        room_code = data['room_code']
        username = session.get('user_name', 'Anonymous')
        user_id = session.get('user_id')
        
        emit('stage_request', {
            'user_id': user_id,
            'username': username
        }, room=room_code)
    
    @socketio.on('approve_stage')
    def handle_approve_stage(data):
        """Handle approving stage request"""
        room_code = data['room_code']
        target_user_id = data['user_id']
        
        # Update database
        if not session.get('demo_mode'):
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM voice_rooms WHERE room_code = %s", [room_code])
            room = cur.fetchone()
            if room:
                cur.execute("""
                    UPDATE room_participants
                    SET role = 'stage'
                    WHERE room_id = %s AND user_id = %s
                """, (room[0], target_user_id))
                mysql.connection.commit()
        
        emit('stage_approved', {
            'user_id': target_user_id
        }, room=room_code)
    
    @socketio.on('webrtc_offer')
    def handle_webrtc_offer(data):
        """Handle WebRTC offer"""
        room_code = data['room_code']
        emit('webrtc_offer', data, room=room_code, include_self=False)
    
    @socketio.on('webrtc_answer')
    def handle_webrtc_answer(data):
        """Handle WebRTC answer"""
        room_code = data['room_code']
        emit('webrtc_answer', data, room=room_code, include_self=False)
    
    @socketio.on('webrtc_ice_candidate')
    def handle_ice_candidate(data):
        """Handle ICE candidate"""
        room_code = data['room_code']
        emit('webrtc_ice_candidate', data, room=room_code, include_self=False)
    
    @socketio.on('whiteboard_draw')
    def handle_whiteboard_draw(data):
        """Handle whiteboard drawing"""
        room_code = data['room_code']
        emit('whiteboard_draw', data, room=room_code, include_self=False)
    
    @socketio.on('whiteboard_clear')
    def handle_whiteboard_clear(data):
        """Handle whiteboard clear"""
        room_code = data['room_code']
        emit('whiteboard_clear', {}, room=room_code, include_self=False)
    
    @socketio.on('whiteboard_text')
    def handle_whiteboard_text(data):
        """Handle whiteboard text"""
        room_code = data['room_code']
        emit('whiteboard_text', data, room=room_code, include_self=False)
    
    @socketio.on('whiteboard_text_update')
    def handle_whiteboard_text_update(data):
        """Handle whiteboard text update (notepad style)"""
        room_code = data['room_code']
        emit('whiteboard_text_update', data, room=room_code, include_self=False)
    
    @socketio.on('whiteboard_text_render')
    def handle_whiteboard_text_render(data):
        """Handle whiteboard text render to canvas"""
        room_code = data['room_code']
        emit('whiteboard_text_render', data, room=room_code, include_self=False)
    
    @socketio.on('toggle_video')
    def handle_toggle_video(data):
        """Handle video toggle"""
        room_code = data['room_code']
        user_id = session.get('user_id')
        is_on = data['is_on']
        
        emit('user_video_toggle', {
            'user_id': user_id,
            'is_on': is_on
        }, room=room_code)
    
    @socketio.on('toggle_audio')
    def handle_toggle_audio(data):
        """Handle audio toggle"""
        room_code = data['room_code']
        user_id = session.get('user_id')
        is_on = data['is_on']
        
        emit('user_audio_toggle', {
            'user_id': user_id,
            'is_on': is_on
        }, room=room_code)
