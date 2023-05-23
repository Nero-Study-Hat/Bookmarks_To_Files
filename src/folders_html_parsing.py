from bs4 import BeautifulSoup
import os
import favicon

with open("bookmarks_5_20_23.html", "r") as file:
    bookmarks_doc = BeautifulSoup(file, "html.parser")

# grab all link and folder tags in bookmarks html file
_dt_tags: list = bookmarks_doc.find_all("dt")

# Possible results to filter for include (folder) and (link)
def filter_dt_tags(dt_tags_container, desired_result: str) -> list:
    dt_tag_type: str = ''
    dt_tags: list = [] # tags for all links and folders
    if desired_result == "folder":
        dt_tag_type = "h3"
    if desired_result == "link":
        dt_tag_type = "a"
    for dt_tag in dt_tags_container:
        if dt_tag.find_next().name == dt_tag_type: # check if folder or link
            dt_tags.append(dt_tag)
    return dt_tags
        
class bookmarks_folders:
    def clean_folder_name(name: str) -> str:
        name.strip(" ")
        if "/" in name:
            new_name: str = name.replace("/", "")
            return new_name
        else:
            return name
    
    # This will get the path of the request folder.
    def update_path(request_folder_dt_tag, folder_tags: list) -> list:
        folder_dt_tag = request_folder_dt_tag
        folder_name: str = bookmarks_folders.clean_folder_name(request_folder_dt_tag.find_next().text)
        path: list = [folder_name]
        while folder_dt_tag != folder_tags[0]:
            folder_dt_tag = bookmarks_folders.get_folder_parent_tag(folder_dt_tag, folder_tags)
            folder_name: str = bookmarks_folders.clean_folder_name(folder_dt_tag.find_next().text)
            # if " " in folder_name:
            #     folder_name = "'" + folder_name + "'" # ' is so that spaces are allowed in path
            path.insert(0, folder_name) # append folder names to beginning of the path list
        return path

    def get_folder_parent_tag(folder_dt_tag, folder_tags: list):
        parent_tag = folder_dt_tag # for recursively finding valid parent
        is_parent_folder: bool = False
        is_valid_folder: bool = False
        while is_valid_folder == False: # base recusion condition
            parent_tag = parent_tag.parent
            if parent_tag.name == "dl": # this will always be before the parent dt_folder_tag
                is_parent_folder = True
            if is_parent_folder and folder_tags.__contains__(parent_tag): # grab valid folder tag after passing dl_tag
                is_valid_folder = True
        return parent_tag # this is a dt_folder_tag

    def prettify_path(folders_path: list) -> str:
        path: str = "/".join(folders_path)
        return path

    def create_folder(folder_path: str):
        if os.path.isdir(folder_path) == False: # This breaks at imported folder due to Tabli exception.
            os.mkdir(folder_path)

class bookmarks_links:
    def create_link_file(bookmark_path:str, bookmark_name: str, bookmark_url: str):
        search_name: str = "Name="
        search_url: str = "URL="
        search_icon_path: str = "Icon="
        new_name: str = bookmark_name
        new_url: str = bookmark_url
        new_icon_path: str = "" #TODO
        with open("template_bookmark.desktop", "r") as desktop_file:
            template_bookmark_file: str = desktop_file.read()
            new_link_file: str = template_bookmark_file.replace(search_name, new_name)
            new_link_file: str = new_link_file.replace(search_url, new_url)
            # new_link_file = new_link_file.replace(search_icon_path, new_icon_path)
        with open(f"{bookmark_path}/{bookmark_name}.desktop", "w") as desktop_file:
            desktop_file.write(new_link_file)
    
    def get_link_contents(link_tag):
        bookmark = link_tag.find_next()
        bookmark_name: str = bookmark.text
        bookmark_url: str = bookmark.get("href")
        return bookmark_name, bookmark_url
            

# Will create standard directories to match bookmarks folders with their paths
# and .desktop files for the bookmark links.
def main():
    folder_tags: list = filter_dt_tags(_dt_tags, "folder") # all bookmark folders
    debug: bool = False
    for folder_tag in folder_tags:
        folder_name: str = folder_tag.find_next().text
        if folder_name == "Imported":
            debug = True
        if folder_name == "Bookmarks": #FIXME have a default first level parent if there is no parent instead of exceptions
            continue # because these are first level items in html doc
        if folder_name == "Tabli Saved Windows":
            break
        folder_path: list = bookmarks_folders.update_path(folder_tag, folder_tags)
        pretty_folder_path: str = bookmarks_folders.prettify_path(folder_path)
        bookmarks_folders_location: str = "/home/nero_admin/Downloads/Testing_Bookmarks_Project"
        folder_path: str = f"{bookmarks_folders_location}/{pretty_folder_path}"
        bookmarks_folders.create_folder(folder_path)
        
        # link_tags = filter_dt_tags(folder_tag, "link")
        # for link_tag in link_tags:
        #     bookmark_name, bookmark_url = bookmarks_links.get_link_contents(link_tag)
        #     bookmarks_links.create_link_file(folder_path, bookmark_name, bookmark_url)
            


main()