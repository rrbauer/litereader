# litereader
A Python script to download stories from Literotica

Litereader will download stories from the erotic fiction website, Literotica. Given a URL to the story's first page, it will fetch the contents, including multiple pages and illustrations/images. It saves the content as a single html file, with links to the original story on Literotica, and local links to any downloaded illustrations/images.

It's handy for saving a copy of your favorite stories, for reading again later.

The illustrations/images (if applicable) are saved to a directory with the same name as the story html file.

Dependencies:
- Python3
- BeautifulSoup

Usage: literader.py url

The story html and illustrations/images will be saved in the current directory.
