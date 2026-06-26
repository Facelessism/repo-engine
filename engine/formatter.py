class TreeFormatter:
    def format(self, name, tree):
        print(f"{name}/")
        self._walk(tree)

    def _walk(self, node, prefix=""):
        items = list(node.items())

        for index, (name, children) in enumerate(items):
            last = index == len(items) - 1
            branch = "└── " if last else "├── "

            print(prefix + branch + name)

            if children:
                extension = "    " if last else "│   "
                self._walk(children, prefix + extension)
