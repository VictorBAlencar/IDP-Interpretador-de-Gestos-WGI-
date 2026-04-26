import cv2
import mediapipe as mp
import time
import threading
import traceback
import pyautogui
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import calculo_distancia as util
import cursor_movement
import left_click
import right_click
import double_click
import scroll


mpHands = mp.solutions.hands
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
screen_w, screen_h = pyautogui.size()

last_click_time = 0
click_cooldown = 0.4 
is_dragging = False
last_left_click_detected_time = 0
is_tracking = False
left_click_start_time = 0
mouse_down_triggered = False

current_state = {"x": 0.5, "y": 0.5, "action": "move"}
camera_ready_event = threading.Event()

def detect_gesture(frame, landmark_list, processed):
    global last_click_time, is_dragging, last_left_click_detected_time
    global left_click_start_time, mouse_down_triggered
    global current_state

    current_time = time.time()
    action = "move"

    if len(landmark_list) >= 21:
        hand_landmarks = processed.multi_hand_landmarks[0]
        palm_center = cursor_movement.get_palm_center(hand_landmarks)
        
     
        x, y = cursor_movement.get_normalized_position(palm_center, landmark_list)
        
        if x is not None and y is not None:
            current_state["x"], current_state["y"] = x, y
            pyautogui.moveTo(int(x * screen_w), int(y * screen_h))

        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])
        
        is_scrolling, scroll_amount = scroll.detect_scroll(landmark_list)
        is_db = double_click.is_double_click(landmark_list, thumb_index_dist)
        is_rc = right_click.is_right_click(landmark_list, thumb_index_dist)
        is_lc = left_click.is_left_click(landmark_list, thumb_index_dist, is_dragging)

        if is_scrolling:
            action = "scroll"
            if scroll_amount != 0:
                pyautogui.scroll(scroll_amount)
        elif is_db:
            action = "double_click"
        elif is_rc:
            action = "right_click"
        elif is_lc:
            last_left_click_detected_time = current_time
            if not is_dragging:
                is_dragging = True
                left_click_start_time = current_time
                mouse_down_triggered = False
                action = "left_click_intent"
            else:
                if current_time - left_click_start_time > 0.3 and not mouse_down_triggered:
                    pyautogui.mouseDown()
                    mouse_down_triggered = True
                action = "drag" if mouse_down_triggered else "holding_click"
        else:
            if is_dragging:
                if current_time - last_left_click_detected_time > 0.2:
                    is_dragging = False
                    if mouse_down_triggered:
                        action = "release_drag"
                        pyautogui.mouseUp()
                        mouse_down_triggered = False
                    else:
                        action = "left_click"
                        pyautogui.click()
                    last_click_time = current_time
                else:
                    action = "drag" if mouse_down_triggered else "holding_click"

        if not is_dragging and current_time - last_click_time > click_cooldown:
            if action == "right_click":
                pyautogui.click(button='right')
                last_click_time = current_time
            elif action == "double_click":
                pyautogui.doubleClick()
                last_click_time = current_time

        current_state["action"] = action
        
        cv2.putText(frame, f"Action: {action}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if cursor_movement.is_frozen(landmark_list):
            cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)
            
    else:
        if is_dragging:
            is_dragging = False
            if mouse_down_triggered:
                pyautogui.mouseUp()
                mouse_down_triggered = False

def _tracking_loop(headless):
    global is_tracking
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    hands = mpHands.Hands(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.85,
        min_tracking_confidence=0.85,
        max_num_hands=1
    )
    
    camera_ready_event.set()

    try:
        while cap.isOpened() and is_tracking:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.flip(frame, 1)
            processed = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            landmark_list = []
            if processed.multi_hand_landmarks:
                for lm in processed.multi_hand_landmarks[0].landmark:
                    landmark_list.append((lm.x, lm.y))
                draw.draw_landmarks(frame, processed.multi_hand_landmarks[0], mpHands.HAND_CONNECTIONS)

            detect_gesture(frame, landmark_list, processed)

            if not headless:
                cv2.imshow('WGI Engine', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'): break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        is_tracking = False

class WGIServer(BaseHTTPRequestHandler):
    def do_POST(self):
        message = "Ação não reconhecida."
        if self.path == '/start_tracking': 
            start_tracking(headless=True)
            message = "Câmera ativa e rastreando!"
        elif self.path == '/stop_tracking': 
            stop_tracking()
            message = "Câmera parada com sucesso."
        self.send_response(200); self.send_header('Access-Control-Allow-Origin', '*'); self.end_headers()
        self.wfile.write(json.dumps({"message": message}).encode())

    def do_GET(self):
        if self.path == '/state':
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Access-Control-Allow-Origin', '*'); self.end_headers()
            self.wfile.write(json.dumps(current_state).encode())
            if current_state["action"] not in ["move", "drag", "holding_click"]: current_state["action"] = "move"
        elif self.path == '/':
            self.send_response(200); self.send_header('Content-Type', 'text/plain'); self.send_header('Access-Control-Allow-Origin', '*'); self.end_headers()
            self.wfile.write(b"WGI Server is running! Available endpoints: GET /state, POST /start_tracking, POST /stop_tracking")
        else:
            self.send_error(404, "Endpoint not found")

def start_tracking(headless):
    global is_tracking
    if not is_tracking:
        camera_ready_event.clear()
        is_tracking = True
        threading.Thread(target=_tracking_loop, args=(headless,), daemon=True).start()
        camera_ready_event.wait(timeout=10.0)

def stop_tracking(): global is_tracking; is_tracking = False

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8765), WGIServer)
    print("WGI Server Running on 8765...")
    server.serve_forever()