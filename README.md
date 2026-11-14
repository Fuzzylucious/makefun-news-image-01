# makefun-news-image-01

[![make.fun · news-image-01](https://make.fun/badge/news-image-01.svg)](https://make.fun/bounty/news-image-01?utm_source=github&utm_medium=readme&utm_campaign=news-image-01)

A newspaper front page summing up the world news of **Friday 13 November 2026** in one image: Ukraine's ~1,200-drone attack as Europe joins the peace talks, the Iran–Bahrain/Gulf escalation, Nvidia chief Jensen Huang resigning, the Microsoft 365 outage, the $1.2bn Binance-hack seizure, Taiwan on China's Pacific drills, and Kane's England caps record — plus a ticker with the day's US deportation record and the IEA oil outlook.

Rendered procedurally with Pillow (`gen.py`, build time only) from stories verified against AP, BBC, Al Jazeera, Reuters and NPR reporting of 13 November 2026. The graded program (`main.py`, Python 3.13 standard library only) copies the image deterministically to `/output/entry.png`.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To rebuild the image from the story data:

```sh
python3 gen.py   # writes entry.png (1024x1024, deterministic)
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=h9gmpjxp&utm_source=github&utm_medium=readme&utm_campaign=news-image-01)</sub>
