import os
import pandas as pd
import subprocess
from tqdm import tqdm

FPS = 60
SEGMENT_SECONDS = 5
WINDOW = SEGMENT_SECONDS * FPS  # 60 FPS * 5 seconds = 300 frames

def parse_gcsv(file_path):
    df = pd.read_csv(file_path, comment="#", skiprows=10)
    return df[['rx', 'ry', 'rz']]

def score_segments(df):
    scores = []
    for i in range(0, len(df) - WINDOW):
        window = df.iloc[i:i+WINDOW]
        motion = window.abs().sum().sum()  # sum of abs(rx, ry, rz)
        scores.append((i, motion))
    return sorted(scores, key=lambda x: x[1], reverse=True)

def select_top_segments(scored, min_distance=WINDOW):
    selected = []
    used_indices = set()
    for idx, score in scored:
        if all(abs(idx - s[0]) >= min_distance for s in selected):
            selected.append((idx, score))
        if len(selected) == 3:
            break
    return selected

def extract_clip(video_path, start_frame, output_path):
    start_time = start_frame / FPS
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-i", video_path,
        "-t", str(SEGMENT_SECONDS),
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_video(video_path, gcsv_path, output_dir, idx_prefix=""):
    print(f"Processing: {os.path.basename(video_path)}")

    df = parse_gcsv(gcsv_path)
    print("Scoring segments...")
    scored = score_segments(df)
    selected = select_top_segments(scored)

    clips = []
    for i, (start_idx, _) in enumerate(selected):
        out_name = f"{idx_prefix}_clip{i+1}.mp4"
        out_path = os.path.join(output_dir, out_name)
        extract_clip(video_path, start_idx, out_path)
        clips.append(out_path)
        print(f"  → Extracted clip {i+1}: starts at frame {start_idx} ({start_idx/FPS:.2f}s)")

    return clips

def combine_clips(clip_paths, output_path):
    print("Combining clips into final summary video...")
    with open("clips.txt", "w") as f:
        for path in clip_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "clips.txt",
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd)
    os.remove("clips.txt")
    print(f"✅ Summary video created: {output_path}")

def main():
    video_dir = "./videos"
    log_dir = "./gcsv"
    output_dir = "./output"

    os.makedirs(output_dir, exist_ok=True)

    all_clips = []

    video_files = sorted([f for f in os.listdir(video_dir) if f.endswith(".MP4")])
    for i, video_file in enumerate(tqdm(video_files, desc="Videos")):
        base_name = os.path.splitext(video_file)[0]
        video_path = os.path.join(video_dir, video_file)
        gcsv_path = os.path.join(log_dir, base_name + ".gcsv")

        if os.path.exists(gcsv_path):
            clips = process_video(video_path, gcsv_path, output_dir, idx_prefix=f"{i}")
            all_clips.extend(clips)
        else:
            print(f"⚠️  No matching .gcsv for {video_file}")

    final_output = "final_summary.mp4"
    combine_clips(all_clips, final_output)

if __name__ == "__main__":
    main()
