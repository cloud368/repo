import requests

def count_files_in_folder(owner, repo, path, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        contents = response.json()
        file_count = sum(1 for item in contents if item['type'] == 'file')
        return file_count
    else:
        print(f"错误: {response.status_code}")
        print(response.text)
        return None

# 主程序
if __name__ == "__main__":
    # 使用示例
    owner = "cloud368"
    repo = "repo"
    path = "repo/debs/"
    token = "PAT"

    file_count = count_files_in_folder(owner, repo, path, token)
    if file_count is not None:
        print(f"文件夹 '{path}' 中的文件数量: {file_count}")
