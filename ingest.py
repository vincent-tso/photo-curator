from PIL import Image, ExifTags
import magic

# Ingest folder
# { path, size, mime, exif_datetime, phash? }
# Return scan.json
# Acceptance criteria: python app.py scan --input ~/photo_sample

def scan_folder(img_path):
    json_res = None

    try:
        with Image.open(img_path) as img:
            img_exif = img.getexif()

            if img_exif:
                img_path = img.filename
                img_size = img.size
                img_mime = magic.from_file(img_path, mime=True)
                img_date_time = img_exif.get(ExifTags.TAGS.get(ExifTags.Base.DateTime), "")

                json_res = {
                    "path": img_path,
                    "size": img_size,
                    "exif_datetime": img_date_time,
                    "mime": img_mime
                }

            else:
                print("\nNo EXIF data found.")

    except OSError:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")

    return json_res
