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
    folder_contents = get_folder_contents(dt_folder_tags[1])
    test = dt_folder_tags[1].next_sibling
    print(test)

def get_folder_contents(dt_folder_tag):
    p_tag = dt_folder_tag.find("dl").find_next()
    folder_contents: list = p_tag.find_all("dt")
    folder_tags: list = get_dt_folder_tags(folder_contents)
    return folder_tags

main()