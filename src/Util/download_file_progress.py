def download_file_with_progress(url: str):
    """
    This method downloads a file from the provided URL and displays download progress.
    """
    from os.path import join, exists
    from time import time
    import requests
    filename = url.split("/")[-1]
    file_path = join("downloaded_data", filename)

    # Check if the file already exists
    if exists(file_path):
        print(f"File {filename} already exists.")
        return

    start_time = time()

    # Download the file using requests library
    with requests.Session() as session:
        response = session.get(url, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            total_size = int(response.headers.get("content-length", 0))
            downloaded_size = 0

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        progress = downloaded_size / total_size * 100
                        download_speed = downloaded_size / (time() - start_time) / 1024  # KB/s
                        print(f"Downloading: {filename} - {progress:.2f}% | "
                              f"Speed: {download_speed:.2f} KB/s", end="\r")

            print(f"\nFile download completed: {filename}")
        else:
            print(f"Error downloading file. Response status code: {response.status_code}")
