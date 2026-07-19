import requests
import sys
from pprint import pprint
from urllib.parse import quote


def get_cards(query: str) -> list:
    def gen_url(page: int) -> str:
        return f"https://api.scryfall.com/cards/search?q={quote(query)}&order=set&unique=prints&page={page}"

    cards = []
    page = 1

    while True:
        url = gen_url(page)
        page += 1
        res = requests.get(url, headers={"User-Agent": "Script"})
        body = res.json()
        cards += body["data"]
        if not body["has_more"]:
            return cards


def main(queries: list[str]):
    output = []
    cards = [card for query in queries for card in get_cards(query)]
    printed_sets = set()
    for card in cards:
        set_name = card["set_name"]
        set_number = card["set"]
        if set_name not in printed_sets:
            printed_sets.add(set_name)
            if len(printed_sets) > 1:
                output.append("\n#pagebreak()\n")

            set_title = f"{set_name} ({set_number})"
            heading = f"""#counter(page).update(1)
#set page(footer: context [
  {set_title}
  #h(1fr)
  #counter(page).display(
    "1"
  )
])
#place(
    top + center,
    scope: "parent",
    float: true,
    pad(bottom: 2em, text(1.4em, weight: "bold")[
        {set_title}
    ]),
)
"""
            output.append(heading)
        title = card["name"]
        if "flavor_name" in card:
            title = f"{card['flavor_name']} (_{title}_)"
        if card["lang"] != "en" and "printed_name" in card:
            title = f"{title} ({card['printed_name']})"
        output.append(f"- [ ] \\#{card['collector_number']} {title}")

    print(f"""
#import "@preview/cheq:0.4.0": checklist

#set page(columns: 2)
#set text(font: "IBM Plex Mono", size: 8pt)

#show: checklist

{"\n".join(output)}""")


if __name__ == "__main__":
    main(sys.argv[1:])
