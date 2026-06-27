#!/usr/bin/env python3
"""Build script: reads bio.md and injects content into index.html."""

import re

def md_to_html(md_text):
    """Convert simple markdown sections to HTML paragraphs."""
    sections = []
    current_section = None
    current_lines = []

    for line in md_text.strip().split('\n'):
        if line.startswith('## '):
            if current_section is not None:
                sections.append((current_section, '\n'.join(current_lines).strip()))
            current_section = line[3:].strip()
            current_lines = []
        elif line.strip() == '':
            if current_lines:
                current_lines.append('')
        else:
            current_lines.append(line)

    if current_section is not None:
        sections.append((current_section, '\n'.join(current_lines).strip()))

    html_parts = []
    for title, content in sections:
        html_parts.append(f'<p class="section-header">/* {title} */</p>')
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        for para in paragraphs:
            para = para.replace('\n', ' ')
            para = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', para)
            html_parts.append(f'<p>{para}</p>')

    return '\n'.join(html_parts)


def inject_bio(html, start_marker, end_marker, indent, bio_title):
    """Replace content between start_marker and end_marker with new bio HTML."""
    # Build bio content from bio.md
    bio_html = md_to_html(open('bio.md').read())
    lines = bio_html.split('\n')

    block = f'{indent}<p class="section-header bio-title">/** {bio_title} */</p>\n'
    for line in lines:
        block += f'{indent}{line}\n'

    start = html.find(start_marker)
    end = html.find(end_marker)

    if start == -1 or end == -1:
        print(f'ERROR: markers {start_marker} / {end_marker} not found!')
        return html

    html = html[:start + len(start_marker) + 1] + block + html[end:]
    return html


def main():
    with open('index.html', 'r') as f:
        html = f.read()

    indent12 = '            '  # 12 spaces

    html = inject_bio(html,
        '<!-- BIO_DESKTOP_START -->',
        '<!-- BIO_DESKTOP_END -->',
        indent12, 'Bio')

    html = inject_bio(html,
        '<!-- BIO_MOBILE_START -->',
        '<!-- BIO_MOBILE_END -->',
        indent12, 'Bio')

    with open('index.html', 'w') as f:
        f.write(html)

    print('Build complete: bio.md → index.html')


if __name__ == '__main__':
    main()
