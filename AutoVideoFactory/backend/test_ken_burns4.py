import subprocess, os

ffmpeg = r"C:\Users\ADMIN\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
out = r"D:\HirePost\AutoVideoFactory\backend\output\videos\testz"

# Try zoompan with explicit fps
tests = [
    # (name, vf)
    ("zp1", "zoompan=z=1.1:d=150:fps=30:s=1080x1920"),
    ("zp2", "zoompan=z=1.1:d=30*5:s=1080x1920"),
    ("zp3", "zoompan=z=zoom+0.01:d=150:s=1080x1920:fps=30"),
    ("zp4", "zoompan=z='if(eq(on,1),1,zoom+0.01)':d=150:s=1080x1920:fps=30"),
]

for name, vf in tests:
    op = f"{out}_{name}.mp4"
    cmd = [
        ffmpeg, "-y",
        "-f", "lavfi",
        "-i", "color=c=blue:s=1080x1920:d=5:r=30",
        "-vf", vf,
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        op,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    sz = os.path.getsize(op) if os.path.exists(op) else 0
    print(f"{name}: rc={r.returncode}, sz={sz}")
    if r.returncode != 0:
        print(f"  {r.stderr[-200:]}")
