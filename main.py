from bloomfilter import BloomFilter
from sys import argv

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
            print(f"False Positive Rate: {bf.get_false_positive_rate()}")
            quit(1)
        # Print Optimal Hash Count
        elif arg5 == "-h":
            print(f"Optimal Hash Count: {bf.get_hash_count()}")
            quit(1)
        # Print bit array
        elif arg5 == "-b":
            print(f"Bit Array: {bf.get_bit_array()}")
            quit(1)
        # Print False Positive Rate and Optimal Hash Count
        elif arg5 == "-d":
            print(f"False Positive Rate: {bf.get_false_positive_rate()}")
            print(f"Optimal Hash Count: {bf.get_hash_count()}")
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
            print(f"{item}: Possibly present")
        else:
            print(f"{item}: Not present")

    # Print result data
    print("\n"
          f"Optimal Hash Count: {bf.get_hash_count()}\n"
          f"False Positive Rate: {bf.get_false_positive_rate()}"
          )
