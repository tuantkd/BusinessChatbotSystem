import re


def markdown_to_html(text):
    # Chuyển đổi văn bản nghiêng
    text = re.sub(r'_([^_]*?)_', r'<i>\1</i>', text)

    # Chuyển đổi văn bản đậm
    text = re.sub(r'\*\*([^\*]*?)\*\*', r'<b>\1</b>', text)

    # Chuyển đổi văn bản gạch bỏ
    text = re.sub(r'~~([^~]*?)~~', r'<del>\1</del>', text)

    # Chuyển đổi tiêu đề cấp 1
    text = re.sub(r'^# ([^\n]*)', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # Chuyển đổi tiêu đề cấp 2
    text = re.sub(r'^## ([^\n]*)', r'<h2>\1</h2>', text, flags=re.MULTILINE)

    # Chuyển đổi tiêu đề cấp 3
    text = re.sub(r'^### ([^\n]*)', r'<h3>\1</h3>', text, flags=re.MULTILINE)

    # Chuyển đổi danh sách không thứ tự
    text = re.sub(r'^- (.*)', r'<ul><li>\1</li></ul>', text, flags=re.MULTILINE)

    # Chuyển đổi danh sách có thứ tự
    text = re.sub(r'^[0-9]+\. (.*)', r'<ol><li>\1</li></ol>', text, flags=re.MULTILINE)

    # Chuyển đổi liên kết
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)

    # Chuyển đổi hình ảnh
    text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img alt="\1" src="\2">', text)

    # Chuyển đổi bảng
    lines = text.split('\n')
    table = []
    is_table = False
    for line in lines:
        if line.strip() == '':
            continue
        if line.startswith('|'):
            is_table = True
            table.append(line)
        elif is_table:
            break
    if table:
        html_table = '<table>\n'
        for row in table:
            html_table += '  <tr>\n'
            cells = row.strip('|').split('|')
            for cell in cells:
                html_table += f'    <td>{cell.strip()}</td>\n'
            html_table += '  </tr>\n'
        html_table += '</table>'
        text = text.replace('\n'.join(table), html_table)

    # \n -> <br>
    text = text.replace('\\n', '<br>')


    return text