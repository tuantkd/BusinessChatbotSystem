import re


import re

def is_ul_open(html_lines):
        ul_count = 0
        li_count = 0

        for line in reversed(html_lines):
            if '</ul>' in line:
                ul_count += 1
            if '<ul>' in line:
                ul_count -= 1
            if '<li>' in line:
                li_count += 1
            if '</li>' in line:
                li_count -= 1

            # Nếu tìm thấy một <ul> mà chưa bị đóng, trả về True
            if ul_count < 0:
                return True

        return False

def markdown_to_html(markdown_text):
    # Tách các dòng văn bản
    lines = markdown_text.strip().split('\n')
    
    html_lines = []
    in_table = False

    for line in lines:
        line = line.strip()

        # Chuyển đổi in đậm
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)

        # Chuyển đổi in nghiêng với dấu gạch dưới
        line = re.sub(r'_(.*?)_', r'<em>\1</em>', line)

        # Chuyển đổi bảng
        if line.startswith('|'):
            if not in_table:
                html_lines.append('<table>')
                in_table = True
            cells = ''.join([f'<td>{cell.strip()}</td>' for cell in line.split('|') if cell.strip() != ''])
            html_lines.append(f'<tr>{cells}</tr>')
        else:
            if in_table:
                html_lines.append('</table>')
                in_table = False

            # Chuyển đổi danh sách không thứ tự
            if line.startswith('- '):
                if not is_ul_open(html_lines):
                    html_lines.append('<ul>')
                html_lines.append(f'<li>{line[2:]}</li>')
            else:
                if is_ul_open(html_lines):
                    html_lines.append('</ul>')
                html_lines.append(f'<p>{line}</p>')

    # Đóng thẻ ul nếu còn mở
    if is_ul_open(html_lines):
        html_lines.append('</ul>')

    # Đóng thẻ table nếu còn mở
    if in_table:
        html_lines.append('</table>')

    return '\n'.join(html_lines)

def process_messages(messages):
    processed_messages = []
    for message in messages:
        if 'text' in message:
            # Chuyển đổi Markdown sang HTML cho tin nhắn dạng văn bản
            html_content = markdown_to_html(message['text'])
            processed_messages.append({
                'text': html_content
            })
        elif 'custom' in message:
            # Xử lý tin nhắn dạng quick replies
            if message['custom']['type'] == 'quick_replies':
                quick_replies = message['custom']['content']
                quick_replies['title'] = markdown_to_html(quick_replies['title'])
                for button in quick_replies['buttons']:
                    button['title'] = button['title']
                    button['description'] = markdown_to_html(button['description'])
                processed_messages.append({
                    'type': 'custom',
                    'custom': {
                        'type': 'quick_replies',
                        'content': quick_replies
                    }
                })
    return processed_messages