import os
import datetime

PWD = os.path.dirname(os.path.abspath(__file__))
TIMESTAMP_DIR = os.path.join(PWD, "updated_timestamp.py")

def update_timestamp():
    with open(TIMESTAMP_DIR, "w") as fp:
        fp.write(f'"Updated {str(datetime.datetime.now(datetime.timezone.utc))}"\n')


if __name__ == "__main__":
    update_timestamp()
