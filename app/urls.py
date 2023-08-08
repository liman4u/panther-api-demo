from app.apis import (
    hello_world_api,
    info_api,
    book_api,
    single_book_api,
)

urls = {
    '/': hello_world_api,
    'info/': info_api,
    'book/': book_api,
    'book/<int:book_id>/': single_book_api,
}
