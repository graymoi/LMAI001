import os
from docx import Document

# 读取大纲文件
file_outline = r"f:\AIlm\000项目管理\标书编写\大纲11.12晚.docx"
file_meeting = r"f:\AIlm\000项目管理\标书编写\背街小巷治理会议工作部署-修.docx"

def read_docx(file_path):
    if os.path.exists(file_path):
        try:
            doc = Document(file_path)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            return '\n'.join(fullText)
        except Exception as e:
            return f"读取出错：{e}"
    else:
        return "文件不存在"

# 读取文件
outline_content = read_docx(file_outline)
meeting_content = read_docx(file_meeting)

# 保存到文件
output_file = r"f:\AIlm\000项目管理\标书编写\大纲_读取内容.md"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=== 大纲文件内容 ===\n\n")
    f.write(outline_content)
    f.write("\n\n=== 会议工作部署文件内容 ===\n\n")
    f.write(meeting_content)

print(f"✅ 文件已读取并保存到：{output_file}")
