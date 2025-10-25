import os
from multiprocessing import Process, Queue
from producer_consumer import producer_task, consumer_task


if __name__ == "__main__":
    producer_dir = "producer"  
    consumer_dir = "consumer"  
    
    os.makedirs(producer_dir, exist_ok=True)
    os.makedirs(consumer_dir, exist_ok=True)
    
    files = os.listdir(producer_dir)
    print(f"Files in producer directory: {files}\n")
    
    queue = Queue()
    
    producer = Process(target=producer_task, args=(queue, producer_dir))
    consumer = Process(target=consumer_task, args=(queue, consumer_dir))
    
    print("Starting processes...\n")
    
    producer.start()
    consumer.start()
    
    producer.join()
    consumer.join()
    total = len([
        f for f in os.listdir(consumer_dir) 
        if f.lower().endswith("-thumbnail.jpg")
    ])
    
    print(f"\n{total} images converted successfully!\n")
