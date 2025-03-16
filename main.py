import sqlite3
import streamlit as st

def create_database():
    conn = sqlite3.connect("text.db")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS text(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT NOT NULL,
                       author TEXT NOT NULL,
                       year INTEGER NOT NULL,
                       genre TEXT NOT NULL,
                       read_status BOOLEAN NOT NULL
                   )
                   """)
    conn.commit()
    conn.close()
    
def add_book():
    st.subheader("➕ Add a New Book")
    title = st.text_input("Enter the book title")
    author = st.text_input("Enter the book author")
    year = st.number_input("Enter the year", min_value=0, max_value=2100)
    genres = ["Fiction", "Non-fiction", "Science", "Religious", "Biography", "Fantasty", "Mystery", "Others"]
    genre = st.selectbox("Select the genre", genres)
    read_status = st.radio("Have you read this book?", ('Yes', 'No'))
    read_status = True if read_status == 'Yes' else False
    if st.button("➕ Add Book"):
        conn = sqlite3.connect("text.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO text(title, author, year, genre, read_status)
            VALUES(?, ?, ?, ?, ?)'''
            , (title, author, year, genre, read_status)
            )
        conn.commit()
        conn.close()
        st.success("✅ Book added successfully")
    
def remove_book():
    st.subheader("❌ Remove a Book")
    title = st.text_input("Enter the title of the book you want to remove")
    if st.button("🗑️ Remove Book"):
        conn = sqlite3.connect("text.db")
        cursor = conn.cursor()
        
        # Delete book (case insensitive)
        cursor.execute("DELETE FROM text WHERE LOWER(title) = LOWER(?)", (title,))
        conn.commit()

        # Check how many rows were deleted
        if cursor.rowcount > 0:
            st.success("✅ Book removed successfully")
        else:
            st.error("❌ Book not found")
        
        conn.close()

def search_book():
    st.subheader("🔎 Search for a Book")
    search_by = st.radio("Search by", ('Title', 'Author'))
    if search_by == 'Title':
        title = st.text_input("Enter book title")
        query = "SELECT * FROM text WHERE title = ?"
        params = (title,)
    else:
        author = st.text_input("Enter the author")
        query = "SELECT * FROM text WHERE author = ?"
        params = (author,)
    if st.button("🔎 Search"):
        conn = sqlite3.connect("text.db")
        cursor = conn.cursor()
        cursor.execute(query, params)
        matching_books = cursor.fetchall()
        if matching_books:
            st.write("Matching books:")
            for book in matching_books:
                status = "Read" if book[5] else "Unread"
                st.write(f"{book[1]} by {book[2]} ({book[3]} - {book[4]}) {status}")
        else:
            st.write("No matching book found")
        conn.close()
    
def display_all_books():
    st.subheader("📚Your Library")
    conn = sqlite3.connect("text.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM text")
    books = cursor.fetchall()
    if not books:
        st.write("Your library is empty")
    else:
        for book in books:
            status = "Read" if book[5] else "Unread"
            st.write(f"{book[1]} by {book[2]} ({book[3]} - {book[4]}) {status}")
    conn.close()
        
def display_statistics():
    st.subheader("📊Library Statistics")
    conn = sqlite3.connect("text.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM text")
    total_books = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM text WHERE read_status = 1")
    read_books = cursor.fetchone()[0]
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {percentage_read:.2f}%")
    conn.close()
    
def main():
    st.title("📚 Personal Library Manager🎉")
    menu = ["➕ Add a book", "❌ Remove a book", "🔎 Search a book", "📖 Display all books", "📊 Display statistics", "🚪 Exit"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    create_database()
    
    if choice == "➕ Add a book":
        add_book()
    elif choice == "❌ Remove a book":
        remove_book()
    elif choice == "🔎 Search a book":
        search_book()
    elif choice == "📖 Display all books":
        display_all_books()
    elif choice == "📊 Display statistics":
        display_statistics()
    elif choice == "🚪 Exit":
        st.write("Goodbye")
        st.stop()

if __name__ == "__main__":
    main()