import random
import string

def generate_coupon_code():
    prefix = "PA"
    number = random.randint(10, 999)
    return f"{prefix}{number}"




def generate_coupon_name():
    letters = ''.join(random.choices(string.ascii_letters, k=2)).title()
    numbers = random.randint(10000, 99999)
    return f"{letters}{numbers}"