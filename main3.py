import os
from tqdm import tqdm
from video_processor import process_video, combine_clips

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
            print(f"No matching .gcsv for {video_file}")

    final_output = "final_summary.mp4"
    combine_clips(all_clips, final_output)

if __name__ == "__main__":
    main()
