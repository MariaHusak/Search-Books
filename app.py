from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector


app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'books',
}

def create_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('books1.html')



@app.route('/process_input', methods=['POST'])
def process_input():
    connection = create_connection()
    cursor = connection.cursor()

    book_name = request.form['book_name']
    author_name = request.form['author_name']
    genre = request.form['genre']
    gender_author = request.form['gender_author']
    year_of_writing = request.form['year_of_writing']
    cover_color = request.form['cover_color']
    nationality = request.form['nationality']


    cursor.execute("SELECT booksbase.book_id FROM booksbase "
                   "JOIN details ON booksbase.book_id = details.details_id "
                   "WHERE booksbase.book_name = %s OR booksbase.author_name = %s OR details.genre = %s"
                   " OR details.gender_author = %s OR details.year_of_writing = %s"
                   " OR details.cover_color = %s OR details.nationality = %s",
                   (book_name, author_name, genre, gender_author, year_of_writing, cover_color, nationality))

    book_id = cursor.fetchone()


    return redirect(url_for('result',  book_id=book_id[0]))


@app.route('/books2/<int:book_id>')
def result(book_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT image_PathName, book_name, author_name FROM booksbase WHERE book_id = %s", (book_id,))
    result_data = cursor.fetchone()
    author_name = result_data[2]
    cursor.execute("SELECT author_name, book_name, image_PathName FROM booksbase WHERE author_name = %s",
                   (author_name,))
    all_books_by_author = cursor.fetchall()

#genre

    cursor.execute("SELECT genre FROM details WHERE details_id = %s", (book_id,))
    result_data1 = cursor.fetchone()
    genre = result_data1[0]

    cursor.execute("SELECT booksbase.book_id FROM booksbase "
                   "JOIN details ON booksbase.book_id = details.details_id "
                   "WHERE details.genre = %s",
                   (genre,))
    books_with_same_genre = cursor.fetchall()

    all_books_by_genre = []
    for book_with_same_genre in books_with_same_genre:
        cursor.execute("SELECT author_name, book_name, image_PathName FROM booksbase WHERE book_id = %s",
                       (book_with_same_genre[0],))
        book_data = cursor.fetchone()
        all_books_by_genre.append(book_data)

#gender_author

    cursor.execute("SELECT gender_author FROM details WHERE details_id = %s", (book_id,))
    result_data1 = cursor.fetchone()
    gender_author = result_data1[0]

    cursor.execute("SELECT booksbase.book_id FROM booksbase "
                   "JOIN details ON booksbase.book_id = details.details_id "
                   "WHERE details.gender_author = %s",
                   (gender_author,))
    books_with_same_gender_author = cursor.fetchall()

    all_books_by_gender_author = []
    for book_with_same_gender_author in books_with_same_gender_author:
        cursor.execute("SELECT author_name, book_name, image_PathName FROM booksbase WHERE book_id = %s",
                       (book_with_same_gender_author[0],))
        book_data = cursor.fetchone()
        all_books_by_gender_author.append(book_data)

#year_of_writing

    cursor.execute("SELECT year_of_writing FROM details WHERE details_id = %s", (book_id,))
    result_data1 = cursor.fetchone()
    year_of_writing = result_data1[0]

    cursor.execute("SELECT booksbase.book_id FROM booksbase "
                   "JOIN details ON booksbase.book_id = details.details_id "
                   "WHERE details.year_of_writing = %s",
                   (year_of_writing,))
    books_with_same_year_of_writing = cursor.fetchall()

    all_books_by_year_of_writing = []
    for book_with_same_year_of_writing in books_with_same_year_of_writing:
        cursor.execute("SELECT author_name, book_name, image_PathName FROM booksbase WHERE book_id = %s",
                       (book_with_same_year_of_writing[0],))
        book_data = cursor.fetchone()
        all_books_by_year_of_writing.append(book_data)

#cover_color

    cursor.execute("SELECT cover_color FROM details WHERE details_id = %s", (book_id,))
    result_data1 = cursor.fetchone()
    cover_color = result_data1[0]

    cursor.execute("SELECT booksbase.book_id FROM booksbase "
                   "JOIN details ON booksbase.book_id = details.details_id "
                   "WHERE details.cover_color = %s",
                   (cover_color,))
    books_with_same_cover_color = cursor.fetchall()

    all_books_by_cover_color = []
    for book_with_same_cover_color in books_with_same_cover_color:
        cursor.execute("SELECT author_name, book_name, image_PathName FROM booksbase WHERE book_id = %s",
                       (book_with_same_cover_color[0],))
        book_data = cursor.fetchone()
        all_books_by_cover_color.append(book_data)

#nationality

    cursor.execute("SELECT nationality FROM details WHERE details_id = %s", (book_id,))
    result_data1 = cursor.fetchone()
    nationality = result_data1[0]

    cursor.execute("SELECT booksbase.book_id FROM booksbase "
                   "JOIN details ON booksbase.book_id = details.details_id "
                   "WHERE details.nationality = %s",
                   (nationality,))
    books_with_same_nationality = cursor.fetchall()

    all_books_by_nationality = []
    for book_with_same_nationality in books_with_same_nationality:
        cursor.execute("SELECT author_name, book_name, image_PathName FROM booksbase WHERE book_id = %s",
                       (book_with_same_nationality[0],))
        book_data = cursor.fetchone()
        all_books_by_nationality.append(book_data)

    connection.close()
    if len(all_books_by_author) > 1:
        return render_template('books2.html', books=all_books_by_author)
    elif len(all_books_by_genre) > 1:
        return render_template('books2.html', books=all_books_by_genre)
    elif len(all_books_by_gender_author) > 1:
        return render_template('books2.html', books=all_books_by_gender_author)
    elif len(all_books_by_year_of_writing) > 1:
        return render_template('books2.html', books=all_books_by_year_of_writing)
    elif len(all_books_by_cover_color) > 1:
        return render_template('books2.html', books=all_books_by_cover_color)
    elif len(all_books_by_nationality) > 1:
        return render_template('books2.html', books=all_books_by_nationality)
    else:
        return render_template('books2.html', book=result_data)



@app.route('/save_book', methods=['POST'])
def save_book():
    connection = create_connection()
    cursor = connection.cursor()

    print(request.form)

    author_name = request.form['author_name']

    cursor.execute("SELECT book_id FROM booksbase WHERE author_name = %s", (author_name,))
    result_data = cursor.fetchone()
    existing_book_id = result_data[0]

    if existing_book_id:
        cursor.execute("UPDATE options SET saved = '1' WHERE options_id = %s", (existing_book_id,))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    else:
        return jsonify({'status': 'error', 'message': f'Book with author {author_name} not found'})

@app.route('/del_save_book', methods=['POST'])
def del_save_book():
    connection = create_connection()
    cursor = connection.cursor()

    print(request.form)

    author_name = request.form['author_name']

    cursor.execute("SELECT book_id FROM booksbase WHERE author_name = %s", (author_name,))
    result_data = cursor.fetchone()
    existing_book_id = result_data[0]

    if existing_book_id:
        cursor.execute("UPDATE options SET saved = '0' WHERE options_id = %s", (existing_book_id,))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    else:
        return jsonify({'status': 'error', 'message': f'Book with author {author_name} not found'})

@app.route('/favorite_book', methods=['POST'])
def favorite_book():
    connection = create_connection()
    cursor = connection.cursor()

    print(request.form)

    author_name = request.form['author_name']

    cursor.execute("SELECT book_id FROM booksbase WHERE author_name = %s", (author_name,))
    result_data = cursor.fetchone()
    existing_book_id = result_data[0]

    if existing_book_id:
        cursor.execute("UPDATE options SET favorite = '1' WHERE options_id = %s", (existing_book_id,))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    else:
        return jsonify({'status': 'error', 'message': f'Book with author {author_name} not found'})

@app.route('/del_favorite_book', methods=['POST'])
def del_favorite_book():
    connection = create_connection()
    cursor = connection.cursor()

    print(request.form)

    author_name = request.form['author_name']

    cursor.execute("SELECT book_id FROM booksbase WHERE author_name = %s", (author_name,))
    result_data = cursor.fetchone()
    existing_book_id = result_data[0]

    if existing_book_id:
        cursor.execute("DELETE FROM options WHERE options_id = %s", (existing_book_id,))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    else:
        return jsonify({'status': 'error', 'message': f'Book with author {author_name} not found'})


@app.route('/saved')
def saved():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT options_id FROM options WHERE saved = 1")
    options_id = cursor.fetchall()

    all_books = []
    for options_id in options_id:
        cursor.execute("SELECT author_name, book_name, image_PathName FROM booksbase WHERE book_id = %s",
                       (options_id[0],))
        book_data = cursor.fetchone()
        all_books.append(book_data)

    return render_template('books3.html', books=all_books)



@app.route('/popular')
def popular():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT options_id FROM options WHERE popular = 1")
    options_id = cursor.fetchall()

    all_books = []
    for options_id in options_id:
        cursor.execute("SELECT author_name, book_name, image_PathName FROM booksbase WHERE book_id = %s",
                       (options_id[0],))
        book_data = cursor.fetchone()
        all_books.append(book_data)

    return render_template('books4.html', books=all_books)

@app.route('/favorite')
def favorite():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT options_id FROM options WHERE favorite = 1")
    options_id = cursor.fetchall()

    all_books = []
    for options_id in options_id:
        cursor.execute("SELECT author_name, book_name, image_PathName FROM booksbase WHERE book_id = %s",
                       (options_id[0],))
        book_data = cursor.fetchone()
        all_books.append(book_data)

    return render_template('books5.html', books=all_books)



if __name__ == '__main__':
    app.run(debug=True)
