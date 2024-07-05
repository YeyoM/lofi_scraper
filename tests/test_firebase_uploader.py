import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import firebase_uploader


class TestFirebaseUploader(unittest.TestCase):
    @patch("firebase_uploader.db.reference")
    @patch("firebase_uploader.credentials.Certificate")
    @patch("firebase_uploader.firebase_admin.initialize_app")
    def test_initialize_firebase(
        self, mock_initialize_app, mock_certificate, mock_db_reference
    ):
        mock_certificate.return_value = MagicMock()
        mock_initialize_app.return_value = MagicMock()
        firebase_uploader.initialize_firebase()
        mock_initialize_app.assert_called_once()
        mock_certificate.assert_called_once()
        mock_db_reference.assert_not_called()

    @patch("firebase_uploader.db.reference")
    def test_backup_songs(self, mock_db_reference):
        mock_ref = MagicMock()
        mock_db_reference.return_value = mock_ref
        mock_ref.get.return_value = [{"title": "Song 1"}, {"title": "Song 2"}]
        songs = firebase_uploader.backup_songs(mock_ref, mock_ref)
        self.assertEqual(len(songs), 2)
        mock_ref.set.assert_called_once()

    def test_get_unique_songs(self):
        songs = [{"title": "Song 1"}, {"title": "Song 2"}, {"title": "Song 1"}]
        unique_songs = firebase_uploader.get_unique_songs(songs)
        self.assertEqual(len(unique_songs), 2)

    @patch("builtins.open", create=True)
    def test_update_songs_from_file(self, mock_open):
        mock_open.side_effect = [
            unittest.mock.mock_open(read_data='[{"title": "Song 3"}]').return_value,
            FileNotFoundError,
        ]
        unique_songs = [{"title": "Song 1"}, {"title": "Song 2"}]
        songs_names = set(song["title"] for song in unique_songs)

        firebase_uploader.update_songs_from_file(
            unique_songs, songs_names, "data/scrapped_songs.json"
        )
        self.assertEqual(len(unique_songs), 3)

        songs_names = set(song["title"] for song in unique_songs)
        firebase_uploader.update_songs_from_file(
            unique_songs, songs_names, "non_existent_file.json"
        )
        self.assertEqual(len(unique_songs), 3)

    @patch("firebase_uploader.db.reference")
    def test_update_database(self, mock_db_reference):
        mock_ref = MagicMock()
        mock_db_reference.return_value = mock_ref
        unique_songs = [{"title": "Song 1"}, {"title": "Song 2"}]

        firebase_uploader.update_database(mock_ref, mock_ref, unique_songs)
        mock_ref.set.assert_called()


if __name__ == "__main__":
    unittest.main()
