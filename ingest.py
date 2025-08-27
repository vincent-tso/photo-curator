from PIL import Image, ExifTags

# Ingest folder
# { path, size, mime, exif_datetime, phash? }
# Return scan.json
# Acceptance criteria: python app.py scan --input ~/photo_sample

def scan_folder(img_path):
    try:
        with Image.open(img_path) as img:
            print(img)
            img_exif = img.getexif()

            print(img_exif)

            for k, v in img_exif.items():
                tag_name = ExifTags.TAGS.get(k)
                print(tag_name, v)

    except OSError:
        pass

    return 1