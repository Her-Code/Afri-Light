# lnd_client.py
import os
from dotenv import load_dotenv
from lndgrpc import LNDClient

# Load environment variables from .env file
load_dotenv()

LND_DIR = os.path.expanduser(os.getenv('LND_DIR'))  # still expand ~
LND_GRPC_HOST = os.getenv('LND_GRPC_HOST', 'localhost')
LND_GRPC_PORT = int(os.getenv('LND_GRPC_PORT', '10009'))

lnd = LNDClient(
    lnd_dir=LND_DIR,
    grpc_host=LND_GRPC_HOST,
    grpc_port=LND_GRPC_PORT
)
