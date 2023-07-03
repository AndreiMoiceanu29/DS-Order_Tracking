from .crud_repository import CRUDRepository
from database import MongoDatabase
from pb_grpc.order_tracking_pb2 import Order


class RepositoryDB(CRUDRepository):
    def __init__(self, database: MongoDatabase) -> None:
        super().__init__(database)
        self._set_object_type(Order)
        self._set_collection("orders")