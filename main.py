import requests
import yaml
import argparse
from pprint import pprint
from urllib.parse import quote


parser = argparse.ArgumentParser()
parser.add_argument("queries", nargs="*")
parser.add_argument("-f", "--queries-file")


def typst_quote(value: str) -> str:
    return value.replace("//", "\\/\\/")


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
        if not card["nonfoil"]:
            continue

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
        prices = card.get("prices", {})
        price = prices.get("usd") or prices.get("usd_foil")

        if card.get("flavor_name"):
            title = f"{card['flavor_name']} #text(gray)[({title})]"
        if card["lang"] != "en" and card.get("printed_name"):
            title = f"{title} #text(gray)[({card['printed_name']})]"
        if price:
            title = f"{title} #text(gray)[(\\${price})]"
        output.append(
            f"- [ ] #text(gray)[\\#{str(card['collector_number']).zfill(4)}] {title}"
        )

    print(f"""
#import "@preview/cheq:0.4.0": checklist

#set page(columns: 2)
#set text(font: "IBM Plex Mono", size: 8pt)

#show: checklist

{typst_quote("\n".join(output))}""")


if __name__ == "__main__":
    args = parser.parse_args()
    queries = args.queries

    if args.queries_file:
        with open(args.queries_file) as f:
            queries = queries + yaml.safe_load(f)

    main(queries)
