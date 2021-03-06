# pip3 install fabric
import time
import subprocess
from pathlib import Path
import re
import platform
from pprint import pprint
from fabric import task
'''
tip
    危险命令要求用户使用input确认, are you sure?

todo：
    提取tags和提取links的正则表达式写得很烂，很多边缘情况没考虑，有空重写
'''

note_name_pattern = r'\d{8}_\d{6}_.+\.md'


def open_note_with_default_editor(path):
    if platform.system() == "Darwin":
        # http://stackoverflow.com/a/3520693/261181
        # -R doesn't allow showing hidden folders
        cmd = "open"
    if platform.system() == "Linux":
        cmd = "xdg-open"
    if platform.system() == "Windows":
        cmd = "explorer"
    subprocess.Popen([cmd, str(path)])
    return [cmd, str(path)]


def get_all_notes():
    mds = list(Path('.').glob("*.md"))  # all markdown file
    notes = [md.name for md in mds if re.match(note_name_pattern, md.name)]
    return notes # note Path list


@task
def ls(c):
    '''
    列出所有笔记
    保持与ls输出一致
    '''
    notes = get_all_notes()
    for note in notes:
        print(note)


note_template = '''# note_title
#tag1 #tag2

content

## ref
- [title](url)

## Links
- [note_name](note_name.md)
'''


@task
def new(c, name):
    '''
    创建一条新笔记 --name=new_note
    '''
    now = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    new_note_name = f'{now}_{name}.md'
    new_note_content = note_template.replace("note_title", name)
    with open(new_note_name, 'a+') as f:
        f.write(new_note_content)
    print(f'新笔记 {new_note_name} 创建成功')
    open_note_with_default_editor(new_note_name)


def get_ack_cmd():
    if platform.system() == "Darwin":
        # http://stackoverflow.com/a/3520693/261181
        # -R doesn't allow showing hidden folders
        ack = "ack"
    if platform.system() == "Linux":
        ack = "ack-grep"
    if platform.system() == "Windows":
        ack = "ack-grep"
    return ack


@task
def tags(c, mode="all"):  # mode : tags, all
    '''
    列出所有标签: --mode=[all/only]

    使用ack-grep
    '''
    ack = get_ack_cmd()
    if mode == "all":
        cmd = ack + " '\#{1}[^(\s|\#)]+' 20*.md"  # 20xx年(21世纪)的md笔记，弱模式匹配（足够），可以过滤掉readme.md
        subprocess.call(cmd, shell=True)
        # print(mode)
    if mode == "only":
        cmd = ack + " -h '\#{1}[^(\s|\#)]+' 20*.md" # 20xx年(21世纪)的md笔记，弱模式匹配（足够），可以过滤掉readme.md
        results = subprocess.check_output(cmd, shell=True)
        tags = set(results.decode().strip().split())
        print(tags)


def get_all_links():
    '''
    收集所有note指向的note列表(note:[note])

    todo 使用pharo来做可视化。
    '''
    notes = get_all_notes()
    all_links = {}
    for note_file_name in notes:
        with open(note_file_name) as f:
            content = f.read()
            # 使用正则取出所有links: 20200223_2136_Zettelkasten笔记原则.md
            pattern = r'(?<=\()'+ note_name_pattern + r'(?=\))' # re 环顾
            note_links = list(set(re.findall(pattern, content)))
            all_links[note_file_name] = note_links
    return all_links


@task
def git_backup(c):
    '''
    使用git备份笔记
    '''
    cmd = 'git add *.md; git commit -m "backup note"'
    c.run(cmd)


@task
def link_graph(c, mode="md"):
    '''
    列出笔记之间的连接关系 --mode=[md/pyvis/cli]
        note --link--> note
        note:[note]
    '''
    all_links = get_all_links()
    pprint(all_links)

    if mode.lower().startswith("pyvis"):
        # pip install pyvis networkx
        import networkx as nx
        dg = nx.DiGraph()
        g = nx.Graph()
        node_edge_tuples = []
        for i in all_links:
            for j in all_links[i]:
                node_edge_tuples.append((i, j))
        dg.add_edges_from(node_edge_tuples)
        from pyvis.network import Network
        g = Network(notebook=True, width=1300, height=700)
        g.from_nx(dg)
        viz_html = 'note_graph.html'
        g.show(viz_html)
        open_note_with_default_editor(viz_html)
        # nx.draw(dg)

    if mode.lower() == "md":
        # https://mermaidjs.github.io/
        with open("graph_tpl_md.html") as f:
            html_tpl = f.read()
            md_graph = "graph TD\n"
            for i in all_links:
                for j in all_links[i]:
                    md_graph += f"{i}-->{j}\n"
            with open("graph_md.html", "w") as f:
                h = html_tpl.replace("tpl_content", md_graph)
                f.write(h)
            open_note_with_default_editor("graph_md.html")


@task
def search(c, word="", tag=""):
    '''
    fab search --tag tag ; fab search --word key_word 
    '''
    # 区分mac/linux
    if tag:
        ack = get_ack_cmd()
        cmd = f'{ack} "\#{tag}" 20*.md' # 20xx年(21世纪)的md笔记，弱模式匹配（足够），可以过滤掉readme.md
        subprocess.call(cmd, shell=True)
    if word:
        ack = get_ack_cmd()
        cmd = f"{ack} {word}  20*.md" # 20xx年(21世纪)的md笔记，弱模式匹配（足够），可以过滤掉readme.md
        subprocess.call(cmd, shell=True)
