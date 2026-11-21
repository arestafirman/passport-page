# Republic of Zalvara — The Passport Page of a Country That Isn't There

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/arestafirman/passport-page/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/arestafirman/passport-page/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

A passport spread for the **Republic of Zalvara — the White Salt Sea**, a fictional
salt-flat republic. Holder: **Mira Keth, Salt Caravan Master**.

The spread shows a classic burgundy-and-gold data page (drawn portrait, bilingual
Zalvaran/English fields, signature, MRZ strip), a small map of the dry-season salt
road, and entry stamps from four neighbouring states — every stamp dated **after**
the passport's issue date of 12 Mar 2024, so the travel history is consistent.

The revealing paperwork detail is in the CONDITIONS box: the passport is valid
for the dry-season salt road only, entry by caravan permit, fee **40 salt-koruna,
paid in kind — two sacks of white salt, weighed at the Korvath Gate. No coin
accepted.**

## Run

```sh
python3 generate_image.py   # renders entry.png (1024x1024, deterministic)
node main.ts                # copies entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

`generate_image.py` is fully deterministic (no network, no clock, no randomness):
rendering twice produces a byte-identical `entry.png`.
