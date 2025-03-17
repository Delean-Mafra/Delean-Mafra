class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def inorder_traversal(root):
    if root is not None:
        inorder_traversal(root.left)
        print(root.key, end=' ')
        inorder_traversal(root.right)

# Exemplo de uso
root = Node(5)
root.left = Node(3)
root.right = Node(7)
root.left.left = Node(2)
root.left.right = Node(5)
root.right.right = Node(8)

inorder_traversal(root)
