from multiprocessing import Pool
import os

"""def myfunc(x):
    return 5 + x

if __name__ == '__main__':
    print("total of CPU's: ",os.cpu_count())
    p = Pool(processes=3)
    print(p.map(myfunc, [1, 2, 3]))
    p.close()"""
    
import time
from multiprocessing import Pool


def square(x):
    print(f"start process {x}")
    square = x * x
    time.sleep(1)
    print(f"end process {x}")
    return square


if __name__ == "__main__":
    pool = Pool()
    a = pool.imap(square, range(0, 5))
    for i in a:
        print(f"showing the result as it is ready {i}")
    
    pool.close()