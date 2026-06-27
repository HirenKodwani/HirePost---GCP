import subprocess, os

ffmpeg = r"C:\Users\ADMIN\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
out = r"D:\HirePost\AutoVideoFactory\backend\output\videos\test_zoom"

# Test: ffmpeg zoompan with color source (no input image)
out1 = out + "color.mp4"
cmd1 = [
    ffmpeg, "-y",
    "-f", "lavfi",
    "-i", "color=c=blue:s=1080x1920:d=5",
    "-vf", "zoompan=z='1.0+0.002*n':d=150:s=1080x1920:fps=30",
    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
    out1,
]
print("Test: color source + zoompan")
r1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=30)
print(f"  Return: {r1.returncode}, Size: {os.path.getsize(out1) if os.path.exists(out1) else 0}")
if r1.returncode != 0:
    print(f"  Stderr: {r1.stderr[-400:]}")

# Check ffmpeg version and filters
r2 = subprocess.run([ffmpeg, "-version"], capture_output=True, text=True, timeout=10)
print(f"\nFFmpeg version: {r2.stdout[:100]}")

r3 = subprocess.run([ffmpeg, "-filters"], capture_output=True, text=True, timeout=10)
zoompan_line = [l for l in r3.stdout.split("\n") if "zoompan" in l]
print(f"Zoompan filter: {zoompan_line}")
