class TreeBuilder:
    def build(self, files):
        tree = {}

        for item in files:
            path = item["path"].split("/")
            current = tree

            for part in path[:-1]:
                current = current.setdefault(part, {})

            current[path[-1]] = {}

        return tree
