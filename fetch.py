#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor, as_completed
import re

import youtube_dl


def main():
    reg = re.compile(r"^<?(?P<url>\S+)>?\s(?P<name>.*)$")
    with open("00_todownload.md", "r") as f:
        lines = filter(lambda x: bool(x), map(lambda x: x.strip(), f.readlines()))

    with ThreadPoolExecutor() as executor:
        promises = {executor.submit(download, line, reg): line for line in lines}
        for future in as_completed(promises):
            line = promises[future]
            print(line, future.result())


def download(line, reg):
    options = {
        "format": "bestaudio/best",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    groups = reg.match(line)
    print(f"start download of {groups['name']}")
    options["outtmpl"] = groups["name"] + ".%(ext)s"
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([groups["url"]])
        print(f"finished download of {groups['name']}")


if __name__ == "__main__":
    main()

