import json
import os

import firebase_admin
from dotenv import find_dotenv, load_dotenv
from firebase_admin import credentials, db


def initialize_firebase():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    # Parse the credentials as JSON
    cred_dict = {
        "type": os.getenv("FIREBASE_TYPE"),
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace(
            "\\n", "\n"
        ),  # Replace \\n with actual newlines
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
        "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv(
            "FIREBASE_AUTH_PROVIDER_X509_CERT_URL"
        ),
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN"),
    }

    # Remove any None values
    cred_dict = {k: v for k, v in cred_dict.items() if v is not None}

    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {"databaseURL": os.getenv("FIREBASE_URL")})


def backup_songs(songs_ref, backup_ref):
    songs = songs_ref.get()

    if songs is None:
        # print("No songs found")
        return []

    # print(f"Found {len(songs)} songs")
    backup_ref.set(songs)
    # print("Backup created/updated")
    return songs


def get_unique_songs(songs):
    songs_names = set()
    unique_songs = []

    for song in songs:
        last_len = len(songs_names)
        try:
            songs_names.add(song["title"])
            if len(songs_names) > last_len:
                unique_songs.append(song)
        except KeyError:
            print(f"Song without title: {song}")

    # print(f"Found {len(songs_names)} unique songs")
    return unique_songs


def update_songs_from_file(unique_songs, songs_names, file_path):
    try:
        with open(file_path, "r") as f:
            scrapped_songs = json.load(f)
            print(f"Found {len(scrapped_songs)} scrapped songs")
            for song in scrapped_songs:
                last_len = len(songs_names)
                try:
                    songs_names.add(song["title"])
                    if len(songs_names) > last_len:
                        unique_songs.append(song)
                except KeyError:
                    print(f"Song without title: {song}")
    except FileNotFoundError:
        print("No scrapped_songs.json file found")


def update_database(songs_ref, backup_ref, unique_songs):
    songs_ref.set(unique_songs)
    # print("Database updated")

    backup_ref.set(unique_songs)
    # print("Backup updated")


if __name__ == "__main__":
    print("Starting Firebase uploader")

    initialize_firebase()
    print("Firebase initialized correctly")

    songs_ref = db.reference("/songs")
    backup_ref = db.reference("/songs_backup")
    print("Database references created")

    songs = backup_songs(songs_ref, backup_ref)
    print("Backup created/updated")

    unique_songs = get_unique_songs(songs)
    print("Unique songs created")

    update_songs_from_file(
        unique_songs,
        set(song["title"] for song in unique_songs),
        "data/scrapped_songs.json",
    )
    print("Scrapped songs added")

    update_database(songs_ref, backup_ref, unique_songs)
    print("Database updated")
