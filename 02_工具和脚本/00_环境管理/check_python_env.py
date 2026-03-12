import sys
import site

print("=" * 60)
print("Python 环境信息")
print("=" * 60)
print(f"Python 版本: {sys.version}")
print(f"Python 路径: {sys.executable}")
print(f"Python 编译器: {sys.version_info}")
print()

print("=" * 60)
print("模块搜索路径 (sys.path)")
print("=" * 60)
for i, path in enumerate(sys.path, 1):
    print(f"{i}. {path}")
print()

print("=" * 60)
print("site-packages 位置")
print("=" * 60)
site_packages = site.getsitepackages()
for i, path in enumerate(site_packages, 1):
    print(f"{i}. {path}")
print()

print("=" * 60)
print("用户 site-packages 位置")
print("=" * 60)
user_site = site.getusersitepackages()
print(user_site)
print()

print("=" * 60)
print("虚拟环境检测")
print("=" * 60)
print(f"是否在虚拟环境中: {hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)}")
print(f"sys.prefix: {sys.prefix}")
if hasattr(sys, 'base_prefix'):
    print(f"sys.base_prefix: {sys.base_prefix}")
print()