def get_version() -> str:
    with open("./gitgrade/version.txt", "r", encoding="utf8") as version_file:
        return version_file.read().rstrip()
