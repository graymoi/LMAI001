"""
合并需求规格说明书的多个文件
"""

def read_file(file_path):
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件 {file_path} 失败: {e}")
        return ""

def merge_files():
    """合并需求规格说明书文件"""
    base_path = r"f:\AIlm\000项目管理\标书编写"

    # 主文档
    main_doc = read_file(f"{base_path}\\需求规格说明书_天津背街小巷诊断数字化管理平台.md")

    # 续文档1
    cont1_doc = read_file(f"{base_path}\\需求规格说明书_天津背街小巷诊断数字化管理平台_续.md")

    # 续文档2
    cont2_doc = read_file(f"{base_path}\\需求规格说明书_天津背街小巷诊断数字化管理平台_续2.md")

    # 合并文档
    merged_doc = main_doc

    # 找到主文档的结束位置，添加续文档内容
    if cont1_doc:
        # 移除续文档的标题行
        cont1_lines = cont1_doc.split('\n')
        if cont1_lines[0].startswith('#'):
            cont1_lines = cont1_lines[1:]
        merged_doc += '\n\n' + '\n'.join(cont1_lines)

    if cont2_doc:
        # 移除续文档的标题行
        cont2_lines = cont2_doc.split('\n')
        if cont2_lines[0].startswith('#'):
            cont2_lines = cont2_lines[1:]
        merged_doc += '\n\n' + '\n'.join(cont2_lines)

    # 保存合并后的文档
    output_path = f"{base_path}\\需求规格说明书_天津背街小巷诊断数字化管理平台_完整版.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(merged_doc)

    print(f"合并完成！")
    print(f"输出文件: {output_path}")
    print(f"主文档长度: {len(main_doc)} 字符")
    print(f"续文档1长度: {len(cont1_doc)} 字符")
    print(f"续文档2长度: {len(cont2_doc)} 字符")
    print(f"合并后长度: {len(merged_doc)} 字符")

if __name__ == "__main__":
    merge_files()