#!/usr/bin/env python3

string = 'F4X67ENQPK0{MTJRHL}O3G59UB-ZAWV8S2YI1CD'
indices = [26,25,38,10,6,35,6,12,13,2,14,17,27,38,18,29,23,23,27,30,2,33,27,26,11,16,37,7,22,19]

solution = ''
for i in indices:
    # indices start at 1 on the TI-84
    solution += string[i-1]
print(f'Solution: {solution}')
