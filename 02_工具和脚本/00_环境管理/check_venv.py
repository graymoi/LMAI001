import subprocess
import sys

print("=" * 60)
print("Python 虚拟环境检查")
print("=" * 60)

# 检查conda
try:
    result = subprocess.run(['conda', '--version'], capture_output=True, text=True, timeout=5)
    print(f"Conda 版本: {result.stdout.strip()}")
except:
    print("Conda: 未安装")

print()

# 检查venv
try:
    import venv
    print("venv 模块: 可用")
except:
    print("venv 模块: 不可用")

print()

# 检查当前环境
print("=" * 60)
print("当前环境详情")
print("=" * 60)
print(f"Python 可执行文件: {sys.executable}")
print(f"sys.prefix: {sys.prefix}")
if hasattr(sys, 'base_prefix'):
    print(f"sys.base_prefix: {sys.base_prefix}")
    if sys.prefix != sys.base_prefix:
        print("✓ 在虚拟环境中")
    else:
        print("✗ 不在虚拟环境中（使用系统Python）")
else:
    print("✗ 不在虚拟环境中（使用系统Python）")

print()

# 检查环境变量
print("=" * 60)
print("环境变量")
print("=" * 60)
import os
if 'VIRTUAL_ENV' in os.environ:
    print(f"VIRTUAL_ENV: {os.environ['VIRTUAL_ENV']}")
else:
    print("VIRTUAL_ENV: 未设置")

if 'CONDA_DEFAULT_ENV' in os.environ:
    print(f"CONDA_DEFAULT_ENV: {os.environ['CONDA_DEFAULT_ENV']}")
else:
    print("CONDA_DEFAULT_ENV: 未设置")

print()

# 检查pip安装位置
print("=" * 60)
print("pip 安装位置")
print("=" * 60)
try:
    import pip
    print(f"pip 模块位置: {pip.__file__}")
except:
    print("pip 模块位置: 无法确定")

try:
    result = subprocess.run([sys.executable, '-m', 'pip', 'show', 'pip'], capture_output=True, text=True, timeout=5)
    for line in result.stdout.split('\n'):
        if line.startswith('Location:'):
            print(f"pip 安装位置: {line.split(':', 1)[1].strip()}")
except:
    print("pip 安装位置: 无法确定")

print()

# 检查常见包的安装位置
print("=" * 60)
print("常见包的安装位置")
print("=" * 60)
packages = ['numpy', 'pandas', 'matplotlib', 'requests']
for pkg in packages:
    try:
        mod = __import__(pkg)
        print(f"{pkg:15s}: {mod.__file__}")
    except ImportError:
        print(f"{pkg:15s}: 未安装")

print()
print("=" * 60)