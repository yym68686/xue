import os
import re
from .core import *

class MarkdownEntity:
    def __init__(self, content: str = "", entity_type: str = ""):
        self.content = content
        self.entity_type = entity_type

    def __repr__(self):
        return f'<{self.entity_type}: {repr(self.content)}>'

    def copy(self):
        return self.__class__(self.content)

class TitleEntity(MarkdownEntity):
    def __init__(self, content: str = "", level: int = 1):
        super().__init__(content, 'TitleEntity')
        self.level = level

class CodeBlock(MarkdownEntity):
    def __init__(self, content: str = "", language: str = 'python'):
        super().__init__(content, 'CodeBlock')
        self.language = language

class ListItem(MarkdownEntity):
    def __init__(self, content: str = ""):
        super().__init__(content, 'ListItem')

class LinkEntity(MarkdownEntity):
    def __init__(self, content: str = "", url: str = ""):
        super().__init__(content, 'LinkEntity')
        self.url = url

class ImageEntity(MarkdownEntity):
    def __init__(self, content: str = "", url: str = ""):
        super().__init__(content, 'ImageEntity')
        self.url = url
        self.alt_text = content

class EmptyLine(MarkdownEntity):
    def __init__(self, content: str = ""):
        super().__init__(content, 'EmptyLine')

class Text(MarkdownEntity):
    def __init__(self, content: str = ""):
        super().__init__(content, 'Text')

class CompositeEntity(MarkdownEntity):
    def __init__(self, content: str = "", entity_type: str = ""):
        super().__init__(content, entity_type)
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class ListItem(CompositeEntity):
    def __init__(self, content: str = "", level: int = 0):
        super().__init__(content, 'ListItem')
        self.level = level
        self.parse_content()

    def parse_content(self):
        inline_elements = parse_inline_elements(self.content)
        for elem in inline_elements:
            if isinstance(elem, str):
                self.add_child(Text(elem))
            else:
                self.add_child(elem)

class OrderedListItem(ListItem):
    def __init__(self, content: str = "", level: int = 0, index: int = 1):
        super().__init__(content, level)
        self.entity_type = 'OrderedListItem'
        self.index = index

class UnorderedListItem(ListItem):
    def __init__(self, content: str = "", level: int = 0):
        super().__init__(content, level)
        self.entity_type = 'UnorderedListItem'

class DisplayMath(MarkdownEntity):
    def __init__(self, content: str = ""):
        super().__init__(content, 'DisplayMath')

class InlineLink(MarkdownEntity):
    def __init__(self, content: str = "", url: str = ""):
        super().__init__(content, 'InlineLink')
        self.url = url

class InlineMath(MarkdownEntity):
    def __init__(self, content: str = ""):
        super().__init__(content, 'InlineMath')

class Paragraph(CompositeEntity):
    def __init__(self, content: str = ""):
        super().__init__(content, 'Paragraph')
        self.parse_content()

    def parse_content(self):
        inline_elements = parse_inline_elements(self.content)
        for elem in inline_elements:
            if isinstance(elem, str):
                self.add_child(Text(elem))
            else:
                self.add_child(elem)

    def __repr__(self):
        return f'<Paragraph: {repr(self.children)}>'

def parse_inline_elements(text):
    elements = []
    current_text = ""

    i = 0
    while i < len(text):
        if text[i:i+2] == '$$':  # Display math
            if current_text:
                elements.append(Text(current_text))
                current_text = ""
            end = text.find('$$', i+2)
            if end != -1:
                elements.append(DisplayMath(text[i+2:end]))
                i = end + 2
            else:
                current_text += text[i:]
                break
        elif text[i] == '$':  # Inline math
            if current_text:
                elements.append(Text(current_text))
                current_text = ""
            end = text.find('$', i+1)
            if end != -1:
                elements.append(InlineMath(text[i+1:end]))
                i = end + 1
            else:
                current_text += text[i:]
                break
        elif text[i] == '[':  # 潜在的链接
            if current_text:
                elements.append(Text(current_text))
                current_text = ""

            # 查找匹配的右括号
            bracket_count = 1
            j = i + 1
            while j < len(text) and bracket_count > 0:
                if text[j] == '[':
                    bracket_count += 1
                elif text[j] == ']':
                    bracket_count -= 1
                j += 1

            if j < len(text) and text[j] == '(':
                # 找到了有效的链接格式
                content_end = j - 1
                url_start = j + 1
                url_end = text.find(')', url_start)
                if url_end != -1:
                    content = text[i+1:content_end]
                    url = text[url_start:url_end]
                    elements.append(InlineLink(content, url))
                    i = url_end + 1
                    continue

            # 如果不是有效的链接格式，将其作为普通文本处理
            current_text += text[i]
            i += 1
        else:
            current_text += text[i]
            i += 1

    if current_text:
        elements.append(Text(current_text))

    return elements

