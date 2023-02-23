def solution(n):
    # n has 309 digits which can be represented by a float64, how conspicuous...
    n = int(n)
    n = format(n, 'b')
    # This is an interesting problem because it was easier to work out the solution in binary
    # representation.
    
    # The algorithm is:
    # If even, divide n by 2 (drop the last digit in binary), repeat until n is odd or 1.
    # Add 1 if the final two digits are '11'. Subtract otherwise.
    #   This is because after adding, we'll get at least 2 zeros which can be divided 
    #   out with one operation each. If we subtract, we'll only get 1 zero and will 
    #   have to divide once and then either add or subtract again before dividing
    #   which takes 3 operations total.
    # Exception: when n=3 ('11') subtract instead of adding.
    # Repeat
    
    count = 0
    
    def AddOneToOdd(n):
        for idx in [digit for digit in range(len(n)-1)][::-1]:
            if n[idx] == '0':
                n = n[:idx] + '1' + '0' * len(n[idx+1:])
                return n
        n = '1' + '0' * len(n) # in case we have all 1s
        return n

    while n != '1':
        while n[-1] == '0':
            n = n[:-1] # divide by two in binary
            count += 1
        if n == '1':
            return count
        if n[-2:] == '11' and n != '11': # 3 is an edge case here
            n = AddOneToOdd(n)
            count += 1
        else: 
            n = n[:-1] + '0' # Subtract 1 from an odd number in binary
            count += 1

    return count
    
    # If you plot the number of operations vs n it's surprising how few operations are required
    # for large n. I don't think it's asymptotic but could be related to log n or log n / log 2
    # I think I will investigate further when I have time
