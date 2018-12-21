import re
import generatebook

class Chunk:
    def __init__(self, line):
        self.id = self.con = None
        id = re.search('id=\".*?\"', line)
        if id is not None:
            self.id = id.group()[4:-1]
        con = re.search('continue=\".*?\"', line)
        if con is not None:
            self.con = con.group()[10:-1]
        self.code = []

    def name(self):
        if re.search('_\d\d$', self.id):
            return self.id[1:-3]
        else:
            return self.id[1:]

    def keeper(self):
        return self.id is not None and self.id[0] == '_'

    def addline(self, line):
        self.code.append(line)

    def __str__(self):
        return "".join(self.code)

with open('docs/fullbook.md', 'r') as booklines:
    chunks = []
    chunking = False
    for line in booklines:
        if line[:9] == '```python':
            currentchunk = Chunk(line)
            if currentchunk.keeper():
                chunks.append(currentchunk)
                chunking = True
        elif line[:3] == '```':
            chunking = False
        elif chunking:
            currentchunk.addline(line)

chunks.sort(key = Chunk.name)
tangled = {}
for chunk in chunks:
    name = chunk.name()
    if name in tangled:
        tangled[name].append(chunk)
    else:
        tangled[name] = [chunk]

for name, chunklist in tangled.items():
    with open('code/' + name + '.py', 'w') as outfile:
        for chunk in chunklist:
            outfile.write(str(chunk))
            outfile.write("\n")
