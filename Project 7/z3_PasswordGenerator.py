import random
import string

class PasswordGenerator:
    # initialize the generator with length, charset and count
    def __init__(self, length, charset=None, count=10):
        self.length = length  # Desired password length
        self.charset = charset or (string.ascii_letters + string.digits)  # Default charset
        self.count = count  # Number of passwords to generate
        self.generated = 0  # Counter for generated passwords

    # return self as iterator
    def __iter__(self):
        return self

    # generate next password or raise StopIteration
    def __next__(self):
        if self.generated >= self.count:
            # no more passwords
            raise StopIteration  
        self.generated += 1
        # manually build a password character by character
        password = ''.join(map(lambda _: random.choice(self.charset), range(self.length)))
        return password


if __name__ == "__main__":
    print("Using next() explicitly:")
    gen = PasswordGenerator(length=8, count=3)
    print(next(gen))
    print(next(gen))
    print(next(gen))
    # print(next(gen))  # Would raise StopIteration

    print("\nUsing for loop:")
    for pwd in PasswordGenerator(length=10, count=5):
        print(pwd)
