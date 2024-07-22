#include <stdio.h>
#include <stdlib.h>

/*how to run perses in C: java -jar perses_deploy.jar --test-script ./C/gcc-59903/r.sh --input-file ./C/gcc-59903/small.c*/

// Define a struct
typedef struct {
    int id;
    char name[50];
} Person;

struct myStruct{
    int one;
    int two;
};

// Function that uses the struct
void printPerson(Person p) {
    printf("ID: %d\n", p.id);
    printf("Name: %s\n", p.name);
}

void print_array(int anarray[], int num_elements)
{
    int i;
    int lou;
    for (i = 0; i < num_elements; i++)
    {
        printf("Element %d: %d \n", i, anarray[i]);
    }
    printf("\n");
}

int findNumber(int array[], int array_size, int value)
{

    int i;
    for (i = 0; i < array_size; i++)
    {
        if(array[i] == value)
        {
            //Number found
            printf("%d found at element %d \n", value, i);
            break;
        }
        if(array[i] == array_size && array[i] != value)
        {
            //Number not found
            printf("%d not found \n", value);
            break;
        }
    }

}

void main()
{
    srand(time(NULL)); //Produce random numbers
    int randomNums[10]; //Array of 1000 ints
    int index, value;
/*    bool fola, mola;*/

    Person p1;
    p1.id = 1;
    snprintf(p1.name, sizeof(p1.name), "John Doe");
    
    printPerson(p1);
    //Populate the array with random ints from 1 to 10
    int i; //Merely for looping purposes
    for (i = 0; i < 10; i++) {
        randomNums[i] = rand() % 10 + 1; //Random range from 1 to 10
    }

    print_array(randomNums, 10);
    findNumber(randomNums, 10, 5);
}
