import deflate

b64charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
base64_alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
source_relations = {"Zero or One": "|o", "Exactly One": "||", "Zero or Many": "}o", "One or Many": "}|"}
target_relations = {"Zero or One": "o|", "Exactly One": "||", "Zero or Many": "o{", "One or Many": "|{"}

def encode_plant_uml(diagram):
    data = diagram.encode()
    level = 6
    compressed = deflate.deflate_compress(data, level)

    chunks_8bit = ''.join([format(bits,'08b') for bits in compressed])

    chunks_6bit = [chunks_8bit[bits:bits+6] for bits in range(0,len(chunks_8bit),6)]
    padding_amount = ( 6 - len(chunks_6bit[len(chunks_6bit)-1]) )
    chunks_6bit[len(chunks_6bit)-1] += padding_amount * '0'


    encoded = ''.join([base64_alphabet[int(bits,2)] for bits in chunks_6bit])
    encoded += int(padding_amount/2) * '='

    return encoded

def create_uml_diagram(data):
    uml = '@startuml\n'
    for ent in data['entities']:
        uml += 'entity ' + ent['name'] + '{\n'
        uml += '* ' + ent['name'] + 'ID: number <<generated>>\n--\n'
        for attr in ent['attributes']:
            if('id' in attr['name'].lower()): continue
            uml += '* ' + attr['name'] + ': ' + attr['type'] + '\n'
        uml += '}\n\n'
    
    for rel in data['relations']:
        uml += rel['source'] + ' ' + source_relations[rel['cardinality_of_source']] + '--' + target_relations[rel['cardinality_of_target']] + rel['target'] + '\n'
    
    uml += '@enduml'
    return encode_plant_uml(uml)

def create_mermaid_diagram(data):
    merm = 'erDiagram\n'
    for ent in data['entities']:
        merm += ent['name'] + '{\n'
        merm += 'int ' + ent['name'] + 'ID PK\n'
        for attr in ent['attributes']:
            if('id' in attr['name'].lower()): continue
            merm += attr['type'] + ' ' + attr['name'] + '\n'
        merm += '}\n\n'
    
    for rel in data['relations']:
        merm += rel['source'] + ' ' + source_relations[rel['cardinality_of_source']] + '--' + target_relations[rel['cardinality_of_target']] + rel['target'] + ': ' + rel['name'] + '\n'
    
    return merm