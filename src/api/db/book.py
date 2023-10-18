from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from db.database import Base

# Declare Classes / Tables
book_authors = Table('book_authors', Base.metadata,
                     Column('id', Integer, primary_key=True, nullable=False),
                     Column('book_id', ForeignKey('books.id'), index=True),
                     Column('author_id', ForeignKey('authors.id'), index=True)
                     )


class Book(Base):   
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    page_numbers = Column(Integer, nullable=False)
    year_published = Column(Integer, nullable=True)
    url = Column(String, nullable=True)

    # Define a many-to-Many relationship between Book and Author
    authors = relationship(
        "Author", secondary="book_authors", back_populates='books')

    def __repr__(self):
        return f"Book(name={self.name}, pages={self.page_numbers})"
