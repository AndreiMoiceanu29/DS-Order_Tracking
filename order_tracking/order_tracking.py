""" The Server that handles the periods """
import grpc
from concurrent import futures
from signal import signal, SIGTERM
from service import Order_trackingService
from pb_grpc import order_tracking_pb2_grpc
from repository import RepositoryDB
from logger import mge_log
from database import MongoDatabase



def run_service(port: int) -> None:
    """ Starts the service on the designated port """
    mge_log.info(f"Booting order service...")
    
    database = MongoDatabase("order")
    repository = RepositoryDB(database)
    service = Order_trackingService(repository)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=32))
    order_tracking_pb2_grpc.add_OrderTrackingServiceServicer_to_server(service, server)

    mge_log.info(f"Starting order tracking service on port {port}...")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    mge_log.info(f"Order Tracking service started on port {port}")

    def handle_sigterm(*_):
        """ Handle SIGTERM """

        mge_log.info("Stopping order tracking service...")

        done_event = server.stop(30)
        done_event.wait(30)

        mge_log.info("Order tracking service stopped...")

    server.wait_for_termination()
    signal(SIGTERM, handle_sigterm)

    mge_log.critical("Order tracking service stopped without any reason...")


if __name__ == "__main__":
    run_service(50051)