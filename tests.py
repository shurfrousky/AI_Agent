from functions.write_file import *


print(write_file("calculator", "tast.txt", "wait, this isn't lorem ipsum"))


print(write_file("calculator", "pkger/morelorem.txt", "lorem ipsum dolor sit amet"))


print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))