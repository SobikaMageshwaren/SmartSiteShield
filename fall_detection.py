import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import pygame
import time

# Initialize Mediapipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize pygame for sound
pygame.mixer.init()
alarm_sound_path = "D:/6 SEM LAB/DL LAB/fall/alarm.mp3"  # Replace with your alarm sound file path

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    if a and b and c:
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180:
            angle = 360 - angle
        return round(angle, 2)
    return None

# Function to calculate fall detection value based on body landmarks
def calculate_fall_value(landmarks):
    try:
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]

        shoulder_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
        hip_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

        if shoulder_hip_angle is not None and hip_knee_angle is not None:
            return round(180 - (shoulder_hip_angle + hip_knee_angle), 2)
    except Exception as e:
        st.error(f"Error processing landmarks: {e}")

    return None

# Function to play alarm sound after fall detection is confirmed
def play_alarm():
    pygame.mixer.music.load(alarm_sound_path)
    pygame.mixer.music.play(-1)  # Loop the sound indefinitely

# Streamlit web interface
def main():
    st.title("Fall Detection System")
    st.write("Monitoring fall value via webcam...")

    cap = cv2.VideoCapture(0)
    stframe = st.empty()
    value_display = st.empty()

    fall_detected = False
    last_fall_value = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture video. Please check your camera.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        fall_value = "Calculating..."

        if results.pose_landmarks:
            # Draw landmarks on frame
            mp.solutions.drawing_utils.draw_landmarks(
                frame, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=4),
                connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)
            )

            # Calculate fall value
            fall_value = calculate_fall_value(results.pose_landmarks.landmark)
            if fall_value is not None:
                last_fall_value = fall_value
                if fall_value > 50 and not fall_detected:  # Adjust threshold based on detection logic
                    fall_detected = True
                    value_display.write(f"**Fall Detected, Value:** {last_fall_value}")
                    stframe.image(frame, channels="BGR", use_container_width=True)
                    play_alarm()  # Play alarm only after detecting a fall
                    break  # Stop further updates once fall is detected
                else:
                    value_display.write(f"**Fall Value:** {fall_value}")

        stframe.image(frame, channels="BGR", use_container_width=True)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
