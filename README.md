# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/junod1908/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/junod1908/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Sum up 22 November 2026's world news in one image — a one-page pictorial broadsheet, "The World in One Day": painted hero panels (the Las Vegas Grand Prix under the lights, COP31 in Antalya, the Ashes in Perth), a dense dot world map with red markers at the stories' places, and 19 numbered story cards across regions and fields. Every story was date-audited to Sunday 22 November 2026 — the poster's date line says so on its face. The program draws the whole page itself with the Python standard library only (no network): the hero panels are painted illustrations composited in from `assets/`, and every word on the page is set in type by the program from the bitmap fonts in `assets/font.bin`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
