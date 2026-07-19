.PHONY: default run compile view

default: run compile view

run:
	uv run main.py set:sta set:soa set:fca > output.typ

compile:
	typst compile output.typ

view:
	xdg-open output.pdf
