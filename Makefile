# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docsource
BUILDDIR      = docsource/build

MD:= $(wildcard prose/*.md)
TEX:= $(MD:prose/%.md=prose/tex/%.tex)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile github test docs pdf clean

github:
	@make docs
	@cp -a docsource/build/html/. docs/

test:
	nosetests --with-coverage

docs:	Makefile
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

prose/tex/%.tex: prose/%.md
	prosecode tangle $< --srcdir ds2/
	prosecode weave $< --outfile $@

clean:
	rm prose/tex/fullbook.*

pdf: $(TEX) prose/tex/main.tex
	cd prose/tex; pdflatex -jobname=fullbook main.tex

# %: prose/%.md
# 	prosecode tangle $< --srcdir ds2/
# 	prosecode weave $< --outfile prose/tex/$@.tex

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# %: Makefile
# 	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
