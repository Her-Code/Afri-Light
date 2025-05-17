# import threading
# import time
# from lndgrpc import LNDClient
# from models import db, LightningInvoice

# class InvoiceStreamer:
#     def __init__(self, lnd_client):
#         self.lnd = lnd_client
#         self._stop_event = threading.Event()
#         self._thread = None

#     def start(self):
#         if self._thread and self._thread.is_alive():
#             return  # Already running
#         self._stop_event.clear()
#         self._thread = threading.Thread(target=self._stream_invoices, daemon=True)
#         self._thread.start()

#     def stop(self):
#         self._stop_event.set()
#         if self._thread:
#             self._thread.join()

#     def _stream_invoices(self):
#         print("Starting invoice subscription stream...")
#         while not self._stop_event.is_set():
#             try:
#                 for invoice_update in self.lnd.subscribe_invoices():
#                     if self._stop_event.is_set():
#                         break
#                     r_hash_hex = invoice_update.r_hash.hex()
#                     print(f"Invoice update: {r_hash_hex}, settled: {invoice_update.settled}")

#                     invoice = LightningInvoice.query.filter_by(r_hash_hex=r_hash_hex).first()
#                     if invoice:
#                         invoice.status = 'settled' if invoice_update.settled else 'pending'
#                         db.session.commit()

#             except Exception as e:
#                 print(f"Stream error: {e}. Reconnecting in 5 seconds...")
#                 time.sleep(5)

import threading
import time
from models import db, LightningInvoice

class InvoiceStreamer:
    def __init__(self, lnd_client):
        self.lnd = lnd_client
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return  # Already running
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._stream_invoices, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()

    def _stream_invoices(self):
        print("Starting invoice subscription stream...")
        while not self._stop_event.is_set():
            try:
                for invoice_update in self.lnd.subscribe_invoices():
                    if self._stop_event.is_set():
                        break

                    r_hash_hex = invoice_update.r_hash.hex()
                    print(f"Invoice update: {r_hash_hex}, settled: {invoice_update.settled}")

                    invoice = LightningInvoice.query.filter_by(r_hash_hex=r_hash_hex).first()
                    if invoice:
                        invoice.status = 'settled' if invoice_update.settled else 'pending'
                        db.session.commit()
            except Exception as e:
                print(f"Stream error: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