def parse_markdown(lines, delimiter='\n'):
    entities = []
    current_code_block = []
    current_math_block = []
    in_code_block = False
    in_math_block = False
    language = ""
    # list_stack = []

    for line in lines:
        print(repr(line), line.startswith('```'), in_code_block)
        # print('[' in line)
        # print(']' in line )
        # print( '(' in line and ')' in line )
        # print( line.count('[') == 1 )
        # print(line.strip().endswith(')') )
        # print(line.strip().startswith('!') )
        # print( line.count('!') == 1)
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
            entities.append(TitleEntity(title_content, level))
        elif line.startswith('```'):
            if in_code_block:
                entities.append(CodeBlock('\n'.join(current_code_block), language))
                current_code_block = []
                in_code_block = False
                language = ""
            else:
                in_code_block = True
                language = line.lstrip('`').strip()
        elif in_code_block:
            current_code_block.append(line)
        elif '[' in line and ']' in line and '(' in line and ')' in line and line.count('[') == 1 and line.strip().endswith(')') and line.strip().startswith('[') and line.count('!') == 0:
            start = line.index('[') + 1
            end = line.index(']')
            url_start = line.index('(') + 1
            url_end = line.index(')')
            link_text = line[start:end].strip()
            link_url = line[url_start:url_end].strip()
            entities.append(LinkEntity(link_text, link_url))
        elif '[' in line and ']' in line and '(' in line and ')' in line and line.count('[') == 1 and line.strip().endswith(')') and line.strip().startswith('![') and line.count('!') == 1:
            start = line.index('[') + 1
            end = line.index(']')
            url_start = line.index('(') + 1
            url_end = line.index(')')
            link_text = line[start:end].strip()
            link_url = line[url_start:url_end].strip()
            entities.append(ImageEntity(link_text, link_url))
        else:
            # Check for list items
            list_match = re.match(r'^(\s*)([*+-]|\d+\.)\s(.+)$', line)
            if list_match:
                indent, list_type, content = list_match.groups()
                level = len(indent) // 2  # Assuming 2 spaces per indent level

                # Clear list stack if we're at a lower or same level
                # while list_stack and list_stack[-1][0] >= level:
                #     list_stack.pop()

                if list_type in ['*', '-', '+']:
                    list_item = UnorderedListItem(content, level)
                else:
                    index = int(list_type[:-1])
                    list_item = OrderedListItem(content, level, index)

                entities.append(list_item)
                # if list_stack:
                #     list_stack[-1][1].add_child(list_item)
                # else:
                #     entities.append(list_item)

                # list_stack.append((level, list_item))

            elif line.strip():
                # 处理其他内容(段落、链接等)
                inline_elements = parse_inline_elements(line)
                para = Paragraph()
                for elem in inline_elements:
                    if isinstance(elem, str):
                        para.add_child(Text(elem))
                    else:
                        para.add_child(elem)
                entities.append(para)
            else:
                entities.append(EmptyLine(line))

    # 处理文档末尾可能未闭合的数学公式块
    if in_math_block:
        entities.append(DisplayMath(''.join(current_math_block)))

    return entities

