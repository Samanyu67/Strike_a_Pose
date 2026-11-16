# STRIKE A POSE: a pose appears on screen. Copy it with your body and hold it for 1 second to score.
# Run it from this folder:  python strike_a_pose.py      (movenet.onnx and requirements.txt must sit next to this file)
# Lines marked (given) are done for you. Your job is TODO 1 to TODO 4. Do them in order, and run the program after each one.
# Keys in the camera window: r = play again   q or Esc = quit (or close the window)
# Errors appear in this terminal, not in the camera window.

import os
import random
import subprocess
import sys
import time

# (given) A: install the three packages if they are missing, then load them.
HERE = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--disable-pip-version-check", "-r", os.path.join(HERE, "requirements.txt")])
import cv2                                          # opencv-python, numpy and onnxruntime: installed by the line above
import numpy as np
import onnxruntime

# (given) B: the five poses as 4 arm angles in degrees (left upper arm, left forearm, right upper arm, right forearm),
#   the game settings, the AI model (MoveNet), the 12 bones that join the 17 points, and the colours.
POSES = {"Arms up!": [-90, -90, -90, -90], "T-pose!": [180, 180, 0, 0], "Right arm up!": [90, 90, -90, -90],
         "Left arm up!": [-90, -90, 90, 90], "Strong arms!": [180, -90, 0, -90]}   # arm angles: left upper, left lower, right upper, right lower
SECONDS, HOLD = 10, 1.0                             # seconds for each pose, and how long to hold it
model = onnxruntime.InferenceSession(os.path.join(HERE, "movenet.onnx"))     # MoveNet: finds 17 body points
BONES = [(5, 7), (7, 9), (6, 8), (8, 10), (5, 6), (5, 11), (6, 12), (11, 12), (11, 13), (13, 15), (12, 14), (14, 16)]
FONT, WHITE, YELLOW, GREEN = cv2.FONT_HERSHEY_SIMPLEX, (255, 255, 255), (0, 255, 255), (0, 200, 0)


def find_body(frame):
    side = max(frame.shape[:2])
    # TODO 1: get the 17 body points from the AI, as (x, y, sure) in pixels of the frame.
    #   a) Pad the frame at the bottom and right with black, so it becomes a square of side x side (the AI wants a square).
    #   b) Resize it to 192 x 192, change BGR (OpenCV's order) to RGB, make the numbers int32, and add a "how many
    #      pictures" axis in front, so the shape is (1, 192, 192, 3). Call it x.
    #   c) Run the model on x. Its answer has the shape (1, 1, 17, 3): for each point y, x and how sure (all from 0 to 1).
    #      Return a list of 17 tuples (x in pixels, y in pixels, sure): multiply y and x by side.
    # Check: stand in front of the camera. A yellow skeleton follows your body.
    return [(0, 0, 0)] * 17                         # (given) placeholder: "no body found". Replace it.


def match(points, target):
    # TODO 2: score how close the arms are to the target pose, from 0 to 100.
    #   a) If any arm point (5 to 10) is less than 0.3 sure, return 0: the AI cannot see your arms.
    #   b) For each of the 4 angles, find the difference to the target angle the short way round the circle
    #      (so 179 and -179 are 2 degrees apart, not 358). The trick: (a - t + 180) % 360 - 180, then its size.
    #   c) Return 100 minus the mean difference, but never less than 0.
    # Check: the bar shows "match 10%" whatever you do: the angles are still placeholders (TODO 3 fixes that).
    return 0                                        # (given) placeholder: "no match". Replace it.


def arm_angles(points):
    # TODO 3: turn the arm points into 4 angles in degrees: left upper arm, left forearm, right upper arm, right forearm.
    #   The arms are points 5, 7, 9 (shoulder, elbow, wrist on one side) and 6, 8, 10 (the other side). The "left" arm
    #   is the one whose shoulder is further left on the screen (smaller x). For each bone from point a to point b,
    #   the angle is np.arctan2(how far down, how far right) from a to b, changed to degrees.
    # Check: the match % follows your arms. Copy the pose on the screen: it goes over 80% and the bar turns green.
    return [0, 0, 0, 0]                             # (given) placeholder: every arm points right. Replace it.


