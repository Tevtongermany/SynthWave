import os
import requests
import globals
import zipfile
import shutil


def setup(bot):
    r = requests.get(globals.SYNTHWAVE_GITHUB_REPO_URL)
    if r.ok:
        rjson = r.json()
        version = rjson["tag_name"]
        sourcecode_zip_url = rjson["zipball_url"] 
        if globals.VERSION == version:
            print("No New version!")
            return
        print("New Update found! do you want to update?")
        prompt = input("Y/N: ")
        if prompt == "Y":
            src = requests.get(sourcecode_zip_url, allow_redirects=True)
            with open(f"{version}.zip",mode="wb") as file:
                file.write(src.content)
            with zipfile.ZipFile(f"{version}.zip",'r') as zipfile_ref:
                zipfile_ref.extractall(f"{version}")
            os.remove(f"{version}.zip")


            


        