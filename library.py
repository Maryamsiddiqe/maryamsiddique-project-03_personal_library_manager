import streamlit as st
import json

# File  library data store
LIBRARY_FILE = "library.txt"

# Function to load the library from a file
def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)  # Load JSON data from the file
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist

# Function to save the library to a file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file)  #  JSON  data

# Load  library data from the file
the_library = load_library()

# styling  app
st.markdown(
    """
    <style>
        body { background-color: #f5f5f5; }
        .stApp { background-color: #e3f2fd; }
        h1, h2, h3, h4 { color: #1976d2; }
        .stButton>button { background-color: #64b5f6; color: white; border-radius: 8px; }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #90caf9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }
        
    </style>
    """,
    unsafe_allow_html=True
)

# App title
st.title("📚 Personal Library Manager")

# Sidebar menu options
menu = ["Add Book", "Remove Book", "Search Book", "Library", "Statistics"]
choice = st.sidebar.selectbox("📌 Menu", menu)

#  genre options
genre_options = ["Fiction", "Non-Fiction", "Mystery", "Fantasy", "Science Fiction", "Biography", "History", "Romance", "Thriller", "Self-Help"]

# Adding a new book
if choice == "Add Book":
    st.subheader("📖 Add a New Book")
    title = st.text_input("📌 Enter Book Title")
    author = st.text_input("✍ Enter Author")
    year = st.number_input("📅 Enter Publication Year", min_value=1000, max_value=2025, step=1)
    genre = st.selectbox("📚 Select Genre", genre_options)
    read = st.checkbox("✅ Mark as Read")
    
    if st.button("➕ Add Book"):
        book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
        the_library.append(book)  # Add book to the list
        save_library(the_library)  
        st.success("🎉 Book added successfully!")

# Removing a book
elif choice == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    book_titles = [book["title"] for book in the_library]
    if book_titles:
        book_to_remove = st.selectbox("Select Book to Remove", book_titles)
        if st.button("❌ Remove Book"):
            the_library = [book for book in the_library if book["title"] != book_to_remove]  # Remove selected book
            save_library(the_library)
            st.success("📕 Book removed successfully!")
    else:
        st.warning("⚠️ No books available to remove.")

# Searching for a book
elif choice == "Search Book":
    st.subheader("🔎 Search for a Book")
    search_option = st.selectbox("Search by", ["Title", "Author", "Genre", "Year"])
    search_query = st.text_input(f"Enter {search_option}")
    
    if st.button("🔍 Search"):
        results = []
        if search_option == "Year":
            try:
                search_query = int(search_query)
                results = [book for book in the_library if book["year"] == search_query]
            except ValueError:
                st.warning("⚠️ Please enter a valid year.")
        else:
            results = [book for book in the_library if search_query.lower() in book[search_option.lower()].lower()]
        
        if results:
            for book in results:
                st.markdown(f"<p style='color:blue; font-size:16px;'><b>{book['title']}</b> by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}</p>", unsafe_allow_html=True)
        else:
            st.warning("❌ No matching books found!")

# Displaying all books in the library
elif choice == "Library":
    st.subheader("📚 Your Library")
    if the_library:
        for book in the_library:
            st.markdown(f"<p style='color:green; font-size:18px;'><b>{book['title']}</b> by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}</p>", unsafe_allow_html=True)
    else:
        st.info("📭 Your library is empty!")

#  statistics
elif choice == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(the_library)
    read_books = sum(1 for book in the_library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    
    st.write(f"📚 Total Books: {total_books}")
    st.write(f"📖 Books Read: {read_books} ({read_percentage:.2f}%)")
    
    if st.button("📕 Show Read Books"):
        read_books_list = [book for book in the_library if book["read"]]
        for book in read_books_list:
            st.write(f"📖 {book['title']} by {book['author']}")
    
    if st.button("📘 Show Unread Books"):
        unread_books_list = [book for book in the_library if not book["read"]]
        for book in unread_books_list:
            st.write(f"📖 {book['title']} by {book['author']}")

# Footer 
st.markdown(
    """
    <div class='footer'>
        <p style="text-align:center; font-size:20px; font-weight:bold;">Created by Maryam Siddique </p>
    </div>
    """,
    unsafe_allow_html=True
)
