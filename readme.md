# How to Guide

### The backend expects an postgres db

- with a database named **library**
- username - postgres
- password - p@ssword

### Dummy Data Generation

- There are is dummy_data creator script include at the `src/api/db/dummy_data.py` location.
- to generate the dummy data uncomment the last line from the `[main.py](http://main.py)` file in `src/api` directory
- don’t forget to uncomment the line back ‼️

### Users :

After creating the dummy data 

You can use the following credentials

username - **admin**

password  - **p@ssword**

### Some Assumptions on the system

1. A book can have more than 1 Authors (book ↔ authors is a many to many relationship)
2. We can have an Author without any Book.
3. A book will always have at-least one writer.
4. There are two types of user **admin and non-admin**
    1. Idea was to have a set of users capable to invite other users to the platform
5. I have added couple of extra fields in both the Book and Author Schema (Just for Asthetics.)
    1. Book - (year_published, description, url)
    2. Author - (description, Age)

### Supported Operations :

**Books :**

1. Add a new book
2. View all the books
3. Search for any book by name
4. Update a book.
5. Delete a book.

**Author :**

1. Add a new author
2. View all the authors
3. Search for any author by name
4. update an Author
5. Delete an Author