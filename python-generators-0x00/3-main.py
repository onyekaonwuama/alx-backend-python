#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_paginate

try:
    for page in lazy_paginator(100):  # Change the page size as needed
        for user in page:
            print(user)
except BrokenPipeError:
    sys.stderr.close()
