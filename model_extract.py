import struct


target_file = "C:\\Users\\Joe bingle\\Downloads\\boardguard_testing\\.godot\\imported\\ritual_stone.obj-30f9aba14dfd620040c6c19d3935ab3d.mesh"



def little_endian_4(f):
    return struct.unpack_from("<4",f.read(4))

def read_string(f):
    output = ""
    while True:
        byte = f.read(1)[0]
        if byte == 0 or not byte: 
            break   
        output += chr(byte)
    return output

def read_delimited_string(f):
    length = little_endian_4(f)
    byte = f.read(length)
    output = ""
    for i in range(length):
        if byte[i] == 0: 
            continue
        output += chr(byte[i])
    return output



def doody_mode(): 
    with open(target_file, "rb") as f:
        # read all the filler junk
        f.read(0x18)
        # check to make sure the file is this format
        if read_delimited_string(f) != "ArrayMesh":
            print("not the right format!!!")
            return
        # skip more junk
        f.read(0x40)

        # process the labels
        label_count = little_endian_4(f)
        for i in range(label_count):
            label = read_delimited_string(f)
            
        f.read(8)
        if read_delimited_string(f) != "ArrayMesh":
            print("not the right format!!!")
            return
        f.read(0x14)

        component_count = little_endian_4(f)
        for i in range(component_count):
            unk_0000_0005 = little_endian_4(f)
            label = read_delimited_string(f)
            match label:
                case "format":
                    f.read(12)
                case "primitive":
                    f.read(8)
                case "vertex_data":
                    vert_format = little_endian_4(f)
                    vert_buffer_size = little_endian_4(f)
                    f.read(vert_buffer_size)
                case "vertex_count":
                    f.read(8)
                case "attribute_data": # codeword for UV? or just unnamed data buffer block?
                    attribute_format = little_endian_4(f)
                    attribute_buffer_size = little_endian_4(f)
                    f.read(attribute_buffer_size)
                case "aabb":
                    f.read(28)
                case "uv_scale":
                    f.read(20)
                case "index_data":
                    index_format = little_endian_4(f)
                    index_buffer_size = little_endian_4(f)
                    f.read(index_buffer_size)
                case "index_count":
                    f.read(8)
                case "name":
                    f.read(12)
                    count3 = little_endian_4(f)
                    name = read_delimited_string(f)

        # now convert to obj file

        


        


doody_mode()