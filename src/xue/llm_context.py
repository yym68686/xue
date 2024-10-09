import os
import fnmatch

def read_gitignore(directory):
    """
    读取.gitignore文件并返回忽略规则列表
    """
    gitignore_path = os.path.join(directory, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as file:
            return [line.strip() for line in file if line.strip() and not line.startswith('#')]
    return []

def should_ignore(path, ignore_patterns):
    """
    检查路径是否应该被忽略
    """
    path = os.path.normpath(path)
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

def read_file_content(file_path):
    """
    读取文件内容
    :param file_path: 文件路径
    :return: 文件内容的字符串
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"无法读取文件内容: {str(e)}"

def get_folders_and_files(directory, ignore_patterns):
    """
    获取目录下的文件夹和文件列表
    """
    contents = os.listdir(directory)
    folders = []
    files = []
    for item in contents:
        full_path = os.path.join(directory, item)
        if not should_ignore(full_path, ignore_patterns):
            if os.path.isdir(full_path) and item not in exclude_dirs:
                folders.append(item)
            elif os.path.isfile(full_path):
                files.append(item)
    folders.sort()
    files.sort()
    return folders, files

def print_directory_tree(directory, prefix="", ignore_patterns=None):
    """
    打印目录树结构
    :param directory: 要展示的目录路径
    :param prefix: 用于缩进的前缀字符串
    """
    directory_tree_context = []
    folders, files = get_folders_and_files(directory, ignore_patterns)

    # 打印文件夹
    for i, folder in enumerate(folders):
        if i == len(folders) - 1 and len(files) == 0:
            directory_tree_context.append(f"{prefix}└── {folder}")
            # print(f"{prefix}└── {folder}")
            directory_tree_context.extend(print_directory_tree(os.path.join(directory, folder), prefix + "    ", ignore_patterns))
        else:
            directory_tree_context.append(f"{prefix}├── {folder}")
            # print(f"{prefix}├── {folder}")
            directory_tree_context.extend(print_directory_tree(os.path.join(directory, folder), prefix + "│   ", ignore_patterns))

    # 打印文件
    for i, file in enumerate(files):
        if i == len(files) - 1:
            directory_tree_context.append(f"{prefix}└── {file}")
            # print(f"{prefix}└── {file}")
        else:
            directory_tree_context.append(f"{prefix}├── {file}")
            # print(f"{prefix}├── {file}")
    return directory_tree_context

def print_file_content(directory, exclude_files, ignore_patterns=None):
    """
    打印目录树结构
    :param directory: 要展示的目录路径
    :param prefix: 用于缩进的前缀字符串
    """
    file_content_context = []
    folders, files = get_folders_and_files(directory, ignore_patterns)

    # 打印文件夹
    for i, folder in enumerate(folders):
        if i == len(folders) - 1 and len(files) == 0:
            file_content_context.extend(print_file_content(os.path.join(directory, folder), exclude_files, ignore_patterns))
        else:
            file_content_context.extend(print_file_content(os.path.join(directory, folder), exclude_files, ignore_patterns))

    # 打印文件
    for i, file in enumerate(files):
        file_path = os.path.join(directory, file)
        # print(f"file_path: {file_path}\nexclude_files: {exclude_files}", file_path in exclude_files)
        if file_path not in exclude_files:
            content = read_file_content(file_path)
            file_path = file_path.replace("/Users/yanyuming/Downloads/GitHub/", "")
            # print(f"Content:")
            if content is None or content.strip() == "":
                file_content_context.append(f"{file_path}: This file is empty.")
                # print(f"This file is empty.")
                print(f"{file_path}")
            else:
                print(f"{file_path}")
                file_content_context.append(f"{file_path}:")
                for line in content.splitlines():
                    file_content_context.append(f"{line}")
                    # print(f"{line}")
            file_content_context.append(f"\n")  # 在文件内容之后添加一个空行

    return file_content_context

context = []
exclude_files = [
    "src/xue/markdown.py",
    "src/xue/llm_context.py",
    # "src/xue/llm_context-split.py",
    "setup.py",
    # "requirements.txt",
    "README.md",
    "README_CN.md",
    "LICENSE",
    ".gitignore",
    "xue_context.txt",
    "test/components/test_button copy.py",
    "test/components/test_dropdown.py",
    # "test/components/test_form_uni_api.py",
]

exclude_dirs = [
    ".git",
    ".github",
    "uni-api",
    "__pycache__",
    "example",
]
# 使用示例
directory_path = "/Users/yanyuming/Downloads/GitHub/xue"  # 替换为你想要展示的目录路径
exclude_files = [os.path.join(directory_path, file) for file in exclude_files]
ignore_patterns = read_gitignore(directory_path)
context.append(f"这是所有文件的目录树结构和具体的内容，某些文件内容暂时不相关不会被提供:\n")
context.append(f"Directory tree of {directory_path}:")
directory_tree_context = print_directory_tree(directory_path, ignore_patterns=ignore_patterns)
context.extend(directory_tree_context)
file_content_context = print_file_content(directory_path, exclude_files, ignore_patterns=ignore_patterns)
context.extend(file_content_context)
# print("\n".join(context))
file_context = "\n".join(context)

prompt = '''
我开发了一个新的前端框架，它是一个由 HTMX 和 Python 组成的极简主义 Web 前端框架。名字是 xue。该项目仅依赖 FastAPI，HTMX，httpx。不依赖 jinja2。

src/xue/components 是我为 xue 组件编写的代码文件，其中包含了一些组件的代码。主要模仿了 Shadcn 组件库的设计。模仿 Shadcn 来设计组件，包括丝滑的动态效果，优雅简洁美观的界面，平滑的动画效果和响应式交互。

test/components 是我为 xue 组件编写的测试文件，其中包含了一些组件的测试代码。主要测试 src/xue/components 中的组件是否正常工作。

回答我的问题的时候，不要使用纯 html 代码，而是使用 xue 组件库中的组件代码。要返回 html，请使用 xue 框架的 render() 方法。

如果需要写新的组件，尽量复用已经写好的组件代码，目前已经写好的组件代码在 src/xue/components 中。目前已经写好的组件有：button，checkbox，dropdown，form，input，select。

所有组件必须符合 shadcn/ui 的风格：

1. 丝滑的动态效果
2. 优雅简洁美观的界面
3. 平滑的动画效果和响应式交互。
4. 不引入过多的颜色，例如:
    - shadcn/ui 的按钮要么是黑底白字，要么是白底黑字，鼠标悬浮时黑底白字会变灰色，白底黑字会变深灰色。
'''

final_context = [prompt, file_context]

print(len(file_context.split("\n")))
# print("\n".join(final_context))

# 保存到文件
with open("xue_context.txt", "w") as file:
    file.write("\n".join(final_context))
    print("Context saved to xue_context.txt")