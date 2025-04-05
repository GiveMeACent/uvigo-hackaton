import subprocess
import os

FPS = 60
SEGMENT_SECONDS = 5
WINDOW = SEGMENT_SECONDS * FPS  # 60 FPS * 5 seconds = 300 frames


def parse_gcsv(file_path):
    f = open(file_path, "r")
    lines = f.readlines()
    f.close()

    data_gcsv = []
    gcsvs = lines[16:]  # Skip the first 16 lines (header)
    for gcsv in gcsvs:
        gcsvData = gcsv.split(",")
        data_gcsv.append([gcsvData[1], gcsvData[2], gcsvData[3]])
    return data_gcsv


def score_segments(df):
    scores = []
    for i in range(0, len(df) - WINDOW):
        window = df[i:i+WINDOW]  # Slice the data directly
        motion = 0  # Initialize motion
        for sublist in window:
            for val in sublist:
                motion += abs(float(val))  # Sum absolute values of rx, ry, rz
        scores.append((i, motion))
    return sorted(scores, key=lambda x: x[1], reverse=True)


def select_top_segments(scored, min_distance=WINDOW):
    selected = []
    for idx, score in scored:
        if len(selected) == 0 or (idx - selected[-1][0]) >= min_distance:
            selected.append((idx, score))
        if len(selected) == 3:  # Limit to 3 clips
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

    data_gcsv = parse_gcsv(gcsv_path)
    print("Scoring segments...")
    scored = score_segments(data_gcsv)
    selected = select_top_segments(scored)

    clips = []
    for i, (start_idx, _) in enumerate(selected):
        out_name = f"{idx_prefix}_clip{i+1}.mp4"
        out_path = os.path.join(output_dir, out_name)
        extract_clip(video_path, start_idx, out_path)
        clips.append(out_path)
        print(
            f"Extracted clip {i+1}: starts at frame {start_idx} ({start_idx/FPS:.2f}s)")

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
    print(f"Summary video created: {output_path}")


def main():
    video_dir = "/home/flamingfury/media/2aad:6371/videos/"
    log_dir = "/home/flamingfury/media/2aad:6371/gcsv/"
    output_dir = "/home/flamingfury/media/2aad:6371/output/"

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_clips = []

    # Get list of video files in the video directory
    video_files = os.listdir(video_dir)
    video_files = [f for f in video_files if f.endswith(
        ".MP4")]  # Only MP4 files
    video_files.sort()  # Sort the video files

    # Process each video file
    for i, video_file in enumerate(video_files):
        # Get the base name without extension
        base_name = os.path.splitext(video_file)[0]
        video_path = os.path.join(video_dir, video_file)
        gcsv_path = os.path.join(log_dir, base_name + ".gcsv")

        if os.path.exists(gcsv_path):
            clips = process_video(video_path, gcsv_path,
                                  output_dir, idx_prefix=f"{i}")
            all_clips.extend(clips)  # Add clips to the list
        else:
            print(f"⚠️  No matching .gcsv for {video_file}")

    # Combine all clips into one final summary video
    final_output = "snippet.mp4"
    combine_clips(all_clips, final_output)


if __name__ == "__main__":
    main()
