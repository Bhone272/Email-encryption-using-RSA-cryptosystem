import random
from math import gcd

# --- Helper Functions ---
def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_prime(start=20000000000000000000, end=30000000000000000000):
    primes = [i for i in range(start, end) if is_prime(i)]
    return random.choice(primes)

def mod_inverse(e, phi):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % phi

# --- RSA Key Generation ---
def generate_keys():
    p = 1000000007 
    q = 2232232273
    while q == p:
        q = generate_prime()

    print(f"Chosen primes:\np = {p}, q = {q}")

    n = p * q
    phi = (p - 1) * (q - 1)
    print(f"n = p * q = {n}")
    print(f"phi(n) = (p-1)*(q-1) = {phi}")

    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    print(f"Chosen e = {e} (1 < e < phi and gcd(e, phi)=1)")

    d = mod_inverse(e, phi)
    print(f"Computed d = {d} (mod inverse of e mod phi)")

    return ((e, n), (d, n))  # public, private

# --- Encryption ---
def encrypt(message, public_key):
    e, n = public_key
    print("\nEncryption process:")
    encrypted = []
    for char in message:
        m = ord(char)
        c = pow(m, e, n)
        print(f"char '{char}' -> ASCII {m} -> (m^e mod n) = {m}^{e} mod {n} = {c}")
        encrypted.append(c)
    return encrypted

# --- Decryption ---
def decrypt(ciphertext, private_key):
    d, n = private_key
    print("\nDecryption process:")
    decrypted_chars = []
    for c in ciphertext:
        m = pow(c, d, n)
        print(f"cipher {c} -> (c^d mod n) = {c}^{d} mod {n} = {m} -> char '{chr(m)}'")
        decrypted_chars.append(chr(m))
    return ''.join(decrypted_chars)


# --- Example Usage ---
public_key, private_key = generate_keys()
print("\nPublic Key:", public_key)
print("Private Key:", private_key)

msg = "HELLO WELCOME TO MIIT.EDU.MM"
print("\nOriginal Message:", msg)

encrypted = encrypt(msg, public_key)
print("\nEncrypted Message:", encrypted)

decrypted = decrypt(encrypted, private_key)
print("\nDecrypted Message:", decrypted)