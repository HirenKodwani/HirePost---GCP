import subprocess, os

ffmpeg = r"C:\Users\ADMIN\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
inp = r"D:\HirePost\AutoVideoFactory\backend\output\assets\scene_0.jpg"
out = r"D:\HirePost\AutoVideoFactory\backend\output\videos\test_scale"

# Use scale with frame eval for zoom effect
# scale increasing over time, then crop back to target size
tests = [
    # Zoom in: scale gets larger, crop keeps center
    ("z-in", "scale='iw*(1+0.002*n)':'ih*(1+0.002*n)':eval=frame,crop=1080:1920"),
    # Zoom out: scale gets smaller, pad keeps center
    ("z-out", "scale='iw/(1+0.002*n)':'ih/(1+0.002*n)':eval=frame,crop=1080:1920"),
    # Simpler: fixed zoom with overlay pan
    ("simple-in", "scale=1400:2500,crop=1080:1920:'(1400-1080)*(1-n/150)':'2500-1920':eval=frame"),
]

for name, vf in tests:
    op = f"{out}_{name}.mp4"
    cmd = [
        ffmpeg, "-y",
        "-loop", "1",
        "-i", inp,
        "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{vf}",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        op,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    sz = os.path.getsize(op) if os.path.exists(op) else 0
    print(f"{name}: rc={r.returncode}, sz={sz}")
    if r.returncode != 0:
        print(f"  stderr: {r.stderr[-200:]}")
