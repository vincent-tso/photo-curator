from photocurator.ingest import scan_folder

if __name__ == "__main__":
    data = scan_folder("/Users/vincenttso/Documents/important")
    print(f"Scanned {len(data['items'])} items")

    for k, v in data.items():
        print(f"{k}: {v}")
        