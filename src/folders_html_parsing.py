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
    for dt_folder_tag in dt_folder_tags:
        folder_name: str = dt_folder_tag.find_next().text
        if folder_name == "Bookmarks":
            continue # because these are first level items in html doc
        if folder_name == "Tabli Saved Windows":
            break
        path: list = update_path(dt_folder_tag, dt_folder_tags)
        pretty_path: str = prettify_path("/", path)
        print(pretty_path)


def get_contents(folder_dt_tag): #TODO
    pass

def update_path(base_folder_dt_tag, folder_tags: list) -> list:
    folder_dt_tag = base_folder_dt_tag
    folder_name: str = "'" + folder_dt_tag.find_next().text + "'"
    path: list = [folder_name]
    while folder_dt_tag != folder_tags[0]:
        folder_dt_tag = get_folder_parent_tag(folder_dt_tag, folder_tags)
        folder_name = "'" + folder_dt_tag.find_next().text + "'"
        path.insert(0, folder_name)
    return path

def get_folder_parent_tag(folder_dt_tag, folder_tags: list):
    parent_tag = folder_dt_tag
    is_parent_folder: bool = False
    is_valid_folder: bool = False
    while is_valid_folder == False:
        parent_tag = parent_tag.parent
        if parent_tag.name == "dl":
            is_parent_folder = True
        if is_parent_folder and folder_tags.__contains__(parent_tag):
            is_valid_folder = True
    return parent_tag

def prettify_path(separator: str, folders_path: list) -> str:
    path: str = separator.join(folders_path)
    return path

main()