def convert_entity_to_text(entity, indent='', linemode=False):
    if isinstance(entity, TitleEntity):
        return f"{'#' * entity.level} {entity.content}"
    elif isinstance(entity, CodeBlock):
        code = entity.content.lstrip('\n').rstrip('\n')
        return f"```{entity.language}\n{code}\n```"
    elif isinstance(entity, OrderedListItem) and linemode:
        # content = convert_entities_to_text(entity.children, indent + '  ', inline=True) if entity.children else entity.content
        # return f"{indent}{entity.index}. {content}"
        return f"{indent}{entity.index}. {entity.content}"
    elif isinstance(entity, UnorderedListItem) and linemode:
        # content = convert_entities_to_text(entity.children, indent + '  ', inline=True) if entity.children else entity.content
        # return f"{indent}- {content}"
        return f"{indent}- {entity.content}"
    elif isinstance(entity, (OrderedListItem, UnorderedListItem)) and not linemode:
        prefix = f"{entity.level * 2 * ' '}{entity.index}. " if isinstance(entity, OrderedListItem) else f"{entity.level * 2 * ' '}- "
        # prefix = f"{indent}{entity.index}. " if isinstance(entity, OrderedListItem) else f"{indent}- "
        content = convert_entities_to_text(entity.children, inline=True)
        return f"{prefix}{content}"
    elif isinstance(entity, LinkEntity):
        return f"[{entity.content}]({entity.url})"
    elif isinstance(entity, ImageEntity):
        return f"![{entity.content}]({entity.url})"
    elif isinstance(entity, InlineLink):
        return f"[{entity.content}]({entity.url})"
    elif isinstance(entity, EmptyLine):
        return f"{entity.content}"
    elif isinstance(entity, Text):
        return f"{entity.content}"
    elif isinstance(entity, Paragraph):
        return convert_entities_to_text(entity.children, inline=True)
    elif isinstance(entity, DisplayMath):
        return f"$$\n{entity.content}\n$$"
    elif isinstance(entity, InlineMath):
        return f"${entity.content}$"
    elif isinstance(entity, CompositeEntity):
        if linemode:
            return entity.content
        else:
            return convert_entities_to_text(entity.children, indent, inline=True)
    else:
        return str(entity)

def convert_entities_to_text(entities, indent='', inline=False, linemode=False):
    result = []
    for index, entity in enumerate(entities):
        # print("entity", entity)
        converted = convert_entity_to_text(entity, indent, linemode=linemode)
        if inline:
            result.append(converted)
        elif index != len(entities) - 1 or (index == len(entities) - 1 and isinstance(entities[-1], EmptyLine)):
            result.append(converted + '\n')
        else:
            result.append(converted)

    if result[-1] == '\n':
        result = result[:-1]
    if inline:
        return ''.join(result).rstrip()
    else:
        return ''.join(result)

def save_text_to_file(text: str, file_path: str):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def process_markdown_entities_and_save(entities, file_path, raw_text=None, linemode=False):
    # Step 1: Convert entities to text
    text_output = convert_entities_to_text(entities, linemode=linemode)
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

def check_markdown_parse(markdown_file_path, output_file_path="output.md", delimiter='\n', debug=False):
    # 读取 Markdown 文件
    markdown_text = read_markdown_file(markdown_file_path)

    # 分割 Markdown 文档
    paragraphs = split_markdown(markdown_text, delimiter=delimiter)

    # 解析 Markdown 文档
    parsed_entities = parse_markdown(paragraphs, delimiter=delimiter)
    if debug:
        # print(parsed_entities)
        for entity in parsed_entities:
            print(entity)
            if hasattr(entity, 'children'):
                for child in entity.children:
                    print("child", child)

    # 将解析结果转换为文本
    converted_text = convert_entities_to_text(parsed_entities)

    # 检查原始文本和转换后的文本是否相同
    # print(converted_text)
    if markdown_text != converted_text:
        save_text_to_file(converted_text, output_file_path)
        raise ValueError("The converted text does not match the original text.")

    return parsed_entities

def escape_code_block(content):
    # 使用html.escape函数进行基本的HTML转义
    import html
    escaped_content = html.escape(content)

    # 处理可能导致问题的其他特殊字符
    escaped_content = escaped_content.replace('\n', '&#10;')  # 换行符
    escaped_content = escaped_content.replace('\r', '&#13;')  # 回车符
    escaped_content = escaped_content.replace('\t', '&#9;')   # 制表符
    escaped_content = escaped_content.replace(' ', '&#32;')   # 空格
    escaped_content = escaped_content.replace('`', '&#96;')   # 反引号
    escaped_content = escaped_content.replace('$', '&#36;')   # 美元符号（可能与数学公式冲突）

    # 处理EOF和其他控制字符
    escaped_content = ''.join('&#%d;' % ord(c) if ord(c) < 32 or ord(c) == 127 else c for c in escaped_content)

    return escaped_content

