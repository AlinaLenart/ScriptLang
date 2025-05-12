import string
import secrets

class PasswordGenerator:
    # initialize the generator with length, charset (with default) and max paswords count to generate
    def __init__(self, length, count, charset = None):
        self.length = length 
        if charset is not None:
            self.charset = charset
        else:
            self.charset = string.ascii_letters + string.digits
        self.count = count 
        # counter for generated passwords
        self.generated = 0 

    # return self as iterator
    def __iter__(self):
        return self

    # generate next password or raise StopIteration
    def __next__(self):
        if self.generated >= self.count:
            # no more passwords (max count reached)
            raise StopIteration  
        self.generated += 1
        # build password using secrets module
        password = self._generate_password()
        return password

    #"secrets module is used for generating cryptographically strong random numbers suitable for managing data such as passwords"
    def _generate_password(self):
        return ''.join(secrets.choice(self.charset) for _ in range(self.length))


def main():
    gen = PasswordGenerator(8, 3)
    print("\Next:")
    print(next(gen))
    print(next(gen))
    print(next(gen))
    # print(next(gen))  # raise StopIteration

    print("\nLoop:")
    for pwd in PasswordGenerator(10, 5):
        print(pwd)


if __name__ == "__main__":
   main()
