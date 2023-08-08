from datetime import datetime, timedelta
from app.models import Book
from app.serializers import BookOutputSerializer, BookSerializer
from panther.throttling import Throttling

from panther.app import API
from panther.configs import config
from panther import version, status
from panther.request import Request
from panther.response import Response
from app.throttling import InfoThrottling


@API()
async def hello_world_api():
    return {'detail': 'Hello World'}


@API(cache=True, throttling=InfoThrottling)
async def info_api(request: Request):
    data = {
        'version': version(),
        'datetime_now': datetime.now().isoformat(),
        'user_agent': request.headers.user_agent,
        'db_engine': config['db_engine'],
    }
    return Response(data=data, status_code=status.HTTP_202_ACCEPTED)


@API(
    input_model=BookSerializer,
    output_model=BookOutputSerializer,
    cache=True,
    cache_exp_time=timedelta(seconds=10),
    throttling=Throttling(rate=10, duration=timedelta(minutes=1))
)
async def book_api(request: Request):
    if request.method == 'POST':
        body: BookSerializer = request.data
        print(body)
        try:
            book: Book = Book.insert_one(
                name=body.name,
                author=body.author,
                pages_count=body.pages_count,
            )
            return Response(data=book, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'detail': str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        books: list[Book] = Book.find()
        return Response(data=books, status_code=status.HTTP_200_OK)

    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@API(input_model=BookSerializer)
async def single_book_api(request: Request, book_id: int):
    body: BookSerializer = request.data
    if request.method == 'GET':
        book: Book = Book.find_one(id=book_id)
        if book:
            return Response(data=book, status_code=status.HTTP_200_OK)
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        book: Book = Book.find_one(id=book_id)
        book.update(
            name=body.name,
            author=body.author,
            pages_count=body.pages_count,
        )
        # Another way:
        # is_updated: bool= Book.updateone({'id': book_id}, **body.dict())
        # updated_count: int= Book.updatemany({'id': book_id}, **body.dict())
        return Response(status_code=status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        is_deleted: bool = Book.delete_one(id=book_id)
        if is_deleted:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
        # Another way:
        # is_deleted: bool= Book.deleteone(id: book_id)
        # deleted_count: int= Book.deletemany(id: book_id)
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)



