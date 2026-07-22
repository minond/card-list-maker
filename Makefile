.PHONY: default run view clean

RUN := uv run main.py -f queries.yml

default: view

run:
	$(RUN)

output.typ: main.py queries.yml
	$(RUN) > output.typ

output.pdf: output.typ
	typst compile output.typ

view: output.pdf
	xdg-open output.pdf

clean:
	rm -f output.typ output.pdf
