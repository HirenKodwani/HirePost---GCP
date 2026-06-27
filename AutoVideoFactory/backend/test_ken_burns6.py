import subprocess, os

ffmpeg = r"C:\Users\ADMIN\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
inp = r"D:\HirePost\AutoVideoFactory\backend\output\assets\scene_0.jpg"
outdir = r"D:\HirePost\AutoVideoFactory\backend\output\videos"

# Approach: use Python + PIL to generate frames, then ffmpeg to encode
# This is more reliable than complex filter chains
from PIL import Image
import numpy as np

img = Image.open(inp)
target_w, target_h = 1080, 1920
n_frames = 150

# Scale image to fill target
img_ratio = max(target_w / img.width, target_h / img.height)
new_w = int(img.width * img_ratio)
new_h = int(img.height * img_ratio)
img_resized = img.resize((new_w, new_h), Image.LANCZOS)

# Center crop to target
left = (new_w - target_w) // 2
top = (new_h - target_h) // 2
img_cropped = img_resized.crop((left, top, left + target_w, top + target_h))

# Generate frames with Ken Burns zoom-in
frames_dir = os.path.join(outdir, "kb_frames")
os.makedirs(frames_dir, exist_ok=True)

import math
for n in range(n_frames):
    # Zoom factor: 1.0 to 1.3
    zoom = 1.0 + 0.3 * n / n_frames
    
    # Crop a smaller region from the center
    crop_w = int(target_w / zoom)
    crop_h = int(target_h / zoom)
    
    # Center the crop
    cx = (target_w - crop_w) // 2
    cy = (target_h - crop_h) // 2
    
    frame = img_cropped.crop((cx, cy, cx + crop_w, cy + crop_h))
    frame = frame.resize((target_w, target_h), Image.LANCZOS)
    frame.save(os.path.join(frames_dir, f"frame_{n:04d}.png"))

print(f"Generated {n_frames} frames")

# Encode frames to video
out_path = os.path.join(outdir, "kb_zoom_in.mp4")
cmd = [
    ffmpeg, "-y",
    "-framerate", "30",
    "-i", os.path.join(frames_dir, "frame_%04d.png"),
    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
    out_path,
]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
sz = os.path.getsize(out_path) if os.path.exists(out_path) else 0
print(f"Encode: rc={r.returncode}, sz={sz}")
