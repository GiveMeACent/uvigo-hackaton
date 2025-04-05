import os
import subprocess

# Constants
FPS = 60
SEGMENT_SECONDS = 5
WINDOW = SEGMENT_SECONDS * FPS  # 60 FPS * 5 seconds = 300 frames

def parse_gcsv(file_path):
    f = open(file_path, "r")
    lines = f.readlines()
    f.close()

    data_gcsv = []
    # Skip the first 16 lines (header)
    gcsvs = lines[16:]
    # Process each line simply
    for gcsv in gcsvs:
        # Split the line by comma
        gcsvData = gcsv.split(",")
        # Append rx, ry, rz values (as strings; will convert later)
        data_gcsv.append([gcsvData[1], gcsvData[2], gcsvData[3]])
    return data_gcsv

def score_segments(data):
    # Create an empty list for scores
    scores = []
    total_frames = len(data)
    # Loop through the data from frame 0 to (total_frames - WINDOW)
    i = 0
    while i < total_frames - WINDOW:
        # Calculate the motion for a 5-second window
        motion = 0.0
        j = i
        while j < i + WINDOW:
            # For each value in the current frame's list (rx, ry, rz)
            k = 0
            while k < len(data[j]):
                # Convert the value to float, take absolute value, and add to motion
                motion += abs(float(data[j][k]))
                k = k + 1
            j = j + 1
        # Append the start index and its motion score as a tuple
        scores.append((i, motion))
        i = i + 1
    # Sort the scores in descending order of motion
    # We use a simple sorting algorithm here for clarity.
    sorted_scores = sorted(scores, key=lambda item: item[1], reverse=True)
    return sorted_scores

def select_top_segments(scored, min_distance):
    selected = []
    # Loop through each tuple in the scored list
    i = 0
    while i < len(scored):
        idx, score = scored[i]
        if len(selected) == 0:
            # If none selected yet, add the first one
            selected.append((idx, score))
        else:
            # Check if the current index is far enough from the last selected segment
            last_index = selected[-1][0]
            if idx - last_index >= min_distance:
                selected.append((idx, score))
        # Stop when we have selected 3 segments
        if len(selected) == 3:
            break
        i = i + 1
    return selected

def extract_clip(video_path, start_frame, output_path):
    # Calculate start time in seconds
    start_time = start_frame / FPS
    # Build the ffmpeg command to extract a clip
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-i", video_path,
        "-t", str(SEGMENT_SECONDS),
        "-c", "copy",
        output_path
    ]
    # Run the command quietly
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_video(video_path, gcsv_path, output_dir, idx_prefix):
    print("Processing: " + os.path.basename(video_path))
    # Parse the gcsv file to get motion data
    data = parse_gcsv(gcsv_path)
    print("Scoring segments...")
    scored = score_segments(data)
    # Use WINDOW as the minimum distance (i.e. no overlap)
    selected = select_top_segments(scored, WINDOW)
    
    clips = []
    i = 0
    while i < len(selected):
        start_idx = selected[i][0]
        # Create output file name
        out_name = idx_prefix + "_clip" + str(i+1) + ".mp4"
        out_path = os.path.join(output_dir, out_name)
        print("Extracting clip " + str(i+1) + ": starts at frame " + str(start_idx) +
              " (" + "{:.2f}".format(start_idx/FPS) + "s)")
        extract_clip(video_path, start_idx, out_path)
        clips.append(out_path)
        i = i + 1
    return clips

def combine_clips(clip_paths, output_path):
    print("Combining clips into final summary video...")
    # Create a temporary file that lists all clip paths.
    f = open("clips.txt", "w")
    i = 0
    while i < len(clip_paths):
        # Write the absolute path for each clip, one per line
        f.write("file '" + os.path.abspath(clip_paths[i]) + "'\n")
        i = i + 1
    f.close()
    
    # Build ffmpeg command to concatenate clips.
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "clips.txt",
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd)
    # Remove the temporary file.
    os.remove("clips.txt")
    print("Summary video created: " + output_path)

def main():
    # Set the directories
    video_dir = "/home/flamingfury/media/2aad:6371/videos/"
    log_dir = "/home/flamingfury/media/2aad:6371/gcsv/"
    output_dir = "/home/flamingfury/media/2aad:6371/output/"

    # Create the output directory if it doesn't exist.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_clips = []
    # Get the list of video files from the video directory.
    files = os.listdir(video_dir)
    # Create an empty list for video files.
    video_files = []
    i = 0
    while i < len(files):
        if files[i].endswith(".MP4"):
            video_files.append(files[i])
        i = i + 1
    # Sort the video files
    video_files.sort()

    # Process each video file.
    i = 0
    while i < len(video_files):
        video_file = video_files[i]
        # Get the base name of the file (without extension)
        base_name = os.path.splitext(video_file)[0]
        video_path = os.path.join(video_dir, video_file)
        gcsv_path = os.path.join(log_dir, base_name + ".gcsv")
        if os.path.exists(gcsv_path):
            # Process the video using its corresponding gcsv file.
            clips = process_video(video_path, gcsv_path, output_dir, idx_prefix=str(i))
            j = 0
            while j < len(clips):
                all_clips.append(clips[j])
                j = j + 1
        else:
            print("No matching .gcsv for " + video_file)
        i = i + 1

    # Combine all extracted clips into one summary video.
    final_output = "snippet.mp4"
    combine_clips(all_clips, final_output)

if __name__ == "__main__":
    main()
