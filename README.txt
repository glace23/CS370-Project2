Usage: python3 bloomfilter.py input_filename dictionary_filename bitarray_size [-b | -d | -f | -h]

Required Command Line Argument:
input_filename          input file to check against dictionary's filter
dictionary_filename     dictionary file to create filter
bitarray_size           integer to create a corresponding size bitarray

Optional Command Line Argument:
-b                      outputs entire bitarray
-d                      outputs false positive rate and optimal hash output
-f                      outputs false positive rate
-h                      outputs optimal hash rate

# File Encoding = utf-8