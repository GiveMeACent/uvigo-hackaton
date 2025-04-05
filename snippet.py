import os
import subprocess

# Constants
FPS = 60
SEGMENT_SECONDS = 5
WINDOW = SEGMENT_SECONDS * FPS  # 60 FPS * 5 seconds = 300 frames

def parse_gcsv(file_path):
    """
    Reads a .gcsv file and returns the motion and acceleration data.
    It skips the first 16 lines (header) and returns each remaining line
    as a list of six strings corresponding to [rx, ry, rz, ax, ay, az].
    """
    f = open(file_path, "r")
    lines = f.readlines()
    f.close()
    
    data_gcsv = []
    # Skip the header lines; assume data starts at line 16
    i = 16
    while i < len(lines):
        line = lines[i]
        parts = line.split(",")
        # Expecting at least 7 columns: t, rx, ry, rz, ax, ay, az
        if len(parts) >= 7:
            # Append rx, ry, rz, ax, ay, az (trim newline from last element)
            data_gcsv.append([parts[1], parts[2], parts[3], parts[4], parts[5], parts[6].strip()])
        i = i + 1
    return data_gcsv

def score_braking_segments(data):
    """
    Calculates a braking score for every possible 5-second window.
    
    For each window of WINDOW frames, the function sums the absolute value
    of the forward acceleration (ax) only when it is negative (indicating braking).
    It returns a list of tuples (start_frame, score) sorted by descending score.
    """
    scores = []
    total_frames = len(data)
    i = 0
    while i < total_frames - WINDOW:
        window_score = 0.0
        j = i
        while j < i + WINDOW:
            # Get the forward acceleration (ax) from the data (index 3)
            ax = float(data[j][3])
            if ax < 0:
                window_score = window_score + abs(ax)
            j = j + 1
        scores.append((i, window_score))
        i = i + 1
    # Sort the scores in descending order (highest braking score first)
    scores = sorted(scores, key=lambda item: item[1], reverse=True)
    return scores

def select_top_segments(scored, min_distance):
    """
    Selects three non-overlapping segments from the scored segments.
    
    A segment is selected if it does not overlap with the previously selected one,
    i.e. its start index is at least 'min_distance' frames after the last one.
    """
    selected = []
    i = 0
    while i < len(scored):
        idx, score = scored[i]
        if len(selected) == 0 or (idx - selected[-1][0]) >= min_distance:
            selected.append((idx, score))
        if len(selected) == 3:
            break
        i = i + 1
    return selected

def extract_clip(video_path, start_frame, output_path):
    """
    Uses ffmpeg to extract a clip from the video.
    
    The clip starts at the time corresponding to start_frame (converted to seconds)
    and has a duration equal to SEGMENT_SECONDS. The output is written to output_path.
    """
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

def process_video(video_path, gcsv_path, output_dir, idx_prefix):
    """
    Processes a single video and its corresponding .gcsv file.
    
    It parses the .gcsv to obtain acceleration data, scores every 5-second segment
    based on braking intensity, selects the top three non-overlapping segments,
    and extracts those clips from the video. It prints progress messages and returns
    a list of paths to the extracted clips.
    """
    print("Processing: " + os.path.basename(video_path))
    
    data = parse_gcsv(gcsv_path)
    print("Scoring braking segments...")
    scored = score_braking_segments(data)
    selected = select_top_segments(scored, WINDOW)
    
    clips = []
    i = 0
    while i < len(selected):
        start_idx = selected[i][0]
        out_name = idx_prefix + "_clip" + str(i+1) + ".mp4"
        out_path = os.path.join(output_dir, out_name)
        print("Extracting clip " + str(i+1) + ": starts at frame " + str(start_idx) +
              " (" + "{:.2f}".format(start_idx/FPS) + "s)")
        extract_clip(video_path, start_idx, out_path)
        clips.append(out_path)
        i = i + 1
    return clips

def combine_clips(clip_paths, output_path):
    """
    Combines multiple video clips into one final summary video using ffmpeg.
    
    It writes a temporary text file listing the absolute paths of the clips,
    then calls ffmpeg in concat mode to merge them. The temporary file is deleted after processing.
    """
    print("Combining clips into final summary video...")
    f = open("clips.txt", "w")
    i = 0
    while i < len(clip_paths):
        f.write("file '" + os.path.abspath(clip_paths[i]) + "'\n")
        i = i + 1
    f.close()
    
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
    print("Summary video created: " + output_path)

def main():
    """
    Main function to process all video and .gcsv files.
    
    It reads all .MP4 files from the video directory and, for each, checks for a matching .gcsv file.
    If found, it processes the video to extract three 5-second clips (based on braking events) and combines all clips
    into a final summary video.
    """
    video_dir = "/home/flamingfury/media/2aad:6371/videos/"
    log_dir = "/home/flamingfury/media/2aad:6371/gcsv/"
    output_dir = "/home/flamingfury/media/2aad:6371/output/"
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    all_clips = []
    # Get list of files in the video directory
    files = os.listdir(video_dir)
    video_files = []
    i = 0
    while i < len(files):
        if files[i].endswith(".MP4"):
            video_files.append(files[i])
        i = i + 1
    video_files.sort()  # Sort video files
    
    i = 0
    while i < len(video_files):
        video_file = video_files[i]
        base_name = os.path.splitext(video_file)[0]
        video_path = os.path.join(video_dir, video_file)
        gcsv_path = os.path.join(log_dir, base_name + ".gcsv")
        if os.path.exists(gcsv_path):
            clips = process_video(video_path, gcsv_path, output_dir, idx_prefix=str(i))
            j = 0
            while j < len(clips):
                all_clips.append(clips[j])
                j = j + 1
        else:
            print("No matching .gcsv for " + video_file)
        i = i + 1
    
    final_output = "output.mp4"
    combine_clips(all_clips, final_output)

if __name__ == "__main__":
    main()
