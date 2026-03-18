# UMT-pythonweb-hw-08

## Start

### Install dependencies

```bash
pip install -r requirements.txt
```

### Enviroment

Create a `.env`

```env
DATABASE_URL=postgresql+psycopg://admin:1@localhost:5432/db_name
```

### Execution

```bash
docker compose up -d
uvicorn src.main:app --reload
```

## Swagger

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Endpoints

### Create contact

`POST /contacts/`

```json
{
  "first_name": "Іван",
  "last_name": "Петренко",
  "email": "ivan.petrenko@example.com",
  "phone_number": "+380671234567",
  "birthday": "1999-05-14",
  "additional_data": "Друг з університету"
}
```

### Get all contacts all search

`GET /contacts/`

Приклади:

- `GET /contacts/`
- `GET /contacts/?first_name=Іван`
- `GET /contacts/?last_name=Петренко`
- `GET /contacts/?email=@gmail.com`
- `GET /contacts/?first_name=Іван&email=gmail.com`

### Get contact by id

`GET /contacts/{contact_id}`

### Update contact

`PUT /contacts/{contact_id}`

### Delete contact

`DELETE /contacts/{contact_id}`

### Upcoming birthdays

`GET /contacts/upcoming-birthdays`

example:

- `GET /contacts/upcoming-birthdays`
- `GET /contacts/upcoming-birthdays?days=7`
