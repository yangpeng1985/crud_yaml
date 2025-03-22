import subprocess

try:
    # 执行 pip freeze 命令
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
    # 将输出保存到 requirements.txt 文件
    with open('requirements.txt', 'w') as f:
        f.write(result.stdout)
    print("requirements.txt 文件已生成。")
except subprocess.CalledProcessError as e:
    print(f"执行命令时出错: {e.stderr}")
except Exception as e:
    print(f"发生未知错误: {e}")
    