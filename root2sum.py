def solution(s):
    # This problem was very interesting and difficult.
    
    # First, I noticed that the terms in the summation follow a fractal pattern.
    
    # What I mean by this is that if we look at the number of consecutive integers in the terms, there will either be 2 or 3.
    # For example, the first few terms are 1, 2, 4, 5, 7, 8, 9, 11 so the number of consecutive integers is 2, 2, 3.
    # Moreover, if we follow the update rule 2 -> 2, 3, 2, 3, 2 and 3 -> 2, 3, 2, 3, 2 3, 2, we can recursively calculate the 
    # total number of consecutive integers in the sequence. This was a beautiful pattern but I wasn't able to get my solution
    # down to a low enough time complexity.
    
    # After hours of Googling I found a Mathematics forum posting about a similar question pointing to "Beatty Sequences" (https://mathworld.wolfram.com/BeattySequence.html)
    # Knowing about Beatty Sequences turned out to be quite a big hint, so I can only take partial credit for this solution.
    
    # The idea is as follows. Let a = sqrt(2), an irrational number between 1 and 2. Next, solve for b using 1/a + 1/b = 1.
    # Then the Beatty Sequences {floor(i * sqrt(2))} and {floor(i * (2 + sqrt(2)))} span the positive integers.
    # The key here is that the second Beatty Sequence can be rewritten as {2i + floor(i * sqrt(2))}.
    # Next, we consider the sums of both Beatty Sequences. The sum of both sums is itself the sum of all positive integers
    # up to s = floor(n * sqrt(2)), and the sum from i=1 to n of floor(i * sqrt(2)) (after some arithmetic) becomes
    # s(s+1)/2 - t(t+1) - sum from i=1 to t of floor(i * sqrt(2)) where t is defined as follows:
    # if floor((n-1) * sqrt(2)) is 2 less than floor(n * sqrt(2)), t = ceiling((floor(n * sqrt(2)) - 1)/(2+sqrt(2))).
    # elif floor((n-2) * sqrt(2)) is 3 less than floor(n * sqrt(2)), t = ceiling((floor(n * sqrt(2)) - 2)/(2+sqrt(2))).
    # else t = ceiling((floor(n * sqrt(2)) - 3)/(2+sqrt(2))). 
    # The idea here is that instead of calculating the original sum all the way up to n, we only need to calculate the sum
    # up to t which is only around half of n. 
    # Even better, we can recursively calculate the sum up to t which will only require us to calculate the sum up to roughly 1/2 * t
    # Eventually, t will equal 0 or 1 or 2 and we will have our answer!
    # For n = 10**100, this algorithm will take approximately log base 0.5 or 10^(-100) = 332 steps which is very reasonable.
        
    import math
    
    sqrt2 = 14142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727 # Without explicitly defining 100 decimal places we get precision errors. This is a workaround because Python allows an arbitrary number of digits for integers
    n = int(s)

    def sum_1_to_n(n):
        return n * (n + 1) // 2

    def calculate_t(n, s):
        if s==0:
            return 0
        minus1 = (n - 1) * sqrt2 // 10**100 # this is equivalent to math.floor((n - 1) * math.sqrt(2)), just with more precision
        if s - minus1 == 2:
            t = (s - 1) * 10**100 // (2 * 10**100 + sqrt2) + 1 if s > 1 else (s - 1) * 10**100 // (2 * 10**100 + sqrt2) # equivalent to math.ceil((s - 1) / (2 + math.sqrt(2))) but more precision
            return t
        minus2 = (n - 2) * sqrt2 // 10**100
        if s - minus2 == 3:
            t = (s - 2) * 10**100 // (2 * 10**100 + sqrt2) + 1 if s > 1 else (s - 1) * 10**100 // (2 * 10**100 + sqrt2)
            return t
        else:
            t = (s - 3) * 10**100 // (2 * 10**100 + sqrt2) + 1 if s > 1 else (s - 1) * 10**100 // (2 * 10**100 + sqrt2)
            return t

    def calculate_sum(n):
        if n == 0:
            return 0
        s = (n * sqrt2) // 10**100
        t = calculate_t(n, s)
        answer = sum_1_to_n(s) - t * (t + 1) - calculate_sum(t)
        return answer
  
    answer = calculate_sum(n)
    return str(answer)
