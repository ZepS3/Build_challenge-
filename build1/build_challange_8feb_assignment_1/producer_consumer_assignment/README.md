# Producer-Consumer Assignment

Here is my solution for the producer-consumer problem using Python. 
I implemented a shared queue with a capacity of 10 items as required. The producer threads add items and consumer threads remove them, using condition variables to make sure they wait properly when the queue is full or empty.

## How to Run

You can run the main program like this:

```bash
python main.py
```

It will show the producer creating items and the consumer processing them.

## Testing

I also wrote some unit tests to check if the queue logic works. You can run them with:

```bash
python -m unittest discover tests
```

## My Approach 

- **Queue**: I used `threading.Condition` because it seemed like the best way to handle the waiting logic.
- **Classes**: created separate classes for Producer, Consumer and the SharedQueue to keep things organized.
- **Stopping**: The threads stop gracefully when all items are done.


