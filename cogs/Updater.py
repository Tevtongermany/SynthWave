import requests
import globals



def setup(bot):
    r = requests.get(globals.SYNTHWAVE_GITHUB_REPO_URL)