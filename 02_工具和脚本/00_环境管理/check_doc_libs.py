import sys

print("=" * 60)
print("文档处理库检查")
print("=" * 60)

doc_libs = [
    'docx',
    'openpyxl',
    'xlsxwriter',
    'pypdf',
    'pdfplumber',
    'reportlab',
    'markitdown',
    'python_docx'
]

installed = []
not_installed = []

for lib in doc_libs:
    try:
        mod = __import__(lib)
        version = getattr(mod, '__version__', 'unknown')
        installed.append((lib, version))
        print(f"✓ {lib:15s} {version}")
    except ImportError:
        not_installed.append(lib)
        print(f"✗ {lib:15s} 未安装")

print()
print("=" * 60)
print("总结")
print("=" * 60)
print(f"已安装: {len(installed)} 个")
print(f"未安装: {len(not_installed)} 个")

if not_installed:
    print()
    print("需要安装的库:")
    for lib in not_installed:
        print(f"  - {lib}")
    print()
    print("安装命令:")
    print(f"python -m pip install {' '.join(not_installed)}")