''' # Function for finding prime numbers in a given range
def judge(n) -> bool:
    for x in range(2, int((n ** 0.5) // 1) + 1):
        if n % x == 0:
            return False
    return True


for i in range(2, 100):
    if judge(i):
        print(i)
'''
