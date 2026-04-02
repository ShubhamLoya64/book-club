"""
Seed data for the BookClub API.

Populates the database with ~50 books, 5 users, reviews, and reading lists.
"""

import datetime

from sqlalchemy.orm import Session

from bookclub.models import Book, ReadingList, ReadingListItem, Review, User


def seed_database(db: Session):
    """Populate the database with sample data."""
    users = _seed_users(db)
    books = _seed_books(db)
    _seed_reviews(db, users, books)
    _seed_reading_lists(db, users, books)
    db.commit()


def _seed_users(db: Session) -> list[User]:
    users_data = [
        {"username": "sarah_dev", "email": "sarah@example.com", "display_name": "Sarah Chen"},
        {"username": "marcus_r", "email": "marcus@example.com", "display_name": "Marcus Rivera"},
        {"username": "priya_k", "email": "priya@example.com", "display_name": "Priya Kapoor"},
        {"username": "alex_j", "email": "alex@example.com", "display_name": "Alex Johnson"},
        {"username": "emma_w", "email": "emma@example.com", "display_name": "Emma Williams"},
    ]
    users = []
    for data in users_data:
        user = User(**data)
        db.add(user)
        users.append(user)
    db.flush()
    return users


def _seed_books(db: Session) -> list[Book]:
    books_data = [
        # --- Stephen King books (designed to trigger search bug with query "king") ---
        {
            "title": "The Shining",
            "author": "Stephen King",
            "description": "A family heads to an isolated hotel where a sinister presence influences the father. A masterwork by King.",
            "published_date": "1977-01-28",
            "isbn": "9780385121675",
            "page_count": 447,
        },
        {
            "title": "It",
            "author": "Stephen King",
            "description": "A group of children confront a shapeshifting monster. King's epic tale of childhood fear.",
            "published_date": "1986-09-15",
            "isbn": "9780670813025",
            "page_count": 1138,
        },
        {
            "title": "The Stand",
            "author": "Stephen King",
            "description": "A post-apocalyptic vision of a world decimated by plague. King at his most ambitious.",
            "published_date": "1978-10-03",
            "isbn": "9780385121682",
            "page_count": 823,
        },
        {
            "title": "Misery",
            "author": "Stephen King",
            "description": "A famous novelist is held captive by his self-proclaimed number one fan.",
            "published_date": "1987-06-08",
            "isbn": "9780670813643",
            "page_count": 310,
        },
        {
            "title": "The Dark Tower: The Gunslinger",
            "author": "Stephen King",
            "description": "The first book in King's magnum opus Dark Tower series.",
            "published_date": "1982-06-10",
            "isbn": "9780937986509",
            "page_count": 224,
        },
        # --- Classic fiction ---
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "description": "A young girl in the American South witnesses racial injustice and learns about compassion.",
            "published_date": "1960-07-11",
            "isbn": "9780061120084",
            "page_count": 281,
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "description": "A dystopian masterpiece about totalitarianism, surveillance, and the power of language.",
            "published_date": "1949-06-08",
            "isbn": "9780451524935",
            "page_count": 328,
        },
        {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "description": "A witty exploration of manners, morality, and marriage in Regency-era England.",
            "published_date": "1813-01-28",
            "isbn": "9780141439518",
            "page_count": 432,
        },
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "description": "A portrait of the Jazz Age and the American dream through the eyes of Nick Carraway.",
            "published_date": "1925-04-10",
            "isbn": "9780743273565",
            "page_count": 180,
        },
        {
            "title": "One Hundred Years of Solitude",
            "author": "Gabriel García Márquez",
            "description": "The multi-generational story of the Buendía family in the fictional town of Macondo.",
            "published_date": "1967-05-30",
            "isbn": "9780060883287",
            "page_count": 417,
        },
        # --- Science fiction ---
        {
            "title": "Dune",
            "author": "Frank Herbert",
            "description": "An epic tale of politics, religion, and ecology on the desert planet Arrakis.",
            "published_date": "1965-08-01",
            "isbn": "9780441172719",
            "page_count": 688,
        },
        {
            "title": "Neuromancer",
            "author": "William Gibson",
            "description": "The seminal cyberpunk novel about a washed-up hacker hired for one last job.",
            "published_date": "1984-07-01",
            "isbn": "9780441569595",
            "page_count": 271,
        },
        {
            "title": "The Left Hand of Darkness",
            "author": "Ursula K. Le Guin",
            "description": "An envoy visits a world where people have no fixed gender. Explores society and identity.",
            "published_date": "1969-03-01",
            "isbn": "9780441478125",
            "page_count": 286,
        },
        {
            "title": "Foundation",
            "author": "Isaac Asimov",
            "description": "A mathematician predicts the fall of a galactic empire and creates a plan to shorten the coming dark age.",
            "published_date": "1951-06-01",
            "isbn": "9780553293357",
            "page_count": 244,
        },
        {
            "title": "Snow Crash",
            "author": "Neal Stephenson",
            "description": "A pizza delivery driver and hacker uncovers a conspiracy in a fragmented future America.",
            "published_date": "1992-06-01",
            "isbn": "9780553380958",
            "page_count": 440,
        },
        # --- Non-fiction ---
        {
            "title": "Sapiens: A Brief History of Humankind",
            "author": "Yuval Noah Harari",
            "description": "A sweeping history of the human species from the Stone Age to the present.",
            "published_date": "2011-01-01",
            "isbn": "9780062316097",
            "page_count": 443,
        },
        {
            "title": "Thinking, Fast and Slow",
            "author": "Daniel Kahneman",
            "description": "A Nobel laureate explores the two systems that drive the way we think.",
            "published_date": "2011-10-25",
            "isbn": "9780374533557",
            "page_count": 499,
        },
        {
            "title": "The Design of Everyday Things",
            "author": "Don Norman",
            "description": "A foundational text on human-centered design and usability.",
            "published_date": "1988-01-01",
            "isbn": "9780465050659",
            "page_count": 368,
        },
        {
            "title": "Educated",
            "author": "Tara Westover",
            "description": "A memoir about growing up in a survivalist family and the transformative power of education.",
            "published_date": "2018-02-20",
            "isbn": "9780399590504",
            "page_count": 334,
        },
        {
            "title": "The Immortal Life of Henrietta Lacks",
            "author": "Rebecca Skloot",
            "description": "The story of the woman whose cells were taken without her knowledge and became vital to medical research.",
            "published_date": "2010-02-02",
            "isbn": "9781400052189",
            "page_count": 381,
        },
        # --- Fantasy ---
        {
            "title": "The Name of the Wind",
            "author": "Patrick Rothfuss",
            "description": "A young man tells the story of his life, from orphan to legendary figure, in this lyrical fantasy.",
            "published_date": "2007-03-27",
            "isbn": "9780756404741",
            "page_count": 662,
        },
        {
            "title": "A Game of Thrones",
            "author": "George R.R. Martin",
            "description": "Noble families vie for control of the Iron Throne in this epic fantasy of politics and war.",
            "published_date": "1996-08-01",
            "isbn": "9780553103540",
            "page_count": 694,
        },
        {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "description": "A hobbit is swept into an adventure with dwarves seeking to reclaim their mountain kingdom.",
            "published_date": "1937-09-21",
            "isbn": "9780547928227",
            "page_count": 300,
        },
        {
            "title": "American Gods",
            "author": "Neil Gaiman",
            "description": "Old gods brought to America by immigrants battle new gods of technology and media.",
            "published_date": "2001-06-19",
            "isbn": "9780063081918",
            "page_count": 465,
        },
        {
            "title": "The Fifth Season",
            "author": "N.K. Jemisin",
            "description": "On a continent plagued by catastrophic seismic events, a woman searches for her kidnapped daughter.",
            "published_date": "2015-08-04",
            "isbn": "9780316229296",
            "page_count": 468,
        },
        # --- Mystery / Thriller ---
        {
            "title": "The Girl with the Dragon Tattoo",
            "author": "Stieg Larsson",
            "description": "A journalist and a brilliant hacker investigate a decades-old disappearance.",
            "published_date": "2005-08-01",
            "isbn": "9780307454546",
            "page_count": 465,
        },
        {
            "title": "Gone Girl",
            "author": "Gillian Flynn",
            "description": "A wife disappears on her fifth wedding anniversary, and suspicion falls on her husband.",
            "published_date": "2012-06-05",
            "isbn": "9780307588364",
            "page_count": 415,
        },
        {
            "title": "The Da Vinci Code",
            "author": "Dan Brown",
            "description": "A symbologist uncovers a conspiracy hidden in the works of Leonardo da Vinci.",
            "published_date": "2003-03-18",
            "isbn": "9780307474278",
            "page_count": 489,
        },
        {
            "title": "Big Little Lies",
            "author": "Liane Moriarty",
            "description": "Three women's lives unravel to a shocking climax at a school trivia night.",
            "published_date": "2014-07-29",
            "isbn": "9780399167065",
            "page_count": 460,
        },
        {
            "title": "In the Woods",
            "author": "Tana French",
            "description": "A detective investigates a murder in the Dublin suburb where he experienced a childhood trauma.",
            "published_date": "2007-05-17",
            "isbn": "9780143113492",
            "page_count": 429,
        },
        # --- Literary fiction ---
        {
            "title": "The Kite Runner",
            "author": "Khaled Hosseini",
            "description": "A story of friendship, betrayal, and redemption set against the backdrop of Afghanistan's turmoil.",
            "published_date": "2003-05-29",
            "isbn": "9781594631931",
            "page_count": 371,
        },
        {
            "title": "Normal People",
            "author": "Sally Rooney",
            "description": "Two Irish teenagers navigate a complicated relationship from school through university.",
            "published_date": "2018-08-28",
            "isbn": "9781984822178",
            "page_count": 273,
        },
        {
            "title": "The Road",
            "author": "Cormac McCarthy",
            "description": "A father and son journey through a post-apocalyptic landscape, clinging to hope.",
            "published_date": "2006-09-26",
            "isbn": "9780307387899",
            "page_count": 287,
        },
        {
            "title": "Beloved",
            "author": "Toni Morrison",
            "description": "A former slave is haunted by the ghost of her dead daughter in this Pulitzer-winning novel.",
            "published_date": "1987-09-02",
            "isbn": "9781400033416",
            "page_count": 324,
        },
        {
            "title": "The Remains of the Day",
            "author": "Kazuo Ishiguro",
            "description": "An English butler reflects on his life of service and the choices he failed to make.",
            "published_date": "1989-05-01",
            "isbn": "9780679731726",
            "page_count": 245,
        },
        # --- Tech / Programming ---
        {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "description": "A handbook of agile software craftsmanship with practical advice on writing readable code.",
            "published_date": "2008-08-01",
            "isbn": "9780132350884",
            "page_count": 464,
        },
        {
            "title": "The Pragmatic Programmer",
            "author": "David Thomas and Andrew Hunt",
            "description": "Tips and techniques for modern software development, from career advice to coding practices.",
            "published_date": "1999-10-20",
            "isbn": "9780135957059",
            "page_count": 352,
        },
        {
            "title": "Designing Data-Intensive Applications",
            "author": "Martin Kleppmann",
            "description": "A guide to the principles and practicalities of data systems, from databases to stream processing.",
            "published_date": "2017-03-16",
            "isbn": "9781449373320",
            "page_count": 616,
        },
        {
            "title": "Refactoring",
            "author": "Martin Fowler",
            "description": "Improving the design of existing code through systematic refactoring techniques.",
            "published_date": "1999-07-08",
            "isbn": "9780201485677",
            "page_count": 431,
        },
        {
            "title": "The Mythical Man-Month",
            "author": "Frederick P. Brooks Jr.",
            "description": "Classic essays on software engineering and project management. 'Adding manpower to a late project makes it later.'",
            "published_date": "1975-01-01",
            "isbn": "9780201835953",
            "page_count": 322,
        },
        # --- More books to hit ~50 ---
        {
            "title": "Circe",
            "author": "Madeline Miller",
            "description": "The story of the mythological witch Circe, from outcast to powerful goddess.",
            "published_date": "2018-04-10",
            "isbn": "9780316556347",
            "page_count": 393,
        },
        {
            "title": "Project Hail Mary",
            "author": "Andy Weir",
            "description": "A lone astronaut must save Earth from an extinction-level threat. From the author of The Martian.",
            "published_date": "2021-05-04",
            "isbn": "9780593135204",
            "page_count": 476,
        },
        {
            "title": "Klara and the Sun",
            "author": "Kazuo Ishiguro",
            "description": "An Artificial Friend observes the human world while waiting to be chosen by a customer.",
            "published_date": "2021-03-02",
            "isbn": "9780571364886",
            "page_count": 307,
        },
        {
            "title": "The Midnight Library",
            "author": "Matt Haig",
            "description": "A woman finds a library between life and death where each book represents a life she could have lived.",
            "published_date": "2020-08-13",
            "isbn": "9780525559474",
            "page_count": 288,
        },
        {
            "title": "Atomic Habits",
            "author": "James Clear",
            "description": "A practical guide to building good habits and breaking bad ones through tiny changes.",
            "published_date": "2018-10-16",
            "isbn": "9780735211292",
            "page_count": 320,
        },
        {
            "title": "The Song of Achilles",
            "author": "Madeline Miller",
            "description": "A retelling of the Iliad from the perspective of Patroclus, Achilles' companion.",
            "published_date": "2012-03-06",
            "isbn": "9780062060624",
            "page_count": 378,
        },
        {
            "title": "Piranesi",
            "author": "Susanna Clarke",
            "description": "A man lives in a mysterious house of infinite halls, filled with statues and an ocean.",
            "published_date": "2020-09-15",
            "isbn": "9781635575941",
            "page_count": 272,
        },
        {
            "title": "The Vanishing Half",
            "author": "Brit Bennett",
            "description": "Twin sisters who grew up in a small Black community choose very different paths in life.",
            "published_date": "2020-06-02",
            "isbn": "9780525536291",
            "page_count": 343,
        },
        {
            "title": "Kindred",
            "author": "Octavia E. Butler",
            "description": "A modern Black woman is repeatedly pulled back in time to the antebellum South.",
            "published_date": "1979-06-01",
            "isbn": "9780807083697",
            "page_count": 264,
        },
        {
            "title": "The Three-Body Problem",
            "author": "Liu Cixin",
            "description": "A secret military project sends signals into space, making first contact with an alien civilization.",
            "published_date": "2008-01-01",
            "isbn": "9780765382030",
            "page_count": 400,
        },
    ]

    books = []
    for data in books_data:
        book = Book(**data)
        db.add(book)
        books.append(book)
    db.flush()
    return books


