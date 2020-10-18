import sys
from incoming import (
    grpc,
    http
)


if __name__ == '__main__':
    if sys.argv[1] == 'http' or sys.argv[1] is None:
        http.run()
    elif sys.argv[1] == 'grpc':
        grpc.run()
