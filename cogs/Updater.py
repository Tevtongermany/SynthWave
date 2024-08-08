import filecmp
import os
import requests
import globals
import zipfile
import shutil


def setup(bot):
    try:
        r = requests.get(globals.SYNTHWAVE_GITHUB_REPO_URL)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repository information: {e}")
        return

    rjson = r.json()
    version = rjson["tag_name"]
    sourcecode_zip_url = rjson["zipball_url"]

    if globals.VERSION >= version:
        print("No New version!")
        return

    print("New Update found! Do you want to update?")
    prompt = input("Y/N: ")
    if prompt.upper() == "Y":
        try:
            src = requests.get(sourcecode_zip_url, allow_redirects=True)
            src.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the source code: {e}")
            return

        zip_path = f"{version}.zip"
        with open(zip_path, mode="wb") as file:
            file.write(src.content)

        extract_path = f"{version}_temp"
        with zipfile.ZipFile(zip_path, 'r') as zipfile_ref:
            zipfile_ref.extractall(extract_path)

        os.remove(zip_path)

        new_version_folder = os.path.join(extract_path, os.listdir(extract_path)[0])
        
        def update_files(src_folder, dest_folder):
            for root, dirs, files in os.walk(src_folder):
                for file in files:
                    src_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(src_file_path, src_folder)
                    dest_file_path = os.path.join(dest_folder, relative_path)
                    print(src_file_path)
                    if not os.path.exists(dest_file_path) or not filecmp.cmp(src_file_path, dest_file_path, shallow=False):
                        print(f"Updating file: {dest_file_path} {src_file_path}")
                        dest_file_dir = os.path.dirname(dest_file_path)
                        os.makedirs(dest_file_dir, exist_ok=True)
                        shutil.copy2(src_file_path, dest_file_path)

        update_files(new_version_folder, "./")

        shutil.rmtree(extract_path)
        print("Update completed successfully!")


            


        