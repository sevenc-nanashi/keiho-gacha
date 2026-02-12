#!/usr/bin/env python3

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def normalize_caption(text: str) -> str:
    caption = normalize_text(text)
    if caption.startswith("（") and caption.endswith("）") and len(caption) >= 2:
        return caption[1:-1].strip()
    if caption.startswith("(") and caption.endswith(")") and len(caption) >= 2:
        return caption[1:-1].strip()
    return caption


def extract_articles(xml_path: Path) -> list[dict[str, str]]:
    root = ET.parse(xml_path).getroot()
    articles = root.findall(".//MainProvision//Article")

    results: list[dict[str, str]] = []
    for article in articles:
        title_element = article.find("ArticleTitle")
        if title_element is None:
            raise ValueError("ArticleTitle が見つからない Article があります。")

        title = normalize_text("".join(title_element.itertext()))
        if title == "":
            raise ValueError("空の ArticleTitle を検出しました。")

        caption = ""

        caption_element = article.find("ArticleCaption")
        if caption_element is not None:
            caption = normalize_caption("".join(caption_element.itertext()))

        sentences = []
        for sentence in article.findall(".//Sentence"):
            text = normalize_text("".join(sentence.itertext()))
            if text != "":
                sentences.append(text)

        if len(sentences) == 0:
            raise ValueError(f"{title} の本文が空です。")

        if sentences[0] == "削除":
            continue

        results.append(
            {"title": title, "caption": caption, "text": "\n".join(sentences)}
        )

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="./keiho.xml から { title, text } 形式の JSON を生成します。"
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path("./keiho.xml"),
        help="入力XMLファイルパス（既定: ./keiho.xml）",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="出力JSONファイルパス（省略時は標準出力）",
    )
    args = parser.parse_args()

    records = extract_articles(args.input)
    output_text = json.dumps(records, ensure_ascii=False, indent=2)

    if args.output is None:
        print(output_text)
        return

    args.output.write_text(output_text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
