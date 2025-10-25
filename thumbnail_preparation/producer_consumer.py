import os
import io
from PIL import Image
from multiprocessing import Process, Queue


def producer_task(queue, producer_dir):
    processed_count = 0
    supported_formats = ('.jpg', '.jpeg', '.png')
    
    for filename in os.listdir(producer_dir):
        if not filename.lower().endswith(supported_formats):
            continue
            
        file_path = os.path.join(producer_dir, filename)
        
        try:
            with Image.open(file_path) as img:
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGB")                
                img.thumbnail((128, 128), Image.LANCZOS)
                buffer = io.BytesIO()
                if filename.lower().endswith('.png'):
                    img.save(buffer, format='PNG', optimize=True)
                else:
                    img.save(buffer, format='JPEG', quality=95, optimize=True)
                img_bytes = buffer.getvalue()
                queue.put((filename, img_bytes))
                processed_count += 1
                print(f" Producer: '{filename}' processed into thumbnail.")
                
        except Exception as e:
            print(f" Producer: Failed to process '{filename}'. Error: {e}")
    
    queue.put(None)
    print(f" Producer finished. Total images processed: {processed_count}\n")


def consumer_task(queue, consumer_dir):
    saved_count = 0
    
    while True:
        item = queue.get()
        
        if item is None:
            print(f" Consumer finished. Total thumbnails saved: {saved_count}\n")
            break
        
        filename, img_bytes = item
        
        base_name, _ = os.path.splitext(filename)
        save_path = os.path.join(consumer_dir, f"{base_name}-thumbnail.jpg")
        
        try:
            with open(save_path, "wb") as f:
                f.write(img_bytes)
            
            saved_count += 1
            print(f" Consumer: Thumbnail saved as '{save_path}'")
            
        except Exception as e:
            print(f" Consumer: Failed to save '{filename}'. Error: {e}")
