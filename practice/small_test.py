from bs4 import BeautifulSoup

with open("bookmarks_5_20_23.html", "r") as file:
    bookmarks_doc = BeautifulSoup(file, "html.parser")

_dt_tags: list = bookmarks_doc.find_all("dt")

def get_dt_folder_tags(dt_tags_container) -> list:
    dt_folder_tags: list = []
    for dt_tag in dt_tags_container:
        if dt_tag.find_next().name == "h3":
            dt_folder_tags.append(dt_tag)
    return dt_folder_tags

def main():
    dt_folder_tags: list = get_dt_folder_tags(_dt_tags)
    prev_folder_name: str = 'Bookmarks'
    for dt_folder in dt_folder_tags:
        folder_parent: str = get_folder_parent(dt_folder, dt_folder_tags)
        if folder_parent != prev_folder_name:
            print("--- change ---")
        prev_folder_name = folder_parent
        print(f"{folder_parent} -> is the parent folder of: {dt_folder.find_next().text}")

# Working, only exceptions are
# "Bookmarks" dt item and "Tabli Saved Windows" which are first level in the html file.
def get_folder_parent(dt_folder_tag, folder_tags_list: list) -> str:
    parent_tag = dt_folder_tag
    is_parent_folder: bool = False
    is_valid_folder: bool = False
    if dt_folder_tag.find_next().text == 'Bookmarks': # exception
        return 'Bookmarks'
    if dt_folder_tag.find_next().text == "Tabli Saved Windows": # exception
        return 'Tabli Saved Windows'
    while is_valid_folder == False:
        parent_tag = parent_tag.parent
        if parent_tag.name == "dl":
            is_parent_folder = True
        if is_parent_folder and folder_tags_list.__contains__(parent_tag):
            is_valid_folder = True
    parent_folder_name: str = parent_tag.find_next().text
    return parent_folder_name
        

main()