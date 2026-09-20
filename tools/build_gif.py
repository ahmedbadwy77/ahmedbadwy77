"""One-shot helper: download the source GIF and write a profile-sized version."""
import os
import urllib.request

from PIL import Image, ImageSequence

URL = (
    "https://autoglm-oss.z.ai/auto_fly/3ed4oh_20260920-235426-77117af1-3da-volibear.gif"
    "?auth_key=1789937735-0-0-7e78928b72550fb775894703b5c661e1"
)
SRC = "/tmp/src.gif"
OUT = "assets/volibear.gif"
WIDTH = 360
STEP = 2
COLORS = 96


def main():
    os.makedirs("assets", exist_ok=True)
    urllib.request.urlretrieve(URL, SRC)

    im = Image.open(SRC)
    durations, frames = [], []
    for frame in ImageSequence.Iterator(im):
        durations.append(frame.info.get("duration", im.info.get("duration", 60)) or 60)
        frames.append(frame.convert("RGB"))

    w = WIDTH
    h = round(frames[0].height * WIDTH / frames[0].width)
    idx = list(range(0, len(frames), STEP))
    out = [
        frames[i].resize((w, h), Image.LANCZOS).convert("P", palette=Image.ADAPTIVE, colors=COLORS)
        for i in idx
    ]
    delays = [durations[i] * STEP for i in idx]
    out[0].save(
        OUT,
        save_all=True,
        append_images=out[1:],
        duration=delays,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print("wrote %s (%d bytes, %dx%d, %d frames)" % (OUT, os.path.getsize(OUT), w, h, len(out)))


if __name__ == "__main__":
    main()
