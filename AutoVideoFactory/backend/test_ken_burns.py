import subprocess, os, sys

ffmpeg = r"C:\Users\ADMIN\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
inp = r"D:\HirePost\AutoVideoFactory\backend\output\assets\scene_0.jpg"
out = r"D:\HirePost\AutoVideoFactory\backend\output\videos\test_ken.mp4"

if not os.path.exists(inp):
    print(f"Input not found: {inp}")
    sys.exit(1)

# Test basic loop without zoompan first
cmd = [
    ffmpeg, "-y",
    "-loop", "1",
    "-i", inp,
    "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
    "-t", "5", "-r", "30",
    out,
]
print("Test 1: Basic loop")
r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
print(f"  Return: {r.returncode}, Size: {os.path.getsize(out) if os.path.exists(out) else 0}")
if r.returncode != 0:
    print(f"  Stderr: {r.stderr[-300:]}")

# Test with zoompan
out2 = r"D:\HirePost\AutoVideoFactory\backend\output\videos\test_ken2.mp4"
vf = (
    "scale=1080:1920:force_original_aspect_ratio=increase,"
    "crop=1080:1920,"
    "zoompan=z='min(1.0+0.0020134228187919463*n,1.3)':d=150:s=1080x1920:fps=30"
)
cmd2 = [
    ffmpeg, "-y",
    "-loop", "1",
    "-i", inp,
    "-vf", vf,
    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
    out2,
]
print("Test 2: Zoompan")
r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=120)
print(f"  Return: {r2.returncode}, Size: {os.path.getsize(out2) if os.path.exists(out2) else 0}")
if r2.returncode != 0:
    print(f"  Stderr: {r2.stderr[-500:]}")
else:
    print("  Success!")
