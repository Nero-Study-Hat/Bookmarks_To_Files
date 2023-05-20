from bs4 import BeautifulSoup

with open("bookmarks_12_25_22.html", "r") as file:
    bookmarks_doc = BeautifulSoup(file, "html.parser")

_dt_tags: list = bookmarks_doc.find_all("dt")
_path_folders: list = ['Bookmarks']

def get_dt_folder_tags(dt_tags) -> list:
    dt_folder_tags: list = []
    for dt_tag in dt_tags:
        if dt_tag.find_next().name == "h3":
            dt_folder_tags.append(dt_tag)
    return dt_folder_tags


def main():
    dt_folder_tags: list = get_dt_folder_tags(_dt_tags)
    for dt_folder_tag in dt_folder_tags:
        parent_folder: str = get_folder_contents(dt_folder_tag)
        update_path(parent_folder, dt_folder_tag)


def update_path(parent_folder_name: str, current_dt_tag, current_folder_name: str):
    if current_dt_tag.find_next().text == "Bookmarks":
        return
    loop_limit: int = len(_path_folders) - 1
    for index in range(loop_limit, -1, -1):
        folder_in_path: str = _path_folders[index]
        if folder_in_path != parent_folder_name:
            _path_folders.pop()
            continue
        else:
            _path_folders.append(current_folder_name)
            return

def get_folder_contents(dt_folder_tag) -> str:
    all_tags: list = dt_folder_tag.content
    folder_tags: list = get_dt_folder_tags(all_tags.find_all("dt"))
    #
    