# (given) C: draw a small stick figure of the pose to copy, top right of the window.
def draw_target(view, angles):                      # a small stick figure of the pose to copy, top right
    x, y = view.shape[1] - 80, 150
    cv2.rectangle(view, (x - 76, y - 70), (x + 76, y + 80), (40, 40, 40), -1)
    cv2.circle(view, (x, y - 42), 11, WHITE, 2)
    cv2.polylines(view, [np.array([(x - 20, y - 22), (x + 20, y - 22)]), np.array([(x, y - 22), (x, y + 30)])], False, WHITE, 3)
    step = lambda point, angle: (int(point[0] + 26 * np.cos(np.radians(angle))), int(point[1] + 26 * np.sin(np.radians(angle))))
    for shoulder, (upper, lower) in (((x - 20, y - 22), angles[:2]), ((x + 20, y - 22), angles[2:])):   # each arm: shoulder, elbow, hand
        cv2.polylines(view, [np.array([shoulder, step(shoulder, upper), step(step(shoulder, upper), lower)])], False, YELLOW, 4)


# (given) D: start the camera and the game: the poses in a random order, the turn, the score and the timers.
video = cv2.VideoCapture(0)
order, turn, score, held_since, nice_until, deadline = random.sample(list(POSES), len(POSES)), 0, 0, None, 0, time.time() + SECONDS
while True:
    # (given) E: read a frame, mirror it like a selfie, find the body, and draw every bone whose two points are sure.
    ok, frame = video.read()
    if not ok:
        break
    view = cv2.flip(frame, 1)
    points = find_body(view)
    for a, b in BONES:                              # the body the AI found: 17 points joined into a skeleton
        if points[a][2] > 0.3 and points[b][2] > 0.3:
            cv2.line(view, (int(points[a][0]), int(points[a][1])), (int(points[b][0]), int(points[b][1])), YELLOW, 4)
    if turn < len(order):
        percent = match(points, POSES[order[turn]])
        # TODO 4: turn the match into a score.
        #   a) When percent is 80 or more, remember the time it first got there in held_since; below 80, set held_since to None.
        #   b) When the pose has been held for HOLD seconds, OR the time for this pose is over (deadline): if it was held,
        #      add 1 to score, show "Nice!" for 0.8 seconds (nice_until) and save the picture with cv2.imwrite as
        #      pose_<time>.jpg in HERE. In both cases go to the next pose: turn + 1, held_since None, a new deadline.
        # Check: hold the pose on the screen for 1 second. "Nice!" flashes, the score goes up and a pose_ photo is saved.
        if time.time() > deadline:                  # (given) placeholder: no scoring yet, just the next pose when time is up.
            turn, deadline = turn + 1, time.time() + SECONDS
    # (given) F: the top bar, the pose name, the time left, the score, the match bar and the pose to copy.
    cv2.rectangle(view, (0, 0), (view.shape[1], 60), (30, 30, 30), -1)   # the top bar (not in the saved photo)
    if turn < len(order):
        cv2.putText(view, order[turn], (15, 42), FONT, 1.2, YELLOW, 3)
        cv2.putText(view, f"{max(0, int(deadline - time.time()))} s    score {score}/{len(order)}", (view.shape[1] - 250, 40), FONT, 0.8, WHITE, 2)
        cv2.rectangle(view, (15, 70), (15 + int(3 * percent), 85), GREEN if percent >= 80 else (0, 140, 255), -1)
        cv2.putText(view, "Hold it!" if held_since else f"match {percent:.0f}%", (330, 84), FONT, 0.6, WHITE, 2)
        draw_target(view, POSES[order[turn]])
    else:
        view = view // 3
        cv2.putText(view, f"You scored {score} of {len(order)}!", (40, view.shape[0] // 2), FONT, 1.4, YELLOW, 3)
        cv2.putText(view, "r play again    q quit", (40, view.shape[0] // 2 + 50), FONT, 0.8, WHITE, 2)
    # (given) G: the green "Nice!" flash, then show the picture.
    if time.time() < nice_until:
        cv2.rectangle(view, (0, 0), (view.shape[1] - 1, view.shape[0] - 1), GREEN, 14)
        cv2.putText(view, "Nice!", (view.shape[1] // 2 - 70, view.shape[0] // 2), FONT, 2, GREEN, 5)
    cv2.imshow("Strike a Pose", view)
    # (given) H: the keys. Every key is made lowercase, so Caps Lock does not matter. r starts a new game.
    key = chr(cv2.waitKey(1) & 255).lower()
    if key in ("q", "\x1b") or cv2.getWindowProperty("Strike a Pose", cv2.WND_PROP_VISIBLE) == 0:
        break
    if key == "r":
        order, turn, score, held_since, deadline = random.sample(list(POSES), len(POSES)), 0, 0, None, time.time() + SECONDS
video.release()
cv2.destroyAllWindows()
