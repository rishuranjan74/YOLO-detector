# YOLO-detector
Aegis Vision: An AI-Powered Safety Compliance System
Aegis Vision is an end-to-end computer vision application designed to enhance workplace safety by automatically monitoring personnel for Personal Protective Equipment (PPE) compliance in real-time. This project, developed in Kanpur, UP, moves beyond simple object detection to create a robust, intelligent surveillance solution capable of nuanced decision-making.

🎥 Live Demonstration
[Link to your 60-90 second YouTube video demonstration here. This is the most important part of the README.]

Core Concepts & System Architecture
The power of this project lies in the synergy of three core components: a state-of-the-art Convolutional Neural Network (CNN) for sight, a sophisticated Object Tracking Algorithm for memory, and a custom State Machine for intelligent decision-making.

1. Real-Time Object Detection: The "Eyes"
The system's perception is powered by YOLOv8, a highly efficient CNN architecture. A CNN is used here for its unparalleled ability to learn hierarchical features directly from pixel data.

Why YOLOv8? I chose YOLOv8 for its optimal balance between high accuracy and real-time inference speed, making it perfectly suited for live video analysis on standard hardware. While larger models might offer slightly higher precision, their computational cost would make real-time application impractical.

Functionality: For each frame, the CNN performs two tasks simultaneously:

Object Classification: It identifies what is in the frame (e.g., person, helmet, vest).

Object Localization: It predicts the precise bounding box coordinates for each identified object.

2. Persistent Object Tracking: The "Memory"
Simple frame-by-frame detection is insufficient for monitoring individuals over time. To solve this, the system integrates the ByteTrack algorithm.

The Challenge: Without tracking, the system would know a person is in violation, but wouldn't know if it's the same person from one second to the next. This makes timing-based alerts impossible.

The Solution: ByteTrack analyzes the detections from the CNN across consecutive frames. By comparing the position and appearance of objects, it assigns a stable, unique track_id to each individual. This "memory" is the foundation upon which the entire alarm system is built.

3. State Machine & Logic: The "Brain"
The decision-making core is a custom-built State Machine implemented in Python. This elevates the system from a simple detector to an intelligent agent.

Context-Awareness: The system uses a "Danger Zone"—a user-defined polygon—to apply compliance rules only where they are relevant. This spatial filtering prevents false alarms and focuses the system's attention.

Intelligent Alerting: To prevent "alert fatigue," the state machine tracks the status of each individual track_id. A person in violation progresses through a series of states (pending -> alarming -> reminding -> timed_out) based on a precise set of timing rules. This ensures that alerts are meaningful and actionable, rather than just being constant noise.

Technical Stack
Core AI/CV: YOLOv8 (PyTorch), OpenCV, ByteTrack, NumPy

Utilities: Playsound, OS, CSV, Datetime

Development: Python, Git, GitHub, Virtual Environments (venv)

Setup & Installation
Clone the repository: git clone [your-repo-link]

Create and activate a virtual environment.

Install dependencies: pip install -r requirements.txt

Download Model Weights: [Link to your .pt file on Google Drive/Dropbox]

Run the application: Double
