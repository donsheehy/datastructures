SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docsource
BUILDDIR      = docsource/build
MD:= $(wildcard prose/*.md)
TANGLED:= $(MD:prose/%.md=ds2/.tangled%)
GENERATEDTEX:= $(MD:prose/%.md=tex/generated/%.tex)
TEX = tex/main.tex tex/generated/pygments_macros.tex tex/titlepage.tex
# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile test docs pdf clean weave tangle

test: tangle
	nosetests --with-coverage

docs:	Makefile
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@cp -a docsource/build/html/. docs/

html: docs

tex/generated/pygments_macros.tex :
	prosecode styledefs --outfile tex/generated/pygments_macros.tex

tex/generated/%.tex: prose/%.md
	prosecode weave $< --outfile $@ --execute

ds2/.tangled% : prose/%.md
	prosecode tangle $< --srcdir ds2/
	@touch $@

tangle: $(TANGLED)

clean:
	$(foreach mdfile, $(MD), prosecode cleanup $(mdfile) --srcdir ds2/;)
	rm tex/generated/*
	rm tex/fullbook.*
	rm ds2/.tangled*

weave: $(GENERATEDTEX)

pdf: $(GENERATEDTEX) $(TEX)
	cd tex; pdflatex -jobname=fullbook main.tex
