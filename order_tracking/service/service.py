import grpc
from pb_grpc.order_tracking_pb2 import Status
from pb_grpc.order_tracking_pb2 import Destination
from pb_grpc.order_tracking_pb2 import Order
from pb_grpc.order_tracking_pb2 import CreateOrderRequest
from pb_grpc.order_tracking_pb2 import CreateOrderResponse
from pb_grpc.order_tracking_pb2 import GetOrderRequest
from pb_grpc.order_tracking_pb2 import GetOrderResponse
from pb_grpc.order_tracking_pb2 import UpdateOrderRequest
from pb_grpc.order_tracking_pb2 import UpdateOrderResponse
from pb_grpc.order_tracking_pb2 import DeleteOrderRequest
from pb_grpc.order_tracking_pb2 import DeleteOrderResponse
from pb_grpc import order_tracking_pb2_grpc

from repository.repository_db import RepositoryDB

class Order_trackingService(order_tracking_pb2_grpc.OrderTrackingServiceServicer,):
	def __init__(self, repository: RepositoryDB):
		super().__init__()
		self.repository = repository

	def CreateOrder(self, request: CreateOrderRequest, context: grpc.RpcContext) -> CreateOrderResponse:
		order_name = request.name
		order_destination = request.destination
		order_status = Status.CREATED
		order = Order(name=order_name, destination=order_destination, status=order_status)
		order_created = None
		try:
			order_created = self.repository.save(order)
		except Exception as e:
			raise e
		return CreateOrderResponse(order=order_created)

	def GetOrder(self, request: GetOrderRequest, context: grpc.RpcContext) -> GetOrderResponse:
		order_id = request.id
		order = None
		try:
			order = self.repository.get(order_id)
		except Exception as e:
			raise e
		else:
			return GetOrderResponse(order=order)

	def UpdateOrder(self, request: UpdateOrderRequest, context: grpc.RpcContext) -> UpdateOrderResponse:
		order_id = request.id
		order_status = request.status
		old_order = None
		try:
			old_order = self.repository.get(order_id)
		except Exception as e:
			raise e
		else:
			new_order = Order(name=old_order.name, destination=old_order.destination, status=order_status)
			try:
				self.repository.update(order_id, new_order)
			except Exception as e:
				raise e
			else:
				return UpdateOrderResponse(order=new_order)
			


	def DeleteOrder(self, request: DeleteOrderRequest, context: grpc.RpcContext) -> DeleteOrderResponse:
		order_id = request.id
		try:
			self.repository.delete(order_id)
		except Exception as e:
			raise e
		else:
			return DeleteOrderResponse()

