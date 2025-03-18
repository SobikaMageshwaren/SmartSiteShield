SmartSite Shield — Vision-Based Worker Safety and Zone Compliance System

🚧 Project Overview

SmartSite Shield is an AI-driven safety monitoring system designed to enhance worker protection and ensure zone compliance on construction sites. This project leverages computer vision to detect safety violations and unauthorized access in real time.

🎯 Key Features

Fall Detection: Uses Mediapipe Pose Estimation to detect falls and alert supervisors instantly.

Helmet Compliance Verification: Employs YOLOv8 for object detection combined with HSV color filtering to ensure workers are wearing helmets.

Zone Access Checker: Flags unauthorized entries into restricted zones based on location data and visual tracking.

Real-Time Monitoring Interface: Built with Streamlit for an intuitive, responsive dashboard featuring live video feeds, safety violation alerts, and performance analytics.

🔧 Technologies Used

Python – Core language for building the system

OpenCV – For image and video processing

Mediapipe – Pose estimation for fall detection

YOLOv8 – Helmet detection

HSV Color Filtering – Verifying helmet color compliance

Streamlit – Interactive web-based interface

Pygame – Visual zone mapping and simulations

NumPy & Pandas – Data handling and analysis

To run the project: python <modulename>.py
For Datasets: Refer commonly available dataset repository for easy access.
