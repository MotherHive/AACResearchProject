from pathlib import Path
from urllib.request import urlopen
import nltk

DATA_URL = "https://aclanthology.org/attachments/I17-1099.Datasets.zip"
PROJECT_FOLDER = Path(__file__).resolve().parent


def download_data():
    folder = PROJECT_FOLDER / "data" / "raw"
    folder.mkdir(parents=True, exist_ok=True)

    archive = folder / "dailydialog.zip"

    if archive.exists():
        print("Dataset already downloaded.")
        return

    with urlopen(DATA_URL, timeout=60) as response:
        contents = response.read()

    archive.write_bytes(contents)
    print("Downloaded:", archive)


if __name__ == "__main__":
    download_data()

    nltk.download(
        "averaged_perceptron_tagger_eng",
        download_dir=str(PROJECT_FOLDER / "data" / "raw" / "nltk"),
        raise_on_error=True,
    )

    nltk.download(
        "wordnet",
        download_dir=str(PROJECT_FOLDER / "data" / "raw" / "nltk"),
        raise_on_error=True,
    )

