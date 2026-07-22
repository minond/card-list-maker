.PHONY: default run compile view

queries := \
		   "set:sta" \
		   "set:soa" \
		   "set:fca" \
		   "set:dft cn>=333 cn=<346" \
		   "set:dft cn>=532 cn<=545"

default: run compile view

run:
	uv run main.py $(queries) > output.typ

compile:
	typst compile output.typ

view:
	xdg-open output.pdf
