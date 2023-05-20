from bs4 import BeautifulSoup

with open("bookmarks_12_25_22.html", "r") as file:
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
    folder_parent = get_folder_parent(dt_folder_tags[1])
    test = dt_folder_tags[1].next_sibling
    print(test)

def get_folder_parent(dt_folder_tag, folder_tags_list: list) -> str:
    loop_status: bool = False
    count: int = 0
    parent_tag = dt_folder_tag
    while loop_status == False:
        parent_tag = parent_tag.parent
        if folder_tags_list.__contains__(parent_tag):
            loop_status = True
        count += 1
    if count > 2:
        pass
    else:
        parent_folder_name: str = parent_tag.find_next().text
        

main()