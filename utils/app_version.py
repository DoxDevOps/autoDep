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
