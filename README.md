# Timing Attack

---

## What is a Timing Attack

A **Timing Attack** is a method of breaking a system in which an attacker measures the **time** it takes for a server to process a request, and uses that data to infer secret information. Unlike brute‑force password guessing, here there is no need to try millions of combinations. It is enough to measure how the response time changes depending on the input data.

This attack belongs to the class of **side‑channel** attacks, because it exploits not the code itself but its **physical manifestations** (time, power consumption, electromagnetic radiation).

---

## How the Attack Works

When a server verifies a password, it usually compares it character by character:

Compares the first character -> matches

Compares the second character -> matches

Compares the third character -> DOES NOT match -> exits

The attacker sends many requests with different characters and measures the response time. The character that produces the **largest delay** is most likely the correct one.

---

## What’s Inside the Project

The repository contains three main files:

- `app.py` – vulnerable server (with an artificial delay)
- `app_secure.py` – protected server (with constant‑time comparison)
- `attacker.py` – the program that recovers the password by timing

---

## How to Run

### 1. Install dependencies

```bash
pip install flask requests
```

### 2. Start the vulnerable server

```bash
python app.py
```

### 3. In another terminal, run the attacker

```bash
python attacker.py
```

### 4. Test the protected version
Stop the vulnerable server with Ctrl + C and run:
```bash
python app_secure.py
```

---

## How the Code Works

### Vulnerable Server (`app.py`)

The server stores the password `"86t4RF"`
On each request it compares the password character by character. If a character is correct, the server inserts a delay of **10 ms** and moves to the next one. If a character is wrong, it immediately replies with `ok: false`.

This delay is what creates the vulnerability: the attacker sees that the correct character causes a **longer** response time and thus identifies it.

---

Attacker (`attacker.py`)

The attacker tries characters position by position: first it finds the first character, then the second, and so on. For each candidate it sends **20 requests**, averages the response time, and chooses the character that produced the **maximum delay**.

The password is reconstructed one character at a time.

---

Protected Server (`app_secure.py`)

Instead of storing the password itself, the server stores its **hash** (SHA‑256). When a request arrives, it computes the hash of the entered password and compares the two hashes using `hmac.compare_digest()`.

This comparison is performed in near‑constant time - it does not depend on how many characters match.

The attacker does not see any dependency between the response time and the correctness of the password - the attack **fails**.

---

## Results

### Successful Attack on the Vulnerable Server (`app.py`)

The response time for the correct character is **noticeably larger** than for the others:

AAAAAA: 0.002619

BAAAAA: 0.002386

...

7AAAAA: 0.002358

**8AAAAA: 0.016290 <- time jumps sharply**

9AAAAA: 0.002893

-> 8

The attacker determines the first character - `8`, then continues:

-> 8

-> 86

-> 86t

-> 86t4

-> 86t4R

-> 86t4RF

FOUND: 86t4RF

**Result**: password successfully recovered.

**Why the attack works:**
The vulnerable server compares the password character by character and stops at the first mismatch. After each **correct** character it introduces an artificial delay (`sleep(0.01)`). The response time depends on the number of correct characters at the beginning - the attacker measures this difference.

The artificial delay is added **solely for demonstration purposes**. In real‑world systems the attack works even without it - the timing difference is in the microsecond or nanosecond range, but it can still be measured with a sufficient number of requests. The code of the vulnerable server models a common programming mistake: character‑by‑character comparison with early exit. This kind of logic is exactly what can leak information through response timing.

---

### Failed Attack on the Protected Server (`app_secure.py`)

On the protected server the attacker **cannot** determine the correct characters. The response time is **almost the same** for all candidates:

AAAAAA: 0.002559

BAAAAA: 0.002295

...

8AAAAA: 0.002375

9AAAAA: 0.002445

-> е

The attacker picks the first character as - `е`, but it is a random choice:

-> e

-> eV

-> eVi

-> eVi7

-> eVi7q

-> eVi7qC

FOUND: eVi7qC

**Result:** the attacker outputs an **incorrect password** (`eVi7qC`), which does not match the real one (`86t4RF`).

**Why the attack fails:**
The protected server **does not compare passwords character by character.**
Instead it:

1. Computes the SHA‑256 hash of the entered password.
2. Compares the hashes using `hmac.compare_digest()`.

hmac.compare_digest() performs the comparison in near‑constant time - the time does not depend on how many characters match. The response time is independent of the password, so the attacker cannot distinguish correct from incorrect characters.

---

## Conclusion

Timing attacks are a real threat that can be carried out even without specialised hardware.
This project demonstrates that:

- The vulnerability arises from character‑by‑character comparison with early exit.

- Protection is achieved by using constant‑time comparison (`hmac.compare_digest`).

- An artificial delay is not a security measure - it only amplifies the effect for demonstration purposes.

This project is useful for understanding side‑channel attacks and how to prevent them.





















