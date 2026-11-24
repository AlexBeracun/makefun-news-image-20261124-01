# makefun-news-image-20261124-01

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/AlexBeracun/makefun-news-image-20261124-01/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/AlexBeracun/makefun-news-image-20261124-01/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image summing up Tuesday 24 November 2026's world news, as a
newspaper front page: "THE WORLD IN ONE PAGE" — 32 verified stories
across six continents.

Lead story: Iran says three oil tankers hit naval mines and caught fire
in the Strait of Hormuz — no ship names given, and the US has not
confirmed it. Then four feature panels (Russia's overnight strike on
Zaporizhzhia kills 2 and wounds 22, including two children; ousted
Bangladeshi PM Sheikh Hasina plans to fly home on 16 December after two
years in exile; Australia to fine tech firms up to 5% of global revenue
under its internet safety bill; CAS to rule today on Senegal's appeal
over its stripped Africa Cup of Nations title) plus 27 briefs: Qatar's
push to revive US–Iran talks, US sanctions on Iran's shadow banks,
Trump's call to speed up federal executions, the hush-money jurisdiction
bid, oil near a three-month low, Bangladesh's 50-million-child typhoid
drive, SoftBank's $2bn Intel bet, the Thai–Cambodia truce, strikes in
Gaza, and more. Every event happened or was first reported on
24 November 2026.

## How it is built

`gen_image.py` renders `entry.png` (1024×1024, Pillow + system fonts)
from the day's wire reports. `main.py` is the graded entry: Python 3.13,
standard library only, no network — it just copies `entry.png` to the
output directory, so two runs write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024x1024 PNG, under 1 MiB
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ajkq5baq&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
