chapters = """00_overview.md 01_python.md 02_oop.md 02b_testing.md
            03_analysis.md 04_stacks_and_queues.md 05_deques_lls.md
            06_dlls.md 07_recursion.md 08_dynamic_programming.md
            09_searching.md 10a_sorting.md 10b_divide_and_conquer.md
            11_selection.md 12_mappings.md 13_trees.md 14_bsts.md
            15_balanced_bsts.md 16_priority_queues.md 17_graphs1.md
            18_graphs2.md""".split()

with open('prose/frontmatter.md', 'r') as fm:
    frontmatter = fm.read()

pagebreak = '<p style="page-break-after:always;"></p>'

def chapternumber(i):
    return """
    <a name="chapter_%02d"></a>
    <p style="font-size:80pt;color:#d0d0d0;font-weight:bold">
    Chapter %d
    </p>
    <hr/>\n\n""" % (i,i)

book = [frontmatter]

for i, chapter in enumerate(chapters):
    book.append(pagebreak)
    book.append(chapternumber(i))
    with open('prose/' + chapter, 'r') as booksection:
        book.append(booksection.read())

with open('docs/fullbook.md', 'w') as outfile:
    outfile.write("".join(book))
