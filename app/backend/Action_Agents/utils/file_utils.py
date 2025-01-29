import os
import base64
import httpx
def load_image(image_path):
    try:
         if image_path.startswith("http://") or image_path.startswith("https://"):
                image = httpx.get(image_path)
                image_data = image.content
         else:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
         image_base64 = base64.b64encode(image_data).decode("utf-8")
         return image_base64
    except Exception as e:
          print(f"Error loading image: {e}")
          return None


def save_to_file(filename, content):
      try:
            with open(filename, "w") as f:
                  f.write(content)
            return True
      except Exception as e:
            print(f"Error saving to file {e}")
            return False