def _seed_reviews(db: Session, users: list[User], books: list[Book]):
    """Create some reviews. Deliberately varied ratings."""
    reviews_data = [
        # Sarah reviews sci-fi
        (0, 10, 5, "Dune is a masterpiece of world-building. Herbert creates a fully realized universe."),
        (0, 11, 4, "Neuromancer defined cyberpunk. Dense prose but rewarding."),
        (0, 13, 5, "Foundation is Asimov at his best. The scope is incredible."),
        (0, 49, 4, "The Three-Body Problem is mind-bending hard sci-fi. Dense but worth it."),
        # Marcus reviews thrillers
        (1, 25, 4, "Girl with the Dragon Tattoo is gripping. Larsson builds tension masterfully."),
        (1, 26, 3, "Gone Girl is twisty but the ending felt rushed."),
        (1, 27, 2, "The Da Vinci Code is fun but the prose is clunky."),
        # Priya reviews literary fiction
        (2, 5, 5, "To Kill a Mockingbird is essential reading. Timeless themes."),
        (2, 30, 5, "The Kite Runner destroyed me. Beautiful and devastating."),
        (2, 31, 4, "Normal People captures the complexity of young relationships perfectly."),
        (2, 33, 5, "Beloved is the most powerful novel I've ever read."),
        # Alex reviews tech books
        (3, 35, 4, "Clean Code has good advice but can be dogmatic. Still worth reading."),
        (3, 36, 5, "The Pragmatic Programmer should be required reading for all developers."),
        (3, 37, 5, "DDIA is the best technical book I've read. Incredibly thorough."),
        (3, 39, 3, "Mythical Man-Month is dated but the core insights still hold."),
        # Emma reviews fantasy
        (4, 20, 5, "Name of the Wind is beautifully written. Rothfuss is a poet."),
        (4, 22, 5, "The Hobbit is pure charm. Tolkien's most accessible work."),
        (4, 23, 4, "American Gods is ambitious. Gaiman at his most expansive."),
        (4, 24, 5, "The Fifth Season broke every rule and it works brilliantly."),
        # Cross-genre reviews for variety
        (0, 0, 5, "The Shining is terrifying. King builds dread unlike anyone else."),
        (1, 6, 4, "1984 is chillingly relevant. Orwell was prophetic."),
        (2, 40, 5, "Circe is gorgeous. Miller breathes life into ancient myth."),
        (3, 41, 5, "Project Hail Mary is pure fun. Weir's best since The Martian."),
        (4, 43, 4, "The Midnight Library is a comforting hug of a book."),
    ]

    for user_idx, book_idx, rating, text in reviews_data:
        review = Review(
            user_id=users[user_idx].id,
            book_id=books[book_idx].id,
            rating=rating,
            text=text,
        )
        db.add(review)
    db.flush()

    # Update average ratings for reviewed books
    reviewed_book_indices = set(r[1] for r in reviews_data)
    for idx in reviewed_book_indices:
        book = books[idx]
        book_reviews = [r for r in reviews_data if r[1] == idx]
        book.average_rating = sum(r[2] for r in book_reviews) / len(book_reviews)
        book.rating_count = len(book_reviews)


