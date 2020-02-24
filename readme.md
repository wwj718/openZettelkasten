# readme
#笔记 #写作 #meta信息

这是我的 Zettelkasten/slip-box 仓库，用于存储我的笔记卡片。

Zettelkasten是一种笔记系统，核心思想很简单: 笔记独立地记录在不同的卡片(Zettel, 德语)上，卡片之间应该形成网络，彼此连接，形成一张思想的网络。

这个笔记系统让你不再惧怕笔记因数量的增长，而变为"信息坟墓"。随着笔记数量的增长，这个有机网络最终将成为你思考和写作的伙伴。它是对你大脑能力的扩展。

构建笔记卡片时，应当遵循以下原则:

[20200223_213607-Zettelkasten笔记原则](20200223_213607-Zettelkasten笔记原则.md)

---

## 结构和格式
笔记格式遵循[Zettelkasten — How One German Scholar Was So Freakishly Productive](https://writingcooperative.com/zettelkasten-how-one-german-scholar-was-so-freakishly-productive-997e4e0ca125)的建议: 采用纯文本([Markdown](https://en.wikipedia.org/wiki/Markdown))，而不对特定工具产生依赖，因其可能会使用数年甚至一生，而大多数技术工具被淘汰得太快。


所有笔记都平坦放置在目录中(完全扁平)，方便彼此连接。

来看一个真实的笔记(zettel)例子: [20200223_213419-Zettelkasten是绝佳的笔记系统](20200223_213419-Zettelkasten是绝佳的笔记系统.md)

`20200223_213419`是时间戳（`年月日-时分秒`），`Zettelkasten是绝佳的笔记系统` 是笔记title，它是一个Markdown文件(以`.md`结尾)

笔记模版为:

```md
# note_title
#tag1 #tag2

content

## ref
- [note_name](note_name.md)

## Links
- [note_name](note_name.md)
```

你可以手动创建笔记(只是纯文本而已，没有魔法)，也可以使用脚本工具(见下文)。

我们使用[fabric](http://www.fabfile.org/)构建一些自动化脚本, 它们只是些[简单的Python脚本](fabfile.py)。在此不是想构建一个笔记应用，而是想提供一些脚本和脚手架，让Zettelkasten使用者方便构建自己的自动化脚本，完成一些日常任务:

*  自动创建笔记(手动输入时间戳和笔记内部结构都很累)
*  显示笔记之间的网络关系
*  列出仓库里的所有标签
*  备份笔记
*  搜素
*  统计
*  ...

笔记是很私人的物品，随着它成长为你的同伴，要如何与之相处，如何从中提取出知识和灵感，换句话说，如何与你的笔记进行深入活动，你通常需要构建自己的脚本，打造自己的探索工具，因为你才对它最为了解。

在此我试图构建一些简单的脚手架，之所以力图简单，是希望你能方便地再出发。

我尽可能重用unix/linux工具箱中工具，诸如

*  搜索使用`ack-grep`
*  备份使用`git`
*  脚本使用Python3

随时掀起引擎盖，查看和调整它，没有魔法：）


## requirements
*  `Python >= 3.6`
    *  pip3 install fabric
*  ack-gtrp

## usage
### 列出所有功能
`fab --list`

```bash
➜  Zettelkasten git:(master) ✗ fab --list
Available tasks:

  git-backup   使用git备份笔记
  link-graph   列出笔记之间的连接关系 --mode=[md/pyvis]
  ls           列出所有笔记
  new          创建一条新笔记 --name=new_note
  search
  tags         列出所有标签: --mode=[all/only]
```

### 创建新笔记
`fab new --name your_note_name`

```bash
➜  Zettelkasten git:(master) ✗ fab new --name 这是一条测试笔记
新笔记 20200224_205312_这是一条测试笔记.md 创建成功
```

创建完笔记后，会自动使用markdown编辑器打开笔记，在我的电脑环境里，它是vscode。

### 列出笔记仓库信息
#### 列出所有笔记
`fab ls`

```bash
➜  Zettelkasten git:(master) ✗ fab ls
20200223_213419-Zettelkasten是绝佳的笔记系统.md
20200223_213607-Zettelkasten笔记原则.md
20200224_2052_这是一条测试笔记.md
readme.md
```

#### 列出标签
`fab tags`

```
➜  Zettelkasten git:(master) ✗ fab tags
20200223_213419-Zettelkasten是绝佳的笔记系统.md
#生产力 #写作 #思想 #笔记

20200223_213607-Zettelkasten笔记原则.md
#原则 #笔记

readme.md
#笔记 #写作 #meta信息
#tag1 #tag2
```

你也可以只看tags:

```bash
➜  Zettelkasten git:(master) ✗ fab tags --mode only
{'#原则', '#笔记', '#tag2', '#思想', '#写作', '#meta信息', '#生产力', '#tag1'}
```

使用了ack-grep

#### 显示笔记网络
`fab link-graph`

默认将打开浏览器，使用svg渲染笔记网络。

你也可以使用[networkx](https://networkx.github.io/)来构建网络图:

`fab link-graph --mode=pyvis`

代码都很简单，只要熟悉使用[networkx](https://networkx.github.io/)和可视化工具，你可以构建任何网络图，你也可以利用networkx与你的网络深入对话。

### 搜索笔记
`fab search key_word`

```bash
➜  Zettelkasten git:(master) ✗ fab search 原则
```

命令行中搜索结果会高亮显示。

使用了ack-grep。

### 备份(git)
`fab git-backup`


## links
*  [20200223_2134-Zettelkasten是绝佳的笔记系统](20200223_213419-Zettelkasten是绝佳的笔记系统.md)
*  [20200223_2136-Zettelkasten笔记原则](20200223_213607-Zettelkasten笔记原则.md)