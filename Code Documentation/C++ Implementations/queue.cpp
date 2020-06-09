using namespace std;

struct Queue 
{ 
    // Initialize front and rear 
    int rear, front; 
  
    // Circular Queue 
    int size;
    int maxSize; 
    int *arr; 
  
    Queue(int max) 
    { 
       front = rear = -1; 
       size = 0; 
       maxSize = max;
       arr = new int[s]; 
    } 
  
    void enQueue(int value); 
    int deQueue(); 
    void displayQueue();
    int numElements();
    bool isFull();

}; 

/* Function to create Circular queue */
void Queue::enQueue(int value) 
{ 
    if ((front == 0 && rear == maxSize-1) || 
            (rear == (front-1)%(maxSize-1))) 
    { 
        printf("\nQueue is Full"); 
        return; 
    } 
  
    else if (front == -1) /* Insert First Element */
    { 
        front = rear = 0; 
        arr[rear] = value; 
    } 
  
    else if (rear == maxSize-1 && front != 0) 
    { 
        rear = 0; 
        arr[rear] = value; 
    } 
  
    else
    { 
        rear++; 
        arr[rear] = value; 
    } 
} 
  
// Function to delete element from Circular Queue 
int Queue::deQueue() 
{ 
    if (front == -1) 
    { 
        printf("\nQueue is Empty"); 
        return INT_MIN; 
    } 
  
    int data = arr[front]; 
    arr[front] = -1; 
    if (front == rear) 
    { 
        front = -1; 
        rear = -1; 
    } 
    else if (front == size-1) 
        front = 0; 
    else
        front++; 
  
    return data; 
} 

void Queue::displayQueue() 
{ 
    if (front == -1) 
    { 
        printf("\nQueue is Empty"); 
        return; 
    } 
    printf("\nElements in Circular Queue are: "); 
    if (rear >= front) 
    { 
        for (int i = front; i <= rear; i++) 
            printf("%d ",arr[i]); 
    } 
    else
    { 
        for (int i = front; i < size; i++) 
            printf("%d ", arr[i]); 
  
        for (int i = 0; i <= rear; i++) 
            printf("%d ", arr[i]); 
    } 
}

int Queue::numElements()
{
    return size;
}

bool Queue::isFull()
{
    if (size == maxSize) return true;
    return false;
}