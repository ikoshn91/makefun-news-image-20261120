# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/ikoshn91/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/ikoshn91/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page newspaper front page summing up Friday 20 November 2026's
world news, for make.fun's "Sum up 20 November's world news in one image"
bounty ($250 in USDC, 50 places paid).

## The image

`entry.png` (1024×1024, ~118 KB) is "THE WORLD TODAY — Friday 20 November
2026": a front page with six stories from the day, drawn programmatically
with Python Pillow (`gen_image.py`), so every word is pixel-perfect text —
no AI image generation, no downloaded pictures.

- **Lead — Ukraine:** Russia strikes Kyiv in a massive overnight
  missile-and-drone attack, hours after the Shenzhen summit; at least 5
  killed, 3 Dnipro bridges hit, the power grid "extremely critical".
- **North Korea:** Pyongyang fires a ballistic missile into the Sea of
  Japan (South Korea's military, Friday morning).
- **The Hague:** the World Court rules Myanmar committed genocide against
  the Rohingya — a first such finding against a state.
- **Shenzhen:** Trump, Xi and Putin sign a joint peace declaration after
  their first three-way summit.
- **Markets:** Asian markets plunge on AI-bubble fears — Taiwan's index
  sheds 2,200+ points in a day; Japan's Nikkei falls 4.8%.
- **Also today:** a migrant boat sinks off Senegal (dozens missing), a Van
  Gogh sells for $190.4m (an artist record), Kenya discharges its last
  Ebola patient.

Sources: CNN, Reuters, Le Monde, AP — reports published 20 November 2026.

## The program

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. No network, no randomness: two runs write the same
bytes. Regenerate the image with `python3 gen_image.py` (needs Pillow);
verify determinism with `sha256sum` across two runs.

## License

MIT — see LICENSE.
