from bs4 import BeautifulSoup

with open("bookmarks_5_20_23.html", "r") as file:
    bookmarks_doc = BeautifulSoup(file, "html.parser")

_dt_items: list = bookmarks_doc.find_all("dt")
_path_complete: str = ''
_path_folders: list = ['Bookmarks']

def get_complete_path(separator: str) -> str:
    #TODO Display message to user saying they need to input a string.
    path: str = separator.join(_path_folders) + separator
    return path

def set_parent_folder(parent_folder: str):
    _parent_folder = parent_folder

def main():
    for dt_item in _dt_items:
        next_item = dt_item.find_next()
        if next_item.name != 'h3':
            continue
        else:
            folder_name = next_item.text
            parent_folder_name: str = get_parent_folder_name(dt_item)
            update_path(dt_item, parent_folder_name, folder_name) #TODO Ask user to input separator.
            _path_complete = get_complete_path("/")
            print(f"{folder_name} has path: {_path_complete}")

        print() # for empty new line seperator

def update_path(dt_folder_item, parent_folder_name: str, current_folder_name: str):
    if dt_folder_item.find_next().text == "Bookmarks":
        return
    loop_limit: int = len(_path_folders) - 1
    for index in range(loop_limit, -1, -1):
        folder: str = _path_folders[index]
        if folder != parent_folder_name:
            _path_folders.pop()
            continue
        else:
            _path_folders.append(current_folder_name)
            return

def get_parent_folder_name(dt_folder_item) -> str:
    exit_status: bool = False
    dt_parent_item = dt_folder_item
    while exit_status == False:
        parent_dt_element = dt_parent_item.find_previous('dt')
        if parent_dt_element.find_next().name == "h3":
            exit_status = True
        dt_parent_item = parent_dt_element
    folder_name: str = parent_dt_element.text
    return folder_name

main()