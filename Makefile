.PHONY: default run view clean

default: view

run:
	uv run main.py -f queries.yml

output.typ: main.py queries.yml
	uv run main.py -f queries.yml > output.typ

output.pdf: output.typ
	typst compile output.typ

view: output.pdf
	xdg-open output.pdf

clean:
	rm output.typ output.pdf
