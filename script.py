# your_script.py
import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python your_script.py <GitHub_repo_URL>")
        sys.exit(1)

    github_repo_url = sys.argv[1]

    # Git 初始化
    subprocess.run("git init", shell=True)

    # 将所有文件添加到暂存区
    subprocess.run("git add .", shell=True)

    # 提交到本地仓库
    subprocess.run("git commit -m \"Initial commit\"", shell=True)

    # 关联远程仓库
    subprocess.run(f"git remote add origin {github_repo_url}", shell=True)

    # 推送到远程仓库
    subprocess.run("git push -u origin master", shell=True)

if __name__ == "__main__":
    main()
