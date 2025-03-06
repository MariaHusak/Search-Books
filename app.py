from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from constants import DB_CONFIG, fields

app = Flask(__name__)


def create_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_db_cursor():
    connection = create_connection()
    cursor = connection.cursor()
    return connection, cursor


def get_form_data(fields=fields):
    return {field: request.form[field] for field in fields}


def fetch_book_id(cursor, form_data):
    query = """
        SELECT booksbase.book_id FROM booksbase
        JOIN details ON booksbase.book_id = details.details_id
        WHERE booksbase.book_name = %s OR booksbase.author_name = %s
        OR details.genre = %s OR details.gender_author = %s
        OR details.year_of_writing = %s OR details.cover_color = %s
        OR details.nationality = %s
    """
    cursor.execute(query, tuple(form_data.values()))
    return cursor.fetchone()


@app.route('/')
def index():
    return render_template('books1.html')


@app.route('/process_input', methods=['POST'])
def process_input():
    connection, cursor = get_db_cursor()
    form_data = get_form_data()
    book_id = fetch_book_id(cursor, form_data)
    connection.close()
    if book_id is None:
        return "Book not found", 404
    return redirect(url_for('result', book_id=book_id[0]))


def fetch_attribute_value(cursor, book_id, attribute):
    cursor.execute(f"SELECT {attribute} FROM details WHERE details_id = %s", (book_id,))
    return cursor.fetchone()[0]


def fetch_books_by_attribute(cursor, attribute, value):
    cursor.execute(f"""
        SELECT booksbase.book_id FROM booksbase
        JOIN details ON booksbase.book_id = details.details_id
        WHERE details.{attribute} = %s
    """, (value,))
    book_ids = cursor.fetchall()
    all_books = []
    for book_id in book_ids:
        cursor.execute(
            "SELECT author_name, book_name, image_PathName FROM booksbase WHERE book_id = %s",
            (book_id[0],)
        )
        all_books.append(cursor.fetchone())
    return all_books


def fetch_main_book_details(cursor, book_id):
    cursor.execute(
        "SELECT image_PathName, book_name, author_name FROM booksbase WHERE book_id = %s",
        (book_id,)
    )
    return cursor.fetchone()


def fetch_books_by_author(cursor, author_name):
    cursor.execute(
        "SELECT author_name, book_name, image_PathName FROM booksbase WHERE author_name = %s",
        (author_name,)
    )
    return cursor.fetchall()


def render_books_template(result_data, **books_by_attributes):
    for book_list in books_by_attributes.values():
        if len(book_list) >= 1:
            return render_template('books2.html', books=book_list)
    return render_template('books2.html', book=result_data)


@app.route('/books2/<int:book_id>')
def result(book_id):
    connection, cursor = get_db_cursor()
    result_data = fetch_main_book_details(cursor, book_id)
    author_name = result_data[2]
    all_books_by_author = fetch_books_by_author(cursor, author_name)
    attributes = [
        'genre', 'gender_author', 'year_of_writing', 'cover_color', 'nationality'
    ]
    books_by_attributes = {
        attr: fetch_books_by_attribute(cursor, attr, fetch_attribute_value(cursor, book_id, attr))
        for attr in attributes
    }
    connection.close()
    return render_books_template(
        result_data, all_books_by_author=all_books_by_author, **books_by_attributes
    )

def update_book_status(cursor, author_name, status_column, status_value):
    cursor.execute(
        "SELECT book_id FROM booksbase WHERE author_name = %s", (author_name,)
    )
    result_data = cursor.fetchone()
    if result_data:
        cursor.execute(
            f"UPDATE options SET {status_column} = %s WHERE options_id = %s",
            (status_value, result_data[0])
        )
        return True
    return False

@app.route('/save_book', methods=['POST'])
def save_book():
    connection, cursor = get_db_cursor()
    if update_book_status(cursor, request.form['author_name'], 'saved', '1'):
        connection.commit()
    connection.close()
    return redirect(url_for('index'))

@app.route('/del_save_book', methods=['POST'])
def del_save_book():
    connection, cursor = get_db_cursor()
    if update_book_status(cursor, request.form['author_name'], 'saved', '0'):
        connection.commit()
    connection.close()
    return redirect(url_for('index'))

@app.route('/favorite_book', methods=['POST'])
def favorite_book():
    connection, cursor = get_db_cursor()
    if update_book_status(cursor, request.form['author_name'], 'favorite', '1'):
        connection.commit()
    connection.close()
    return redirect(url_for('index'))

@app.route('/del_favorite_book', methods=['POST'])
def del_favorite_book():
    connection, cursor = get_db_cursor()
    if update_book_status(cursor, request.form['author_name'], 'favorite', '0'):
        connection.commit()
    connection.close()
    return redirect(url_for('index'))

def fetch_books_by_option(cursor, option):
    cursor.execute(f"SELECT options_id FROM options WHERE {option} = 1")
    options_ids = cursor.fetchall()
    all_books = []
    for options_id in options_ids:
        cursor.execute(
            "SELECT author_name, book_name, image_PathName FROM booksbase WHERE book_id = %s",
            (options_id[0],)
        )
        all_books.append(cursor.fetchone())
    return all_books

@app.route('/saved')
def saved():
    connection, cursor = get_db_cursor()
    all_books = fetch_books_by_option(cursor, 'saved')
    connection.close()
    return render_template('books3.html', books=all_books)

@app.route('/popular')
def popular():
    connection, cursor = get_db_cursor()
    all_books = fetch_books_by_option(cursor, 'popular')
    connection.close()
    return render_template('books4.html', books=all_books)

@app.route('/favorite')
def favorite():
    connection, cursor = get_db_cursor()
    all_books = fetch_books_by_option(cursor, 'favorite')
    connection.close()
    return render_template('books5.html', books=all_books)

if __name__ == '__main__':
    app.run(debug=True)