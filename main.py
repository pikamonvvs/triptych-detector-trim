import re

import ffmpeg


def parse_results_file(file_path):
    """
    Parse the results.txt file to extract the video path and split time ranges.

    Args:
        file_path (str): Path to the results.txt file.

    Returns:
        tuple: (video_path, list of (start_time, end_time) tuples)
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # First line: Original video path
    video_path = lines[0].strip()

    # Extract time ranges (using regex)
    time_ranges = []
    time_pattern = re.compile(r"\('(\d{1,2}:\d{2}:\d{2})', '(\d{1,2}:\d{2}:\d{2})'\)")

    for line in lines[1:]:
        match = time_pattern.search(line)
        if match:
            start_time, end_time = match.groups()
            time_ranges.append((start_time, end_time))

    return video_path, time_ranges


def split_video(video_path, time_ranges, output_folder="output_clips"):
    """
    Split the original video into segments based on given time ranges.

    Args:
        video_path (str): Path to the original video file.
        time_ranges (list): List of tuples (start_time, end_time).
        output_folder (str): Folder to save the split video clips.
    """
    import os

    # Create output folder
    os.makedirs(output_folder, exist_ok=True)

    for i, (start_time, end_time) in enumerate(time_ranges):
        output_path = f"{output_folder}/clip_{i + 1}.mp4"
        (ffmpeg.input(video_path).output(output_path, ss=start_time, to=end_time, c="copy").run(overwrite_output=True, quiet=True))
        print(f"Saved: {output_path}")


if __name__ == "__main__":
    results_file = "continuous_intervals.txt"

    # Parse results file
    video_path, time_ranges = parse_results_file(results_file)
    print(f"Video path: {video_path}")
    print(f"Time ranges: {time_ranges}")

    # Execute video splitting
    split_video(video_path, time_ranges)
