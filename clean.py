import os, shutil

FILE_NAMES_TO_REMOVE = [
    "__pycache__",
    "simulated_games",
]

FILE_EXTENSIONS_TO_REMOVE = []


def clean_folder(folder: str | None = ".") -> None:
    for content in os.scandir(folder):

        if content.is_file():
            name, ext = os.path.splitext(content.name)
            ext = ext.lstrip(".")
            if ext in FILE_EXTENSIONS_TO_REMOVE or content.name in FILE_NAMES_TO_REMOVE:
                os.remove(content.path)

        elif content.is_dir():
            if content.name in FILE_NAMES_TO_REMOVE:
                shutil.rmtree(content.path)
            else:
                clean_folder(content.path)


if __name__ == "__main__":
    clean_folder()
