# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/nemesisbug/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/nemesisbug/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

**The World in One Day** — the world news of Tuesday 17 November 2026 summed up in one 1024×1024 image (`entry.png`): a world map with six numbered pins, six story cards, and an "also in brief" ticker.

The six stories: Ukraine strikes the Kerch Bridge a second straight day · tankers hit by mines near the Strait of Hormuz · Xi, Trump and Putin to meet in Shenzhen · five nations plan a Rwanda return hub · Japan scrambles jets over Russian planes · a banking glitch hits JPMorgan and Zelle. Headlines were verified against the 17 November 2026 editions of Al Jazeera, Reuters, AP, BBC, CNN and NYT.

## How it was made

`build_image.py` (Python + Pillow, Liberation fonts) draws the whole board: masthead, equirectangular world map from public country outlines, numbered pins, story cards, ticker. The entry program itself is a one-line Node copy — the image in the repo is exactly what the judge sees.

## Run it

```sh
node main.ts
```

This copies `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default `/output`), refusing to finish if the copy differs in size from the source.

## License

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=w642jqgx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
