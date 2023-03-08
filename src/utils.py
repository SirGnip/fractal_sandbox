import time


class SimpleTimer:
    """Time block of code with a context manager"""
    def __init__(self):
        self.start = 0.0
        self.elapsed = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.elapsed = time.perf_counter() - self.start