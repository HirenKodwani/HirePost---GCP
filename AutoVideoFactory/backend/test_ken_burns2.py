import subprocess, os

ffmpeg = r"C:\Users\ADMIN\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
inp = r"D:\HirePost\AutoVideoFactory\backend\output\assets\scene_0.jpg"
out = r"D:\HirePost\AutoVideoFactory\backend\output\videos\test_zoompan"

# Test 1: zoompan alone (no pre-scale/crop)
out1 = out + "1.mp4"
cmd1 = [
    ffmpeg, "-y",
    "-loop", "1",
    "-i", inp,
    "-vf", "zoompan=z='1.0+0.002*n':d=150:s=1080x1920:fps=30",
    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
    out1,
]
print("Test 1: zoompan only")
r1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=120)
print(f"  Return: {r1.returncode}, Size: {os.path.getsize(out1) if os.path.exists(out1) else 0}")
if r1.returncode != 0:
    print(f"  Stderr: {r1.stderr[-300:]}")

# Test 2: scale+crop, then zoompan
out2 = out + "2.mp4"
cmd2 = [
    ffmpeg, "-y",
    "-loop", "1",
    "-i", inp,
    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='1.0+0.002*n':d=150:s=1080x1920:fps=30",
    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
    out2,
]
print("Test 2: scale+crop+zoompan")
r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=120)
print(f"  Return: {r2.returncode}, Size: {os.path.getsize(out2) if os.path.exists(out2) else 0}")
if r2.returncode != 0:
    print(f"  Stderr: {r2.stderr[-300:]}")

# Test 3: simpler approach - just scale and zoompan
out3 = out + "3.mp4"
cmd3 = [
    ffmpeg, "-y",
    "-loop", "1",
    "-i", inp,
    "-vf", "scale=1080:1920,zoompan=z='1.0+0.002*n':d=150:s=1080x1920:fps=30",
    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
    out3,
]
print("Test 3: scale then zoompan")
r3 = subprocess.run(cmd3, capture_output=True, text=True, timeout=120)
print(f"  Return: {r3.returncode}, Size: {os.path.getsize(out3) if os.path.exists(out3) else 0}")
if r3.returncode != 0:
    print(f"  Stderr: {r3.stderr[-300:]}")