def convert_entities_to_xue(entities):
    for entity in entities:
        print(entity)
    def process_entity(entity):
        if isinstance(entity, TitleEntity):
            header_tag = globals()[f'H{entity.level}']
            size_class = {
                1: "text-4xl",
                2: "text-3xl",
                3: "text-2xl",
                4: "text-xl",
                5: "text-lg",
                6: "text-base"
            }.get(entity.level, "text-base")
            return header_tag(entity.content, class_=f"font-bold mt-4 mb-4 text-gray-800 dark:text-gray-200 {size_class}")

        elif isinstance(entity, CodeBlock):
            escaped_content = escape_code_block(entity.content)
            code_block = Pre(
                Code(escaped_content, class_=f"language-{entity.language}"),
                class_="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 overflow-x-auto"
            )
            return Div(code_block, class_="code-block-wrapper mt-4")

        # elif isinstance(entity, ListItem):
        #     print("entity", entity)
        #     print("entity.content", entity.content)
        #     print("entity.children", entity.children)
        #     return Li(process_children(entity.children) if hasattr(entity, 'children') else entity.content, class_="mb-2")

        elif isinstance(entity, LinkEntity) or isinstance(entity, InlineLink):
            return A(entity.content, href=entity.url, class_="mr-0 text-primary-light dark:text-primary-dark hover:underline")

        elif isinstance(entity, EmptyLine):
            return None

        elif isinstance(entity, OrderedListItem):
            content = process_children(entity.children) if hasattr(entity, 'children') else [entity.content]
            return Ol(Li(*content, class_="mb-0"), start=entity.index, class_="list-decimal mb-1 ml-4")
            # return Ol(Li(*content, class_="mb-2"), start=entity.index, class_="list-decimal list-inside mb-4")
            # return Ol(Li(Div(*content, class_ = "flex items-center"), class_="mb-0"), class_="list-decimal mb-0 ml-4")

        elif isinstance(entity, UnorderedListItem):
            # print("UnorderedListItem", hasattr(entity, 'children'))
            content = process_children(entity.children) if hasattr(entity, 'children') else [entity.content]
            # return Ul(Li(*content, class_="mb-0"), class_="list-disc list-inside mb-0")
            # return Ul(Li(Div(*content, class_ = "flex items-center"), class_="mb-0"), class_="list-disc mb-0 ml-4")
            return Ul(Li(*content, class_="mb-0"), class_="list-disc mb-1 ml-4")
            # return Ul(Li(Div(*content, class_ = "flex flex-wrap"), class_="mb-0"), class_="list-disc mb-0 ml-4")

        elif isinstance(entity, Paragraph):
            content = process_children(entity.children) if hasattr(entity, 'children') else [entity.content]
            # return Span(process_inline_elements(entity.content), class_="mr-2 flex-shrink-0")
            # return P(process_inline_elements(entity.content), class_="mr-2 mb-0")
            return P(*content, class_="mr-0 mb-1")

        elif isinstance(entity, ImageEntity):
            return Image(src=entity.content, alt=entity.alt_text, class_="max-w-full h-auto rounded-lg shadow-lg mb-4")

        elif isinstance(entity, DisplayMath):
            return Div(entity.content, class_="math-display bg-gray-50 dark:bg-gray-800 p-4 rounded-lg mb-4")

        elif isinstance(entity, InlineMath):
            return Span(entity.content, class_="math-inline")

        elif isinstance(entity, CompositeEntity):
            return Div(*[process_entity(child) for child in entity.children], class_="composite-entity flex items-center mb-2")

        else:
            return str(entity.content)

    def process_children(children):
        # result = []
        # for child in children:
        #     if child is not None:
        #         item = process_entity(child)
        #         if item is not None:
        #             if isinstance(item, (Div, Span, H1, H2, H3, H4, H5, H6)):
        #                 result.append(item)
        #             else:
        #                 result.append(Span(item, class_="mr-2 flex-shrink-0"))
        # return result
        for child in children:
            print("child", child)

        return [process_entity(child) for child in children if child is not None if process_entity(child) is not None]
        # return [Span(process_entity(child), class_="mr-2 w-full") for child in children if child is not None if process_entity(child) is not None]
        # return [Span(process_entity(child), class_="mr-2 flex-shrink-0") for child in children if child is not None if process_entity(child) is not None]
        # return [process_entity(child) for child in children if child is not None if process_entity(child) is not None]

    def process_inline_elements(content):
        # 这里可以添加处理行内元素的逻辑，比如链接、行内数学公式等
        # 现在我们简单地返回内容
        return content

    html_body = Body(class_="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-6 max-w-3xl mx-auto")
    html_body.children.extend(process_children(entities))

    return html_body

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
    # check_markdown_parse("/Users/yanyuming/Downloads/GitHub/PurePage/index.md", "output.md")
    check_markdown_parse("/Users/yanyuming/Downloads/GitHub/PurePage/post/ViT/index.md", "output.md")
    # check_markdown_parse("/Users/yanyuming/Downloads/GitHub/xue/README.md", "output.md")