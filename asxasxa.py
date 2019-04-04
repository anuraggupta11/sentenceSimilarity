import time



import concurrent.futures
from concurrent.futures import ThreadPoolExecutor


def asas(a,b):
    print("Before the sleep statement")
    time.sleep(5)
    print("After the sleep statement")
    return a+b


def main():
    x = [1,2,3,4,5,6,789]
    v = 1
    futures = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        for x1 in x:
             future = executor.submit(asas, x1, v)
             futures.append(future)
    print('Started')
    for future in futures:
        try:
            z = future.result(timeout=1000)
            print(z)
        except Exception as exc:
            print(exc)
        #break
    print('Done')

if __name__ == '__main__':
    main()
