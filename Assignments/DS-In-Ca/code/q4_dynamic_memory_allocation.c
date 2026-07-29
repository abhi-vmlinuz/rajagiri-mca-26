#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("=== 1. DEMONSTRATING MALLOC ===\n");
    // Allocate space for 3 integers (uninitialized / contains garbage)
    int *numbers = (int *)malloc(3 * sizeof(int));

    if (numbers == NULL) {
        fprintf(stderr, "malloc failed!\n");
        return 1;
    }

    // Assign values using pointer dereferencing syntax *(ptr + i)
    *(numbers + 0) = 10;
    *(numbers + 1) = 20;
    *(numbers + 2) = 30;

    printf("malloc array elements: ");
    for (int i = 0; i < 3; i++) {
        printf("%d ", numbers[i]); // Using bracket sugar
    }
    printf("\n\n");


    printf("=== 2. DEMONSTRATING CALLOC ===\n");
    // Allocate space for 3 integers and auto-zero every byte
    int *zeroed_arr = (int *)calloc(3, sizeof(int));

    if (zeroed_arr == NULL) {
        fprintf(stderr, "calloc failed!\n");
        free(numbers); // Clean up previously allocated memory before exiting
        return 1;
    }

    printf("calloc array elements (automatically zeroed): ");
    for (int i = 0; i < 3; i++) {
        printf("%d ", zeroed_arr[i]);
    }
    printf("\n\n");

    // We are done with calloc memory, release it with free()
    free(zeroed_arr);
    zeroed_arr = NULL;


    printf("=== 3. DEMONSTRATING REALLOC ===\n");
    printf("Expanding 'numbers' array from 3 elements to 5 elements...\n");

    // Use a temporary pointer to safely resize the malloc'd memory block
    int *temp = (int *)realloc(numbers, 5 * sizeof(int));

    if (temp != NULL) {
        numbers = temp; // Reassignment safe!

        // Assign values to the 2 newly added slots
        numbers[3] = 40;
        numbers[4] = 50;

        printf("Resized array elements: ");
        for (int i = 0; i < 5; i++) {
            printf("%d ", numbers[i]);
        }
        printf("\n\n");
    } else {
        fprintf(stderr, "realloc failed! Original memory intact.\n");
    }


    printf("=== 4. DEMONSTRATING FREE ===\n");
    // Release the expanded memory back to the system
    free(numbers);
    numbers = NULL; // Prevent dangling pointer
    
    printf("Memory freed successfully.\n");

    return 0;
}
