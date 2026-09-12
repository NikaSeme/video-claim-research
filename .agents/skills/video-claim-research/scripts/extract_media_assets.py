#!/usr/bin/env python3
"""Extract audio, sampled frames, and metadata from a local video file."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

ALLOWED_VIDEO_SUFFIXES = {
    ".3gp",
    ".avi",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpeg",
    ".mpg",
    ".webm",
}


def portable_path(path: Path, root: Path) -> str:
    """Return a commit-safe path without exposing a contributor's home directory."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def run(command: list[str]) -> None:
    if not command or not all(isinstance(part, str) and part for part in command):
        raise ValueError("Command must be a non-empty list of non-empty strings.")
    subprocess.run(command, check=True, shell=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", help="Local video file.")
    parser.add_argument("topic_dir", help="Topic directory under materials used/topics.")
    parser.add_argument("--every-seconds", type=int, default=5, help="Sample one frame every N seconds.")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise SystemExit("ffmpeg and ffprobe are required for media extraction.")

    video = Path(args.video).resolve()
    topic_dir = Path(args.topic_dir).resolve()
    working_root = Path.cwd().resolve()
    if not video.exists():
        raise SystemExit(f"Video not found: {video}")
    if not video.is_file():
        raise SystemExit(f"Video path is not a file: {video}")
    if video.suffix.lower() not in ALLOWED_VIDEO_SUFFIXES:
        raise SystemExit(f"Unsupported video extension: {video.suffix or '(none)'}")

    audio_dir = topic_dir / "audio"
    frames_dir = topic_dir / "frames"
    evidence_dir = topic_dir / "evidence"
    for directory in [audio_dir, frames_dir, evidence_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    metadata_path = evidence_dir / "ffprobe.json"
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(video)],
        check=True,
        shell=False,
        capture_output=True,
        text=True,
    )
    metadata = json.loads(result.stdout)
    if isinstance(metadata.get("format"), dict) and "filename" in metadata["format"]:
        metadata["format"]["filename"] = portable_path(video, working_root)
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    audio_path = audio_dir / "audio.wav"
    run(["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(audio_path)])

    frame_pattern = frames_dir / "frame_%04d.jpg"
    fps_filter = f"fps=1/{max(args.every_seconds, 1)}"
    run(["ffmpeg", "-y", "-i", str(video), "-vf", fps_filter, str(frame_pattern)])

    summary = evidence_dir / "media-assets.md"
    summary.write_text(
        "\n".join(
            [
                "# Media Assets",
                "",
                f"- Source video: `{portable_path(video, working_root)}`",
                f"- Metadata: `{portable_path(metadata_path, working_root)}`",
                f"- Audio: `{portable_path(audio_path, working_root)}`",
                f"- Frame pattern: `{portable_path(frame_pattern, working_root)}`",
                f"- Frame sampling: one frame every {max(args.every_seconds, 1)} seconds",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
