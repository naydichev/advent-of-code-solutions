#!/usr/bin/python

class TreeNode:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def __repr__(self):
        return "%s(children=%s, metadata=%s)" % (self.__class__.__name__, self.children, self.metadata)

def main():
    with open("license.pi") as f:
        license = f.read()

        license_digits = [int(i) for i in license.split()]

        tree = extract_children(license_digits, 0)[0]

        metadata = extract_metadata(tree)

        print("The file check is %d" % sum(metadata))

def extract_children(digits, current_index):
    nodes = []
    num_children = digits[current_index]
    num_metadata = digits[current_index + 1]
    current_index += 2
    for i in range(num_children):
        child_node, current_index = extract_children(digits, current_index)

        nodes.append(child_node)

    metadata = digits[current_index:current_index + num_metadata]
    return TreeNode(nodes, metadata), current_index + num_metadata


def extract_metadata(tree):
    metadata = []
    metadata.extend(tree.metadata)

    for child in tree.children:
        metadata.extend(extract_metadata(child))

    return metadata

if __name__ == "__main__":
    main()
