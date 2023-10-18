# Insert data
import string
from lorem.text import TextLorem
import random
import lorem
from sqlalchemy.orm import Session
from db.user import USER_ROLE, User
from db.author import Author
from db.database import engine
from faker import Faker
from passlib.context import CryptContext

from db.book import Book

fake = Faker()

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

with Session(bind=engine) as session:

    books = [Book(name=fake.catch_phrase(), page_numbers=random.randint(100, 400), year_published=random.randint(
        1900, 2022), description=lorem.paragraph(), url="https://bit.ly/"+''.join(random.choices(string.ascii_lowercase +
                                                                                                 string.digits, k=5))) for _ in range(1000)]
    authors = [Author(name=fake.name(), age=random.randint(
        18, 65), description=lorem.paragraph()) for _ in range(100)]
    admin_user = User(email="admin@openbook.com",username="admin",
                      password=pwd_context.encrypt("p@ssword"), role=USER_ROLE.ADMIN.name)
    user = User(email="teddy@openbook.com",username='teddy',
                password=pwd_context.encrypt("p@ssword"), role=USER_ROLE.USER.name)

    for i, book in enumerate(books):
        if i % 3 == 0:
            book.authors = [authors[random.randint(0, 99)]]
        elif i % 3 == 1:
            book.authors = [authors[random.randint(
                0, 99)], authors[random.randint(0, 99)]]
        else:
            book.authors = [authors[random.randint(0, 99)], authors[random.randint(
                0, 99)], authors[random.randint(0, 99)]]
    session.add_all(authors)
    session.add_all(books)
    session.add_all([admin_user, user])
    session.commit()
