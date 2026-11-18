# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/nemesisbug/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/nemesisbug/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

**The World in One Day** — the world news of Tuesday 17 November 2026 summed up in one 1024×1024 image (`entry.png`): a dense front page with a masthead, a world map with eight numbered flashpoints, a "By the numbers" strip, six lead story cards, and 27 more stories in three columns — 33 real stories in all.

The six leads: the Kerch Bridge partly collapses in a second Ukrainian strike · tankers mined near Hormuz as Gulf strikes spread · Xi, Trump and Putin to meet in Shenzhen · Trump lands in Manila for ASEAN and the Quad · Japan scrambles jets over Russian planes · Nvidia tops earnings amid the Huang exit drama. The 27 briefs run from the five-nation Rwanda return hub and the Houthis closing on Aden to the US losing measles-free status, the Siberian plane crash, COP31 stalling, and Raye leading the Grammy nominations. Every headline was verified against the 17 November 2026 editions of Reuters, AP, BBC, CNN, Al Jazeera and NYT.

This is v2 of the entry: v1 was an atlas board with six story cards (rank #1675, 97.01% dev win rate). The renewal rebuilds it as a dense front page in the pattern the leaderboard's top entries share, keeping v1's legibility — no overlap or clipping, crisp type, deterministic byte-identical reruns.

## How it was made

`build_image.py` (Python + Pillow, Liberation fonts) draws the whole board: masthead, equirectangular world map from public country outlines, numbered pins, stats strip, lead cards, brief columns, footer. The entry program itself is a one-line Node copy — the image in the repo is exactly what the judge sees.

## Run it

```sh
node main.ts
```

This copies `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default `/output`), refusing to finish if the copy differs in size from the source.

## License

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=w642jqgx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
