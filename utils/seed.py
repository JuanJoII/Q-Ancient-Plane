import time

def generate_seed():
    return int(time.time() * 1000) % 1000000