class TreeFormatter:
    def format(self, name, tree, analysis=None):
        lines = [f"{name}/"]
        self._walk(tree, lines)

        result = {
            "name": name,
            "tree": tree,
            "formatted_tree": "\n".join(lines),
        }

        if analysis:
            result.update(analysis)

        return result

    def _walk(self, node, lines, prefix=""):
        items = list(node.items())

        for index, (name, children) in enumerate(items):
            last = index == len(items) - 1
            branch = "└── " if last else "├── "

            lines.append(prefix + branch + name)

            if children:
                extension = "    " if last else "│   "
                self._walk(children, lines, prefix + extension)
