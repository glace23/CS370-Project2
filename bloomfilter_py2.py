from Crypto.Hash import MD5
from bitarray import bitarray
import math
from sys import argv


class BloomFilter:
    """
    Class for Bloom Filter
    """

    def __init__(self, n, m):
        """
        :param int n:
            size of dictionary
        :param int m:
            size of bit vector
        """
        # Size of dictionary
        self.dictionary_size = n

        # size of bit array
        self.array_size = m

        # set number of hash functions
        self.hash_count = int((self.array_size / self.dictionary_size) * math.log(2))

        # set false positive rate
        self.false_positive = (1 - math.e ** (
                -self.hash_count * self.dictionary_size / self.array_size)) ** self.hash_count

        # initialize bitarray and all bits to 0
        self.bitarray = bitarray(self.array_size)
        self.bitarray.setall(0)

    def get_hash_count(self):
        """
        Get the number of hash counts
        :return:
            number of hash counts
        :rtype:
            int
        """
        return self.hash_count

    def get_false_positive_rate(self):
        """
        Get the rate of false positives with 3 decimals
        :return:
            rate of false positives
        :rtype:
            float
        """
        return round(self.false_positive, 3)

    def get_bit_array(self):
        """
        Get current bit array of filter
        :return:
            bit array of filter
        :rtype:
            bitarray
        """
        return self.bitarray

    def add(self, item):
        """
        Adds a user defined item to filter
        :param string item:
            item to add to filter
        :return:
            None
        """
        item.encode(encoding='utf-8', error='replace')
        # set bitarray for hash count times
        for i in range(0, self.hash_count):
            # Initialize hash value for first loop
            if i == 0:
                hash_item = MD5.new(data=bytearray(item, encoding='utf-8'))
            # Update hash value for subsequent loop
            else:
                hash_item.update(data=bytearray(item, encoding='utf-8'))

            # Get index for bit array
            # Digest hex hash value and convert to decimal
            index = int(hash_item.hexdigest(), 16) % self.array_size

            # Set bit array to True for index
            self.bitarray[index] = 1

    def check(self, item):
        """
        Checks whether a user defined item may be in filter or item is not in filter
        :param string item:
            item to check if in filter
        :return:
            item is in filter or not
        :rtype:
            boolean
        """
        item.encode(encoding='utf-8', error='replace')
        for i in range(0, self.hash_count):
            # Initialize hash value for first loop
            if i == 0:
                hash_item = MD5.new(data=bytearray(item, encoding='utf-8'))
            # Update hash value for subsequent loop
            else:
                hash_item.update(data=bytearray(item, encoding='utf-8'))

            # Get index for bit array
            # Digest hex hash value and convert to decimal
            index = int(hash_item.hexdigest(), 16) % self.array_size

            # if a bit is false, then item does not exist in filter
            if self.bitarray[index] == 0:
                return False

        # Item may exist in filter
        return True


if __name__ == "__main__":
    # Report error for too few or too many command line arguments
    if len(argv) < 4:
        print("Not enough Arguments!")
    elif len(argv) > 5:
        print("Too Many Arguments!")
    else:
        # arg1 = Script
        # arg2 = Input File
        # arg3 = Dictionary File
        # arg4 = Bit Array Size
        # arg5 = Optional Argument
        if len(argv) == 5:
            arg1, arg2, arg3, arg4, arg5 = argv
        else:
            arg1, arg2, arg3, arg4 = argv
            arg5 = None

        # Check error if arg4 is not integer
        if not arg4.isdigit():
            print("Bitarray size is invalid!")
            quit(1)

        # get lines from arg2 input file
        with open(arg2) as f:
            input = f.readlines()

        # get lines from arg3 dictionary file
        with open(arg3) as f:
            dictionary = f.readlines()

        # Dictionary size
        n = len(dictionary)
        # Bit array size
        m = int(arg4)

        # BloomFilter Object
        bf = BloomFilter(n, m)

        # Optional Command Line Argument
        if arg5 is not None:
            # Print False Positive Rate
            if arg5 == "-f":
                print("False Positive Rate: ", bf.get_false_positive_rate())
                quit(1)
            # Print Optimal Hash Count
            elif arg5 == "-h":
                print("Optimal Hash Count: ", bf.get_bit_array())
                quit(1)
            # Print bit array
            elif arg5 == "-b":
                print("Bit Array: ", bf.get_bit_array())
                quit(1)
            # Print False Positive Rate and Optimal Hash Count
            elif arg5 == "-d":
                print("False Positive Rate: ", bf.get_false_positive_rate())
                print("Optimal Hash Count: ", bf.get_hash_count())
                quit(1)

        # Error check for hash count
        if bf.get_hash_count() == 0:
            print("Bit Array is too small for dictionary set!\n"
                  "Optimal Hash Count is 0.")
            quit(1)

        # Error check for False Positive Rate
        if bf.get_false_positive_rate() == 1:
            print("Bit Array is too small for dictionary set!\n"
                  "False Positive Rate is 1.")
            quit(1)

        # Add dictionary items to filter
        for line in dictionary:
            item = line.rstrip("\n")
            bf.add(item)

        # Check input items in filter
        for line in input:
            item = line.rstrip("\n")
            result = bf.check(item)
            if result is True:
                print(item, ": Possibly present")
            else:
                print(item, ": Not present")

        # Print result data
        print()
        print("False Positive Rate: ", bf.get_false_positive_rate(), "\n")
        print("Optimal Hash Count: ", bf.get_hash_count(), "\n")
        print("Bitarray Size: ", m)
