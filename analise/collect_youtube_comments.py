"""Coleta comentários de um vídeo do YouTube para análise posterior."""

import argparse
import os
from pathlib import Path

import pandas as pd
from googleapiclient.discovery import build


DEFAULT_VIDEO_ID = "9LIJHRkvOo4"
OUTPUT_PATH = Path(__file__).resolve().parent / "youtube_comments.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exporta comentários públicos de um vídeo do YouTube para CSV."
    )
    parser.add_argument("--video-id", default=DEFAULT_VIDEO_ID)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    if not os.environ.get("YOUTUBE_API_KEY"):
        parser.error("defina YOUTUBE_API_KEY no ambiente antes de executar o coletor")
    return args


def collect_comments(video_id: str, api_key: str) -> list[dict[str, object]]:
    youtube = build("youtube", "v3", developerKey=api_key)
    comments: list[dict[str, object]] = []
    next_page_token = None

    while True:
        response = (
            youtube.commentThreads()
            .list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText",
                order="time",
            )
            .execute()
        )

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]
            data = comment["snippet"]
            comments.append(
                {
                    "comment_id": comment["id"],
                    "author": data.get("authorDisplayName"),
                    "text": data.get("textDisplay"),
                    "published_at": data.get("publishedAt"),
                    "like_count": data.get("likeCount"),
                    "reply_count": item["snippet"]["totalReplyCount"],
                    "video_id": video_id,
                }
            )

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return comments


def main() -> None:
    args = parse_args()
    comments = collect_comments(args.video_id, os.environ["YOUTUBE_API_KEY"])
    dataframe = pd.DataFrame(
        comments,
        columns=[
            "comment_id",
            "author",
            "text",
            "published_at",
            "like_count",
            "reply_count",
            "video_id",
        ],
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(args.output, index=False, encoding="utf-8-sig")

    print(f"Total coletado: {len(dataframe)} comentários")
    print(f"Arquivo salvo: {args.output}")


if __name__ == "__main__":
    main()
