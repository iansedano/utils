from pathlib import Path
import re


f_count, r_count = 0, 0
starting_path = '[PUT STARTING PATH HERE]'

# Here are some different patterns to try, comment/uncomment them as needed:
# p = re.compile(r'(?<!!)\[([^\s\]]*)\]\(([^\s\)]*)\)')
p = re.compile(r'(?<!!)\[(.+?)\]\((.+?)\)') # Agressive variation

"""
the regex matches all Markdown links of the form following form:
    [Example](http://www.example.com)
and replaces them with new-tab HTML links, e.g.:
    <a href="http://www.example.com" target="_blank">Example</a>
NOTE: it does **NOT** match Markdown image links, e.g.
    ![Example](imgs/example.jpg)
which is intentional and expected behavior
"""

def update_links(matchobj):
    """Creates a HTML link that opens in a new tab from an appropriate re.match() object."""
    global r_count
    text = matchobj.group(1)
    url = matchobj.group(2)
    r_count += 1
    return f'<a href="{url}" target="_blank">{text}</a>'


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