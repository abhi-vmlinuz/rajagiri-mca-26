#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME 50

typedef struct Node
{
    char name[MAX_NAME];
    struct Node *left;
    struct Node *right;
} Node;

Node *create_node(const char *name)
{
    Node *node = malloc(sizeof(Node));

    if (node == NULL)
    {
        printf("Memory allocation failed.\n");
        return NULL;
    }

    strcpy(node->name, name);
    node->left = NULL;
    node->right = NULL;

    return node;
}

Node *insert(Node *root, const char *name)
{
    if (root == NULL)
    {
        return create_node(name);
    }

    if (strcmp(name, root->name) < 0)
    {
        root->left = insert(root->left, name);
    }
    else if (strcmp(name, root->name) > 0)
    {
        root->right = insert(root->right, name);
    }

    return root;
}

void inorder(Node *root)
{
    if (root == NULL)
    {
        return;
    }

    inorder(root->left);
    printf("%s ", root->name);
    inorder(root->right);
}

void free_tree(Node *root)
{
    if (root == NULL)
    {
        return;
    }

    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

int main(void)
{
    Node *root = NULL;

    root = insert(root, "Ravi");
    root = insert(root, "Anu");
    root = insert(root, "Kiran");
    root = insert(root, "Bala");
    root = insert(root, "Deepa");
    root = insert(root, "Cathy");

    printf("Names in ascending order: ");
    inorder(root);
    printf("\n");

    free_tree(root);

    return 0;
}
