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
        folder_count = sum(1 for item in contents if item['type'] == 'dir')
        subfolders = [item['name'] for item in contents if item['type'] == 'dir']
        return file_count, folder_count, subfolders
    else:
        print(f"错误: {response.status_code}")
        print(response.text)
        return None, None, None

def count_files_in_subfolders(owner, repo, base_path, token):
    _, _, subfolders = count_files_in_folder(owner, repo, base_path, token)
    if subfolders is None:
        return None

    subfolder_counts = {}
    for subfolder in subfolders:
        full_path = f"{base_path}/{subfolder}"
        file_count, _, _ = count_files_in_folder(owner, repo, full_path, token)
        if file_count is not None:
            subfolder_counts[subfolder] = file_count

    return subfolder_counts

# 主程序
if __name__ == "__main__":
    # 使用示例
    owner = "cloud368"
    repo = "repo"
    path = "repo/debs"
    token = "PAT"

    file_count, folder_count, _ = count_files_in_folder(owner, repo, path, token)
    if file_count is not None:
        print(f"文件夹 '{path}' 中的文件数量: {file_count}")
        print(f"文件夹 '{path}' 中的子文件夹数量: {folder_count}")

    subfolder_counts = count_files_in_subfolders(owner, repo, path, token)
    if subfolder_counts:
        print("\n子文件夹中的文件数量:")
        for subfolder, count in subfolder_counts.items():
            print(f"  {subfolder}: {count}")