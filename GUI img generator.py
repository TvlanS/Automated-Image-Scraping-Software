from tkinter import *
# for image downloading
from bs4 import BeautifulSoup
import requests, lxml, json
import glob
import os
import win32clipboard
import io
from PIL import Image 

def copy_image_to_clipboard(image_path):
    # Open the image
    image = Image.open(image_path)
    
    # Convert the image to BMP format and save it in memory
    output = io.BytesIO()
    image.convert("RGB").save(output, format="BMP")
    data = output.getvalue()[14:]  # Remove BMP header
    output.close()
    
    # Copy the image data to the clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def delete_contents_in_folder(folder_path):
    # Get all contents (files and subdirectories) in the folder
    contents = glob.glob(os.path.join(folder_path, "*"))
    
    for item in contents:
                print(item)
                os.remove(item)
                print(f"Deleted file: {item}")

# Example usage
folder_to_clear = "C:\\Users\\tvlan\\OneDrive\\Documents\\Python Files\\6.0 Image Generator\\2.0 Image dump folder"
# Replace this C:\\Users\\tvlan\\OneDrive\\Documents\\Python Files\\6.0 Image Generator\\2.0 Image dump folder
delete_contents_in_folder(folder_to_clear)


def download_images(query: str, num_images: int):

    query = query.lower().replace(" ", "_")  # Sanitize query for file naming
    print(query)
    #except:
      #  print("Invalid query")
       # pass###

    if "_" not in query :
         query = f"{query}_1"
         print(query)
    # Parameters for the search query
    params = {
        "q": query,
        "first": 1,
        "count": 5  # Number of images to fetch per request
    }
    
    # User-Agent header used to prevent raising suspicion on bing's side
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0 Safari/537.36"
    }
    
    count = 0  # Counter to track the number of downloaded images
    
    while count < num_images:
        # Perform the search query
        response = requests.get("https://www.bing.com/images/search", params=params, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, "lxml")
        
        # Iterate over image elements
        for url_element in soup.select(".iusc"):
    
            img_url = json.loads(url_element["m"])["murl"]
            image = requests.get(img_url, headers=headers, timeout=30)
            
            # Save the image
            if image.status_code == 200:
                count += 1
                with open(f"C:\\Users\\tvlan\\OneDrive\\Documents\\Python Files\\6.0 Image Generator\\2.0 Image dump folder\\{query}_image_{count}.jpg", 'wb') as file:
                    im1 = Image.open(io.BytesIO(image.content))
                    im2 = im1.resize((100, 100))
                    img_byte_arr = io.BytesIO()
                    try:
                        im2.save(img_byte_arr, format='JPEG')
                        img_byte_arr = img_byte_arr.getvalue()
                    except:
                         im2.save(img_byte_arr, format='PNG')
                         img_byte_arr = img_byte_arr.getvalue()
                    file.write(img_byte_arr)

                

                image_path = "C:/Users/tvlan/OneDrive/Documents/Python Files/6.0 Image Generator/2.0 Image dump folder/%s_image_%d.jpg" % (query, count)
                # Replace this C:/Users/tvlan/OneDrive/Documents/Python Files/6.0 Image Generator/2.0 Image dump folder/
                print(image_path)
               
                  
                print(f"Image {count} downloaded: {query}_image_{count}.jpg")
                
                # Stop if the desired number of images is reached
                if count >= num_images:
                    break
        
        # Update pagination for the next request
        params['first'] += params['count']
    
    if count == 0:
        print("No images were found for the query.")
    else:
        print(f"Successfully downloaded {count} image(s).")
    
    copy_image_to_clipboard(str(image_path))


def button_click():
    delete_contents_in_folder(folder_to_clear)
    query=searchfield.get()
    download_images(query,1)

def button_click_clear():
      searchfield.delete(0, END)

     


root = Tk()
root.title("Img Generator")

root.attributes("-topmost",1)

root.geometry("300x60+0+0") #(Width * Height + x position on screen + y position on screen)
#root.config(bg="black")
root.resizable(0,0)# Prevent the window from being resized

# Configure grid weights to allow dynamic resizing
root.grid_rowconfigure(0, weight=1)  # First row expands
root.grid_rowconfigure(1, weight=1)  # Second row expands
root.grid_columnconfigure(0, weight=1)  # First column expands
root.grid_columnconfigure(1, weight=1) 

searchfield = Entry(root,font=('aria',14,'bold'),bg='white',bd=2, relief='sunken') # bd is boarder
#searchfield.pack(fill="both",expand = True) 
searchfield.grid(row=0,column=0,columnspan=2,sticky="nsew") # pady is y axis padding

searchbutton = Button(root,text="Search",bg='lightgrey',command=button_click)
searchbutton.grid(row=1,column=0,sticky="nsew") #nsew expands the button to fill the window

searchbutton = Button(root,text="Clear",bg='lightgrey',command=button_click_clear)
searchbutton.grid(row=1,column=1,sticky="nsew")
root.mainloop() # Keep the window open , needs to be added
