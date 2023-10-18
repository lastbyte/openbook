from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    description = Column(String, nullable=True)

    # Define a many-to-many relationship between Author and Book
    books = relationship("Book", secondary="book_authors", back_populates='authors')

    def __repr__(self):
        return f"Author(name={self.name})"
