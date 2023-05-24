apps = [
        {
            "app_name": "BHT-EMR-API",
            "app_version": "v4.17.2"
        },
        {
            "app_name": "HIS-Core",
            "app_version": "v1.8.1"
        },
    ]

instruction_set = [
    "bundle install --local",
    "./bin/update_art_metadata.sh development"
]

def getTag(app_dir):
    for app in apps:
        if  app["app_name"] in app_dir:
            return app["app_version"]
    return None

def generate_git_url(directory_path):
    base_url = "3000/gitea/"
    # Split the directory path by "/"
    path_parts = directory_path.split("/")
    # Get the last part of the path as the repository name
    repository_name = path_parts[-1]
    # Append ".git" to the repository name
    repository_name_with_extension = repository_name + ".git"
    # Concatenate the base URL, repository name, and ".git" extension
    git_url = base_url + repository_name_with_extension
    return git_url
