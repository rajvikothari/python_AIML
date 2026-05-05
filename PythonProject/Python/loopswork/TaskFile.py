'''
Tasks for Loops in Python

1. For Loop Tasks
Print even, odd numbers between 1 and 20.
Calculate the sum of all elements in a list.
Find the factorial of a number using a for loop
Iterate through a dictionary and print keys and values.
Generate a multiplication table of a given number.
Reverse a list using a for loop.
Print the Fibonacci series up to n terms.  0 1 1 2 3 5 8 13....

2. While Loop Tasks
Find the sum of digits of a number using a while loop.
Keep taking user input until they enter "exit".
Reverse a number using a while loop.
Count the number of digits in a number.
Check if a number is a palindrome.
Print the Fibonacci series using a while loop.
'''

# 1. For Loop Tasks
# Print even, odd numbers between 1 and 20.
# Even numbers between 1 and 20
# print("Even numbers:")
# for i in range(1, 21):
#     if i % 2 == 0:
#         print(i, end=' ')
#
# print("\nOdd numbers:")
# # Odd numbers between 1 and 20
# for i in range(1, 21):
#     if i % 2 != 0:
#         print(i, end=' ')


# 2. Calculate the sum of all elements in a list.
# my_list = [1, 2, 3, 4, 5]
# total = sum(my_list)
# print("Sum of all elements:", total)


# 3. Find the factorial of a number using a for loop


#4. Iterate through a dictionary and print keys and values.
# my_dict = {
#     "name": "rajvi",
#     "age": 26,
#     "city": "Ahmedabad"
# }
#
# for key, value in my_dict.items():
#     print("Key:", key, "-> Value:", value)


#5. Generate a multiplication table of a given number.
# Get input from user
# number = int(input("Enter a number to generate its multiplication table: "))
#
# # Set the range for the table (1 to 10 by default)
# print(f"\nMultiplication Table for {number}:\n")
# for i in range(1, 11):
#     print(f"{number} x {i} = {number * i}")

#6. Reverse a list using a for loop.
# string = ['a', 'b', 'c', 'd']
# reversed = []
# for i in range(len(string) - 1, -1, -1):
#     reversed.append(string[i])
#
# print(reversed)


#7. Print the Fibonacci series up to n terms.  0 1 1 2 3 5 8 13....
# def fibonacci_series(n):
#     a, b = 0, 1
#     for _ in range(n):
#         print(a, end=' ')
#         a, b = b, a + b
#
# # Example usage:
# n = int(input("Enter the number of terms: "))
# fibonacci_series(n)



'''2. While Loop Tasks'''
#1. Find the sum of digits of a number using a while loop.
# Input number
# num = int(input("Enter a number: "))
#
# # Initialize sum
# sum_of_digits = 0
#
# # Use while loop to sum the digits
# while num > 0:
#     digit = num % 10        # Get the last digit
#     sum_of_digits += digit  # Add it to the sum
#     num = num // 10         # Remove the last digit
#
# # Print the result
# print("Sum of digits:", sum_of_digits)


#3. Reverse a number using a while loop.
# Input from the user
# string = ['a', 'b', 'c', 'd', 'e', 'f']
# reversed_list = []
#
# i = len(string) - 1  # Start from the last index
#
# while i >= 0:
#     reversed_list.append(string[i])
#     i -= 1
#
# print(reversed_list)

#4 Count the number of digits in a number.
# Input number
# num = int(input("Enter a number: "))
#
# # Handle negative numbers
# num = abs(num)
#
# # Special case for 0
# if num == 0:
#     count = 1
# else:
#     count = 0
#     # Use while loop to count digits
#     while num > 0:
#         num = num // 10
#         count += 1
#
# # Print the result
# print("Number of digits:", count)


#5 Check if a number is a palindrome.

#6 Print the Fibonacci series using a while loop.
# Input: how many terms to print
# n = int(input("Enter the number of terms: "))
#
# # First two terms of the Fibonacci sequence
# a, b = 0, 1
# count = 0
#
# # Print the Fibonacci series
# print("Fibonacci Series:")
# while count < n:
#     print(a, end=" ")
#     a, b = b, a + b
#     count += 1


