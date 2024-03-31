import os
from langchain_community.document_loaders import YoutubeLoader
from modules.url_mapping import save_mapping

def write_video_content_to_file(url):
    try:
        # Extract page_content and title from the provided data
        loader = YoutubeLoader.from_youtube_url(
            url, add_video_info=True
        )
        data = loader.load()
        page_content = data[0].page_content
        title = data[0].metadata["title"]
        
        # Generate a file name from the title (remove spaces and special characters)
        file_name = ''.join(char if char.isalnum() else '_' for char in title)
        file_name += "_yt.txt"  # Add the ".txt" extension
        file_path = os.path.join("../python-server/files", file_name)
        
        # Write the page_content to a file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(page_content)
        
        print(f"saved transcript '{title}'")
        save_mapping(file_name,url)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# # Example usage:
# data = {
#     "page_content": "To understand our user's experiences...",
#     "metadata": {
#         "title": "Probing in User Interviews",
#         # Other metadata fields
#     }
# }