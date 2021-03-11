from pathlib import Path
import re

f_count, r_count = 0, 0
starting_path = '[PUT STARTING PATH HERE]'

p = re.compile(r'\!\[([^\]]+)\]\(([^\)]+)\)')

"""
the regex matches all Markdown image links of the form following form:
    ![Example](http://www.example.com/image.jpg)
and replaces them with new-tab HTML links, e.g.:
    '<img src="http://www.example.com/image.jpg" alt="Example" class="cn_image img-responsive">
"""

def update_links(matchobj):
    """Creates a HTML link that opens in a new tab from an appropriate re.match() object."""
    global r_count
    text = matchobj.group(1)
    url = matchobj.group(2)
    r_count += 1
    return f'<img src="{url}" alt="{text}" class="cn_image img-responsive">'


def replace(directory):
    """Replaces all Markdown-style links with HTML new-tab links recursively in a folder structure."""
    global f_count
    print(f'Replacing links in {directory.name}')
    for file_ in sorted(directory.rglob('*.md')):
        # not replacing links in README file because that makes the file that isn't used in the course more messy
        if file_.name != "README.md" and file_.name.endswith(".md"):
            print(f'Starting on file {file_.name}')
            f_count += 1
            with open(file_.absolute(), 'r+', encoding='utf8') as f:
                content = f.read()
                # rewind to the beginning of the file and cut out the old content
                f.seek(0)
                f.truncate()
                # write back the content with links replaced
                f.write(re.sub(p, update_links, content))


def main():
    current_dir = Path(starting_path)
    replace(current_dir)
    print(f'Done. Replaced {r_count} links across {f_count} files.')


if __name__ == "__main__":
    main()