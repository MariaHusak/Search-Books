import unittest
from app import *
from unittest.mock import patch, MagicMock

class TestCreateConnection(unittest.TestCase):
    @patch('app.mysql.connector.connect')
    def test_create_connection(self, mock_connect):
        create_connection()
        mock_connect.assert_called_once_with(**db_config)


class TestIndexRoute(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)


class TestProcessInput(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.create_connection')
    def test_process_input_success(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]

        response = self.app.post('/process_input', data={
            'book_name': 'Test Book',
            'author_name': 'Test Author',
            'genre': 'Fiction',
            'gender_author': 'Male',
            'year_of_writing': '2020',
            'cover_color': 'Red',
            'nationality': 'American'
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn('/books2/1', response.location)

    @patch('app.create_connection')
    def test_process_input_no_book_found(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        response = self.app.post('/process_input', data={
            'book_name': 'Nonexistent Book',
            'author_name': 'Unknown Author',
            'genre': 'Unknown',
            'gender_author': 'Unknown',
            'year_of_writing': 'Unknown',
            'cover_color': 'Unknown',
            'nationality': 'Unknown'
        })

        self.assertEqual(response.status_code, 500)


class TestSaveBook(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.create_connection')
    def test_save_book_success(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]

        response = self.app.post('/save_book', data={'author_name': 'Test Author'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.location)

    @patch('app.create_connection')
    def test_save_book_not_found(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        response = self.app.post('/save_book', data={'author_name': 'Unknown Author'})
        self.assertEqual(response.status_code, 500)


class TestFavoriteBook(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.create_connection')
    def test_favorite_book_success(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]

        response = self.app.post('/favorite_book', data={'author_name': 'Test Author'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.location)

    @patch('app.create_connection')
    def test_favorite_book_not_found(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        response = self.app.post('/favorite_book', data={'author_name': 'Unknown Author'})
        self.assertEqual(response.status_code, 500)


class TestDelSaveBook(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.create_connection')
    def test_del_save_book_success(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]

        response = self.app.post('/del_save_book', data={'author_name': 'Test Author'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.location)

    @patch('app.create_connection')
    def test_del_save_book_not_found(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        response = self.app.post('/del_save_book', data={'author_name': 'Unknown Author'})
        self.assertEqual(response.status_code, 500)


class TestDelFavoriteBook(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.create_connection')
    def test_del_favorite_book_success(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]

        response = self.app.post('/del_favorite_book', data={'author_name': 'Test Author'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.location)

    @patch('app.create_connection')
    def test_del_favorite_book_not_found(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        response = self.app.post('/del_favorite_book', data={'author_name': 'Unknown Author'})
        self.assertEqual(response.status_code, 500)


class TestPopularRoute(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.create_connection')
    def test_popular_books_found(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [
            [(1,), (2,)],
            [('Author 1', 'Book 1', 'path/to/image1')],
            [('Author 2', 'Book 2', 'path/to/image2')]
        ]

        response = self.app.get('/popular')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
