import os
import re

class MarkdownEntity:
    def __init__(self, content: str = "", entity_type: str = ""):
        self.content = content
        self.entity_type = entity_type

    def __repr__(self):
        return f'<{self.entity_type}: {repr(self.content)}>'

    def copy(self):
        return self.__class__(self.content)

class Title(MarkdownEntity):
    def __init__(self, content: str = "", level: int = 1):
        super().__init__(content, 'Title')
        self.level = level

class CodeBlock(MarkdownEntity):
    def __init__(self, content: str = "", language: str = 'python'):
        super().__init__(content, 'CodeBlock')
        self.language = language

class ListItem(MarkdownEntity):
    def __init__(self, content: str = ""):
        super().__init__(content, 'ListItem')

class Link(MarkdownEntity):
    def __init__(self, content: str = "", url: str = ""):
        super().__init__(content, 'Link')
        self.url = url

class EmptyLine(MarkdownEntity):
    def __init__(self, content: str = ""):
        super().__init__(content, 'EmptyLine')

class Paragraph(MarkdownEntity):
    def __init__(self, content: str = ""):
        super().__init__(content, 'Paragraph')

class OrderList(MarkdownEntity):
    def __init__(self, content: str = "", index: int = 1):
        super().__init__(content, 'OrderList')
        self.index = index

class DisplayMath(MarkdownEntity):
    def __init__(self, content: str = ""):
        super().__init__(content, 'DisplayMath')

def parse_markdown(lines, delimiter='\n'):
    entities = []
    current_code_block = []
    current_math_block = []
    in_code_block = False
    in_math_block = False
    language = None

    for line in lines:
        if line == delimiter:
            continue
        if line.startswith('$$') and not in_code_block:
            if in_math_block:
                # current_math_block.append(line.strip('$'))
                entities.append(DisplayMath('\n'.join(current_math_block)))
                current_math_block = []
                in_math_block = False
            else:
                in_math_block = True
                # current_math_block.append(line.strip('$'))
        elif in_math_block:
            # print(repr(line))
            current_math_block.append(line)
        elif line.startswith('#') and not in_code_block and not in_math_block:
            level = line.count('#')
            title_content = line[level:].strip()
            entities.append(Title(title_content, level))
        elif line.startswith('```'):
            if in_code_block and language:
                entities.append(CodeBlock('\n'.join(current_code_block), language))
                current_code_block = []
                in_code_block = False
                language = None
            else:
                in_code_block = True
                language = line.lstrip('`').strip()
        elif in_code_block:
            current_code_block.append(line)
        elif '[' in line and ']' in line and '(' in line and ')' in line and line.count('[') == 1 and line.strip().endswith(')') and line.strip().startswith('['):
            start = line.index('[') + 1
            end = line.index(']')
            url_start = line.index('(') + 1
            url_end = line.index(')')
            link_text = line[start:end].strip()
            link_url = line[url_start:url_end].strip()
            entities.append(Link(link_text, link_url))
        elif line == '':
            entities.append(EmptyLine(line))
        # elif line == delimiter:
        #     entities.append(EmptyLine(line))
        elif bool(re.match(r'^\d+\.\s', line)):
            index = int(re.match(r'^\d+\.\s', line).group(0)[:-2])
            content = re.sub(r'^\d+\.\s', '', line)
            entities.append(OrderList(content, index))
        elif line:
            entities.append(Paragraph(line))

    # 处理文档末尾可能未闭合的数学公式块
    if in_math_block:
        entities.append(DisplayMath(''.join(current_math_block)))

    return entities

def convert_entities_to_text(entities):
    result = []
    for entity in entities:
        if isinstance(entity, Title):
            result.append(f"{'#' * entity.level} {entity.content}")
        elif isinstance(entity, CodeBlock):
            code = entity.content.lstrip('\n').rstrip('\n')
            result.append(f"```{entity.language}\n{code}\n```")
        elif isinstance(entity, ListItem):
            result.append(f"- {entity.content}")
        elif isinstance(entity, Link):
            result.append(f"[{entity.content}]({entity.url})")
        elif isinstance(entity, EmptyLine):
            result.append(f"{entity.content}")
        elif isinstance(entity, OrderList):
            result.append(f"{entity.index}. {entity.content}")
        elif isinstance(entity, Paragraph):
            result.append(f"{entity.content}")
        elif isinstance(entity, DisplayMath):
            result.append(f"$$\n{entity.content}\n$$")
    return '\n'.join(result)

def save_text_to_file(text: str, file_path: str):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def process_markdown_entities_and_save(entities, file_path, raw_text=None):
    # Step 1: Convert entities to text
    text_output = convert_entities_to_text(entities)
    if raw_text and raw_text != text_output:
        raise ValueError("The text output does not match the raw text input.")
    # Step 2: Save to file
    save_text_to_file(text_output, file_path)

def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        # 如果文件不存在，创建一个空文件
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            pass  # 创建一个空文件
        return ""  # 返回空字符串

def split_markdown(text, delimiter='\n'):
    # 使用两个换行符作为分割标记，分割段落
    # 创建一个新的列表来存储结果
    paragraphs = text.split(delimiter)
    # print(paragraphs)
    result = []

    # 遍历分割后的段落，在它们之间插入空行实体
    for i, paragraph in enumerate(paragraphs):
        if i > 0:
            # 在非第一段之前插入空行实体
            result.append(delimiter)

        # 添加当前段落
        result.append(paragraph)
    # print(result)

    return result

def get_entities_from_markdown_file(file_path, delimiter='\n', raw_text=None):
    # 读取 Markdown 文件
    if raw_text == None:
        markdown_text = read_markdown_file(file_path)
    else:
        markdown_text = raw_text

    # 分割 Markdown 文档
    paragraphs = split_markdown(markdown_text, delimiter=delimiter)

    # 解析 Markdown 文档
    return parse_markdown(paragraphs, delimiter=delimiter)

def check_markdown_parse(markdown_file_path, output_file_path="output.md", delimiter='\n'):
    # 读取 Markdown 文件
    markdown_text = read_markdown_file(markdown_file_path)

    # 分割 Markdown 文档
    paragraphs = split_markdown(markdown_text, delimiter=delimiter)

    # 解析 Markdown 文档
    parsed_entities = parse_markdown(paragraphs, delimiter=delimiter)
    # print(parsed_entities)

    # 将解析结果转换为文本
    converted_text = convert_entities_to_text(parsed_entities)

    # 检查原始文本和转换后的文本是否相同
    # print(converted_text)
    if markdown_text != converted_text:
        save_text_to_file(converted_text, output_file_path)
        raise ValueError("The converted text does not match the original text.")

    return parsed_entities

if __name__ == '__main__':
    # markdown_file_path = "README_CN.md"  # 替换为你的 Markdown 文件路径

    # # 读取 Markdown 文件
    # markdown_text = read_markdown_file(markdown_file_path)
    # paragraphs = split_markdown(markdown_text)
    # parsed_entities = parse_markdown(paragraphs)

    # # # 显示解析结果
    # # result = [str(entity) for entity in parsed_entities]
    # # for idx, entity in enumerate(result):
    # #     print(f"段落 {idx + 1} 解析：{entity}\n")

    # # 保存到文件
    # output_file_path = "output.md"
    # process_markdown_entities_and_save(parsed_entities, output_file_path, raw_text=markdown_text)

    # print(f"Markdown 文档已保存到 {output_file_path}")
    check_markdown_parse("/Users/yanyuming/Downloads/GitHub/xue/README.md", "output.md")