def _seed_reading_lists(db: Session, users: list[User], books: list[Book]):
    """Create reading lists with items."""
    lists_data = [
        {
            "user_idx": 0,
            "name": "Sci-Fi Classics",
            "description": "The best science fiction ever written",
            "items": [(10, "read"), (11, "read"), (12, "reading"), (13, "read"), (14, "unread")],
        },
        {
            "user_idx": 0,
            "name": "To Read This Year",
            "description": "My 2026 reading goals",
            "items": [(43, "unread"), (41, "unread"), (46, "unread"), (24, "reading")],
        },
        {
            "user_idx": 1,
            "name": "Thriller Marathon",
            "description": None,
            "items": [(25, "read"), (26, "read"), (27, "reading"), (28, "unread"), (29, "unread")],
        },
        {
            "user_idx": 2,
            "name": "Book Club Picks",
            "description": "Books for our monthly meetings",
            "items": [(5, "read"), (30, "read"), (33, "reading"), (40, "unread")],
        },
        {
            "user_idx": 3,
            "name": "Dev Required Reading",
            "description": "Every engineer should read these",
            "items": [(35, "read"), (36, "read"), (37, "reading"), (38, "unread"), (39, "unread")],
        },
        {
            "user_idx": 4,
            "name": "Fantasy Favorites",
            "description": "The best fantasy I've read",
            "items": [(20, "read"), (21, "read"), (22, "read"), (23, "read"), (24, "read")],
        },
    ]

    for data in lists_data:
        reading_list = ReadingList(
            user_id=users[data["user_idx"]].id,
            name=data["name"],
            description=data["description"],
        )
        db.add(reading_list)
        db.flush()

        for book_idx, status in data["items"]:
            item = ReadingListItem(
                reading_list_id=reading_list.id,
                book_id=books[book_idx].id,
                status=status,
            )
            db.add(item)
    db.flush()
