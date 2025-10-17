"""
    My own implementation of the class BitVector.
    It's is used exactly nowhere in this project.
    Just did it for fun.
"""

class BitVec:
    def __init__(self, bits):
        self.bits = [int(ch) for ch in bits]

    def length(self):
        return len(self.bits)

    def print(self):
        print(self.bits)

    def deepcopy(self):
        return BitVec(self.bits)
    
    def concat(self, other):
        return BitVec(self.bits + other.bits)
    
    def ignore_ith_bit(self, i: int):
        self.bits = [x for j, x in enumerate(self.bits) if (j + 1) % i != 0]

    def permute(self, permute_list: list[int], inplace: bool = True):
        if inplace:
            self.bits = [self.bits[i] for i in permute_list]
        else:
            return [self.bits[i] for i in permute_list]

    def circular_shift_right(self, numof_shifts: int):
        neg_numof_shifts = -1*numof_shifts
        self.bits = self.bits[neg_numof_shifts:] + self.bits[:neg_numof_shifts]
        
    def circular_shift_left(self, numof_shifts: int):
        self.bits = self.bits[numof_shifts:] + self.bits[:numof_shifts] 

    def expand_4to6(self):
        expanded_4bits = ([self.bits[4*i : 4*i+4] + self.bits[4*i+2 : 4*i+4] for i in range(self.length() // 4)])
        self.bits = [bit for expanded_4bit in expanded_4bits for bit in expanded_4bit]

    def pad_from_right(self, new_length: int):
        if new_length < self.length():
            return
        self.bits = self.bits + [0 for _ in range(new_length - self.length())]

    def cut_in_half(self):
        if self.length() % 2:
            raise("Length of input is not divisible by two!")
        half_point = self.length() // 2
        left_half = BitVec(self.bits[:half_point])
        right_half = BitVec(self.bits[half_point:])
        return (left_half, right_half)
    
    def xor(self, other):
        if other.length() != self.length():
            raise("Lists don't have teh same size (xor)")
        self.bits = [self.bits[i] ^ other.bits[i] for i in range(self.length())]
    