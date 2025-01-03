from BitVector import BitVector
import sys
[a, b, c, d, e, f, g, h] = ['6a09e667f3bcc908', 'bb67ae8584caa73b', 
                            '3c6ef372fe94f82b', 'a54ff53a5f1d36f1', 
                            '510e527fade682d1', '9b05688c2b3e6c1f', 
                            '1f83d9abfb41bd6b', '5be0cd19137e2179']

K = ['428a2f98d728ae22', '7137449123ef65cd', 'b5c0fbcfec4d3b2f', 'e9b5dba58189dbbc',
    '3956c25bf348b538', '59f111f1b605d019', '923f82a4af194f9b', 'ab1c5ed5da6d8118',
    'd807aa98a3030242', '12835b0145706fbe', '243185be4ee4b28c', '550c7dc3d5ffb4e2',
    '72be5d74f27b896f', '80deb1fe3b1696b1', '9bdc06a725c71235', 'c19bf174cf692694',
    'e49b69c19ef14ad2', 'efbe4786384f25e3', '0fc19dc68b8cd5b5', '240ca1cc77ac9c65',
    '2de92c6f592b0275', '4a7484aa6ea6e483', '5cb0a9dcbd41fbd4', '76f988da831153b5',
    '983e5152ee66dfab', 'a831c66d2db43210', 'b00327c898fb213f', 'bf597fc7beef0ee4',
    'c6e00bf33da88fc2', 'd5a79147930aa725', '06ca6351e003826f', '142929670a0e6e70',
    '27b70a8546d22ffc', '2e1b21385c26c926', '4d2c6dfc5ac42aed', '53380d139d95b3df',
    '650a73548baf63de', '766a0abb3c77b2a8', '81c2c92e47edaee6', '92722c851482353b',
    'a2bfe8a14cf10364', 'a81a664bbc423001', 'c24b8b70d0f89791', 'c76c51a30654be30',
    'd192e819d6ef5218', 'd69906245565a910', 'f40e35855771202a', '106aa07032bbd1b8',
    '19a4c116b8d2d0c8', '1e376c085141ab53', '2748774cdf8eeb99', '34b0bcb5e19b48a8',
    '391c0cb3c5c95a63', '4ed8aa4ae3418acb', '5b9cca4f7763e373', '682e6ff3d6b2b8a3',
    '748f82ee5defb2fc', '78a5636f43172f60', '84c87814a1f0ab72', '8cc702081a6439ec',
    '90befffa23631e28', 'a4506cebde82bde9', 'bef9a3f7b2c67915', 'c67178f2e372532b',
    'ca273eceea26619c', 'd186b8c721c0c207', 'eada7dd6cde0eb1e', 'f57d4f7fee6ed178',
    '06f067aa72176fba', '0a637dc5a2c898a6', '113f9804bef90dae', '1b710b35131c471b',
    '28db77f523047d84', '32caab7b40c72493', '3c9ebe0a15c9bebc', '431d67c49c100d4c',
    '4cc5d4becb3e42b6', '597f299cfc657e2a', '5fcb6fab3ad6faec', '6c44198c4a475817']
                                

class SHA512():
    def __init__(self) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h

    def sha512 (self, plaintext, ciphertext) -> None:
        bva = BitVector(hexstring=self.a)
        bvb = BitVector(hexstring=self.b)
        bvc = BitVector(hexstring=self.c)
        bvd = BitVector(hexstring=self.d)
        bve = BitVector(hexstring=self.e)
        bvf = BitVector(hexstring=self.f)
        bvg = BitVector(hexstring=self.g)
        bvh = BitVector(hexstring=self.h)

        bvk = [BitVector(hexstring = k) for k in K]

        # print (bva.get_bitvector_in_hex())  

        with open (plaintext, 'r') as file:
            text = file.read()

        bv = BitVector(textstring = text)
        length = bv.length()
        bv2 = bv + BitVector(bitstring="1")
        bv2.pad_from_right((1024 - (bv2.length() + 128)) % 1024)
        bv3 = BitVector(intVal = length, size = 128)
        bv4 = bv2 + bv3
                   
        words = [None] * 80
        
        for i in range (0, bv4.length(), 1024):
            block = bv4[i:i+1024]
            

            words[0:16] = [block[i:i+64] for i in range(0, 1024, 64)]

            for i in range(16, 80):
                i_minus_2_word = words[i-2]
                i_minus_15_word = words[i-15]

                s0 = i_minus_15_word.deep_copy() >> 1 ^ i_minus_15_word.deep_copy() >> 8 ^ i_minus_15_word.deep_copy().shift_right(7)
                s1 = i_minus_2_word.deep_copy() >> 19 ^ i_minus_2_word.deep_copy() >> 61 ^ i_minus_2_word.deep_copy().shift_right(6)
            
                words[i] = BitVector (intVal = (int(words[i-16]) + int(s0) + int(words[i-7]) + int(s1)) % (2**64), size = 64)
            
            h0, h1, h2, h3, h4, h5, h6, h7 = bva, bvb, bvc, bvd, bve, bvf, bvg, bvh
            
            for i in range (80):
                # ch = (bve & bvf) ^ (~bve & bvg)
                ch = (h4 & h5) ^ (~h4 & h6)
                # maj = (bva & bvb) ^ (bva & bvc) ^ (bvb & bvc)
                maj = (h0 & h1) ^ (h0 & h2) ^ (h1 & h2)
                sum_a = h0.deep_copy() >> 28 ^ h0.deep_copy() >> 34 ^ h0.deep_copy() >> 39
                sum_e = h4.deep_copy() >> 14 ^ h4.deep_copy() >> 18 ^ h4.deep_copy() >> 41
            
                # t1 = BitVector(intVal=((int(h, 16) + int(ch, 16) + int(sum_e, 16) + int(words[i], 16) + int(bvk[i], 16)) % (2**64)), size=64)
                t1 = BitVector(intVal=((h7.intValue() + int(ch) + int(sum_e) + int(words[i]) + int(bvk[i])) % (2**64)), size=64)
                t2 = BitVector(intVal=(int(sum_a) + int(maj)) % (2**64), size=64)

                h7 = h6
                h6 = h5
                h5 = h4
                h4 = BitVector (intVal = ((int(h3) + int(t1)) % (2**64)), size = 64)
                h3 = h2
                h2 = h1
                h1 = h0
                h0 = BitVector (intVal = ((int(t1) + int(t2)) % (2**64)), size = 64)
            
            bva = BitVector(intVal=(h0.intValue() + int(bva)) % (2**64), size=64)
            bvb = BitVector(intVal=(h1.intValue() + int(bvb)) % (2**64), size=64)
            bvc = BitVector(intVal=(h2.intValue() + int(bvc)) % (2**64), size=64)
            bvd = BitVector(intVal=(h3.intValue() + int(bvd)) % (2**64), size=64)
            bve = BitVector(intVal=(h4.intValue() + int(bve)) % (2**64), size=64)
            bvf = BitVector(intVal=(h5.intValue() + int(bvf)) % (2**64), size=64)
            bvg = BitVector(intVal=(h6.intValue() + int(bvg)) % (2**64), size=64)
            bvh = BitVector(intVal=(h7.intValue() + int(bvh)) % (2**64), size=64)

        final = bva + bvb + bvc + bvd + bve + bvf + bvg + bvh

        with open(ciphertext, 'a') as file:
            file.write(final.get_bitvector_in_hex())

if __name__ == "__main__": 
    cipher = SHA512()
    cipher.sha512(plaintext=sys.argv[1], ciphertext=sys. argv[2])