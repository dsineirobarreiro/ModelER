import deflate
import base64

diagram = """
@startuml
participant Bob [[http://plantuml.com]]
Bob -> Alice : [[http://forum.plantuml.net]] hello
@enduml
"""
b64charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
base64_alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

data = diagram.encode()
level = 6
compressed = deflate.deflate_compress(data, level)

chunks_8bit = ''.join([format(bits,'08b') for bits in compressed])

chunks_6bit = [chunks_8bit[bits:bits+6] for bits in range(0,len(chunks_8bit),6)]
padding_amount = ( 6 - len(chunks_6bit[len(chunks_6bit)-1]) )
chunks_6bit[len(chunks_6bit)-1] += padding_amount * '0'


encoded = ''.join([base64_alphabet[int(bits,2)] for bits in chunks_6bit])
encoded += int(padding_amount/2) * '='
print('Base64 encoded version of {to_encode} is: {result}'.format(to_encode = diagram, result = encoded))
