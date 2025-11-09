import argparse
from utils.pdf_loader import load_pdfs_from_folder
from utils.embed import VectorStore

def main(data_folder="data"):
    docs = load_pdfs_from_folder(data_folder)
    if not docs:
        print("Tidak ada PDF di folder:", data_folder)
        return
    vs = VectorStore()
    vs.build(docs)
    print("Ingest selesai.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data", help="Folder yang berisi PDF")
    args = parser.parse_args()
    main(args.data)
