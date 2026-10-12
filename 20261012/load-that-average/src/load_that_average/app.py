import threading
from threading import Event
import time
import os
from functools import partial
from load_that_average.db_wrapper import DbWriter, DbReader
from load_that_average.http_server import HTTPServer, RequestHandler

def log_load_average(db_path, interval: int, exit_flag: Event):
    writer = DbWriter(db_path)
    while not exit_flag.is_set():
        writer.store_load_average(*os.getloadavg())
        time.sleep(interval)

def main():
    db_path = f'/tmp/test_loadavg-{int(time.time())}.db'
    exit_flag = Event()
    log_load_average_thread = threading.Thread(target=log_load_average,
                                               args=[db_path, 2, exit_flag])

    log_load_average_thread.start()

    time.sleep(1)
    # reader = DbReader(db_path)

    # for _ in range(6):
    #     print("wait 5 seconds")
    #     time.sleep(5)
    #     for lavg in reader.get_latest_load_averages():
    #         print(lavg)

    configured_handler = partial(RequestHandler, db_path)
    server_address = ('', 8000)
    try:
        httpd = HTTPServer(server_address, configured_handler)
        print("Start Serving", server_address)
        httpd.serve_forever()
    except Exception as e:
        print(e)
        pass
    
    print("shutting down")
    exit_flag.set()
    log_load_average_thread.join()
    print("All ready. Exiting")
    
    
