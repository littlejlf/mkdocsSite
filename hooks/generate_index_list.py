"""
MkDocs hook: 自动为分类 index 页面生成子文章列表。

当 navigation.indexes 启用时，某个分类下有 index.md，
hook 自动在该 index 页面末尾插入子页面的链接列表。
"""

from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Section


def on_nav(nav, config, files):
    """
    递归遍历导航树，构建 {index_page_src_uri: [child_items]} 映射。
    存入 config 供 on_page_markdown 使用。
    """
    mapping = {}

    def _walk(items):
        for item in (items or []):
            if isinstance(item, Section) and item.children:
                index_page = None
                others = []
                for child in item.children:
                    if isinstance(child, Page) and child.is_index:
                        index_page = child
                    else:
                        others.append(child)
                if index_page is not None and others:
                    mapping[index_page.file.src_uri] = others
                _walk(item.children)

    _walk(nav)
    config['_index_page_mapping'] = mapping
    return nav


def on_page_markdown(markdown, page, config, files):
    # ---- AI 对话页面格式化 ----
    if markdown.lstrip().startswith('> From:') and config.get('extra', {}).get('conversation_formatting', True):
        markdown = _format_conversation(markdown)
        page._is_conversation = True

    # ---- 分类 index 页面列表生成 ----
    mapping = config.get('_index_page_mapping', {})
    src_uri = page.file.src_uri

    if src_uri not in mapping:
        return markdown

    children = mapping[src_uri]
    listing = _build_listing(children, page)
    if not listing:
        return markdown

    marker = '<!-- more -->'
    if marker in markdown:
        markdown = markdown.replace(marker, listing)
    else:
        markdown = markdown.rstrip() + '\n\n' + listing

    return markdown


def _format_conversation(markdown):
    """将 AI 对话格式美化为简洁灰度风格。"""
    import re

    # 1. 来源 URL → 灰色引用
    markdown = re.sub(
        r'^> From:\s*(.+?)(?:\n|$)',
        r'<blockquote class="conv-source">来源：<a href="\1">\1</a></blockquote>\n',
        markdown, count=1
    )

    # 2. 整体包裹
    markdown = '<div class="ai-conversation">\n' + markdown

    # 3. 用户提问：替换 "# you asked\n" 为 [问] 标签 + 时间戳
    markdown = re.sub(
        r'^# you asked *\n(?:message time: *(.+?))?\n?',
        lambda m: (
            '<div class="conv-block">\n'
            '<p class="conv-label conv-label-q">[问]</p>\n'
            + (f'<p class="conv-time">{m.group(1)}</p>\n' if m.group(1) else '')
        ),
        markdown, flags=re.MULTILINE
    )

    # 4. AI 回复：替换 "# chatgpt response\n" 为 [答] 标签（前一个块自然闭合）
    markdown = re.sub(
        r'^# chatgpt response *\n?',
        '</div>\n<div class="conv-block">\n<p class="conv-label conv-label-a">[答]</p>\n',
        markdown, flags=re.MULTILINE
    )

    # 5. 收尾闭合
    markdown = markdown.rstrip() + '\n</div>\n'

    return markdown


def _build_listing(items, current_page, level=0):
    """递归生成 markdown 列表（使用 .md 相对路径）。"""
    import os.path
    indent = '  ' * level
    lines = []
    cur_dir = os.path.dirname(current_page.file.src_uri)

    for item in items:
        if isinstance(item, Section):
            lines.append(f'{indent}- **{item.title}**')
            if item.children:
                sub = _build_listing(item.children, current_page, level + 1)
                if sub:
                    lines.append(sub)
        elif isinstance(item, Page):
            title = item.title or item.file.name
            # 构建相对于当前 index.md 的路径，确保使用正斜杠
            rel = os.path.relpath(item.file.src_uri, cur_dir).replace('\\', '/')
            date = ''
            if item.meta and item.meta.get('date'):
                d = item.meta['date']
                date = str(d) if not hasattr(d, 'strftime') else d.strftime('%Y-%m-%d')
            if date:
                lines.append(f'{indent}- [{title}]({rel}) — {date}')
            else:
                lines.append(f'{indent}- [{title}]({rel})')

    return '\n'.join(lines)
