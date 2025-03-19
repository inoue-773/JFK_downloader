import os
import requests
from tkinter import Tk
from tkinter.filedialog import askdirectory
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_file(url, dest_folder):
    """
    Downloads 10 files in parallel from the given URL to the destination folder.
    Shows a progress bar if the file size is available.
    """
    # Derive a local filename from the URL
    local_filename = url.split('/')[-1] or "downloaded_file"
    local_filepath = os.path.join(dest_folder, local_filename)
    
    try:
        # Stream the download to handle large files and update the progress bar
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error if the download fails

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  

        # Create a progress bar for the download
        progress_bar = tqdm(
            total=total_size, 
            unit='iB', 
            unit_scale=True, 
            desc=local_filename,
            leave=True  
        )
        
        with open(local_filepath, 'wb') as file:
            for chunk in response.iter_content(block_size):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))
        progress_bar.close()
        
        if total_size != 0 and progress_bar.n != total_size:
            print(f"Warning: Download may be incomplete for {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    
    return local_filepath

def main():
    # Initialize Tkinter and hide the main window
    root = Tk()
    root.withdraw()
    
 
    print("Select the destination folder for downloaded files...")
    dest_folder = askdirectory(title="Select Download Destination")
    if not dest_folder:
        print("No folder selected. Exiting the script.")
        return
    print(f"Files will be saved to: {dest_folder}\n")
    

    urls_file = "jfk_pdfs.txt"
    if not os.path.exists(urls_file):
        print(f"Error: '{urls_file}' not found. Please create this file with one URL per line.")
        return

    # Read each non-empty line from the file as a URL
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        print("No URLs found in the file.")
        return
    
    print(f"Found {len(urls)} URL(s) to download.\n")
    
    # Download files in parallel with up to 10 threads
    max_workers = 10
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(download_file, url, dest_folder): url for url in urls}
        
        # Process results as they complete
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                file_path = future.result()
                print(f"Downloaded {url} to {file_path}")
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
    
    print("\nAll downloads complete.")

if __name__ == '__main__':
    main()
