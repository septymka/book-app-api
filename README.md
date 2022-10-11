
# Book-app

---


## REST API

---

### Books

#### Get a list of all books

    GET /books/

Example response:
 ```json
[
  {
    "id": 0,
    "title": "The Book Title",
    "author": [
      {
        "id": 0,
        "first_name": "John",
        "last_name": "Smith"
      }
    ],
    "summary": "Short summary of the book.",
    "genre": [
      {
        "id": 0,
        "name": "Fantasy"
      }
    ],
    "image": "image_url",
    "rating": 7.8,
    "number_of_ratings": 230,
    "book_review": {
      "user": "Username",
      "review": "Commentary on the book."
    }
  }
]
 ```

#### Add new book

    POST /books/


Example request body:

```json
{
  "title": "The Book Title",
  "author": [
    {
      "id": 0
    }
  ],
  "summary": "Short summary of the book.",
  "genre": [
    {
      "name": "Fantasy"
    }
  ],
  "image": "image_url"
}
```
Example response:
```json
{
  "id": 0,
  "title": "The Book Title",
  "author": [
    {
      "id": 0,
      "first_name": "John",
      "last_name": "Smith"
    }
  ],
  "summary": "Short summary of the book.",
  "genre": [
    {
      "id": 0,
      "name": "Fantasy"
    }
  ],
  "image": "image_url"
}
```

#### Get a book with id = book_id

    GET /books/<book_id>/

Example response:
```json
{
  "id": 0,
  "title": "The Book Title",
  "author": [
    {
      "id": 0,
      "first_name": "John",
      "last_name": "Smith"
    }
  ],
  "summary": "Short summary of the book.",
  "genre": [
    {
      "id": 0,
      "name": "Fantasy"
    }
  ],
  "image": "image_url",
  "rating": 7.8,
  "number_of_ratings": 230,
  "book_review": {
    "user": "Username",
    "review": "Commentary on the book."
  }
}
```

#### Update the book with id = book_id

    PATCH /books/<book_id>/
Example request body:

```json
{
  "title": "The Book Title",
  "author": [
    {
      "id": 0
    }
  ],
  "summary": "Short summary of the book.",
  "genre": [
    {
      "name": "Fantasy"
    }
  ],
  "image": "image_url"
}
```
Example response:
```json
{
  "id": 0,
  "title": "The Book Title",
  "author": [
    {
      "id": 0,
      "first_name": "John",
      "last_name": "Smith"
    }
  ],
  "summary": "Short summary of the book.",
  "genre": [
    {
      "id": 0,
      "name": "Fantasy"
    }
  ],
  "image": "image_url",
  "rating": 7.8,
  "number_of_ratings": 230,
  "book_review": {
    "user": "Username",
    "review": "Commentary on the book."
  }
}
```

#### Delete book with id = book_id
    DELETE /books/<book_id>/

---

### Authors

#### Get a list of all authors

    GET /authors/
Example response:
 ```json
[
  {
    "id": 0,
    "first_name": "John",
    "last_name": "Smith",
    "date_of_birth": "20/09/1923",
    "date_of_death": "12/03/1987",
    "description": "Short biography of the author.",
    "books": [
      {
        "id": 0,
        "title": "The Book"
      },
      {
        "id": 1,
        "title": "New Book"
      }
    ]
  }
]
 ```

#### Get the author with id = author_id

    GET /authors/<author_id>/
Example response:
 ```json
{
  "id": 0,
  "first_name": "John",
  "last_name": "Smith",
  "date_of_birth": "20/09/1923",
  "date_of_death": "12/03/1987",
  "description": "Short biography of the author.",
  "books": [
    {
      "id": 0,
      "title": "The Book"
    },
    {
      "id": 1,
      "title": "New Book"
    }
  ]
}
 ```

#### Add a new author

    POST /authors/<author_id>/
Example request body:
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "date_of_birth": "20/09/1923",
  "date_of_death": "12/03/1987",
  "description": "Short biography of the author."
}
```
Example response:
```json
{
  "id": 0,
  "first_name": "John",
  "last_name": "Smith",
  "date_of_birth": "20/09/1923",
  "date_of_death": "12/03/1987",
  "description": "Short biography of the author."
}
```

#### Update the author with id = author_id

    PATCH /authors/<author_id>/

Example request body:

```json
{
  "first_name": "John",
  "last_name": "Smith",
  "date_of_birth": "20/09/1923",
  "date_of_death": "12/03/1987",
  "description": "Short biography of the author."
}
```
Example response:
```json
{
  "id": 0,
  "first_name": "John",
  "last_name": "Smith",
  "date_of_birth": "20/09/1923",
  "date_of_death": "12/03/1987",
  "description": "Short biography of the author."
}
```

#### Delete author with id = author_id

    DELETE /authors/<author_id>/
---

### Genres

#### Get a list of all genres

    GET /genres/
Example response:
```json
[
  {
    "id": 0,
    "name": "Fantasy",
    "books": [
      {
        "id": 0,
        "title": "The Book"
      },
      {
        "id": 1,
        "title": "New Book"
      }
    ]
  }
]
```

#### Add a new genre

    POST /genres/
Example request body:
```json
{
  "name": "Fantasy"
}
```
Example response:
```json
{
  "id": 0,
  "name": "Fantasy"
}
```

#### Get the genre with id = genre_id

    GET /genres/<genre_id>/
Example response:
```json
{
  "id": 0,
  "name": "Fantasy",
  "books": [
    {
      "id": 0,
      "title": "The Book"
    },
    {
      "id": 1,
      "title": "New Book"
    }
  ]
}
```

#### Update the genre with id = genre_id

    PATCH /genres/<genre_id>/
Example request body:
```json
{
  "name": "Fantasy"
}
```
Example response:
```json
{
  "id": 0,
  "name": "Fantasy"
}
```

#### Delete genre with id = genre_id

    DELETE /genres/<genre_id>/

---

### Reviews

#### Get a list of all current user reviews
    GET /reviews/
Example response:

```json
[
  {
    "id": 0,
    "book": {
      "id": 0,
      "title": "The Book"
    },
    "rating": 7,
    "review": "Good"
  }
]
```

#### Add new review

    POST /reviews/
Example request body:
```json
{
  "book": {
    "id": 0
  },
  "rating": 7,
  "review": "Good"
}
```
Example response:
```json
{
  "id": 0,
  "book": {
    "id": 0,
    "title": "The Book"
  },
  "rating": 7,
  "review": "Good"
}
```

#### Get the review wih id = review_id

    GET /reviews/<review_id>/
Example response:
```json
{
  "id": 0,
  "book": {
    "id": 0,
    "title": "The Book"
  },
  "rating": 7,
  "review": "Good"
}
```

#### Update the review with id = review_id

    PATCH /reviews/<review_id>/
Example request body:
```json
{
  "book": {
    "id": 0
  },
  "rating": 7,
  "review": "Good"
}
```
Example response:
```json
{
  "id": 0,
  "book": {
    "id": 0,
    "title": "The Book"
  },
  "rating": 7,
  "review": "Good"
}
```

#### Delete review with id = review_id

    DELETE /review/<review_id>/


