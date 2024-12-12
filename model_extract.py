import struct
import numpy as np

# run command :         python "model_extract.py"

target_file = "C:\\Users\\Joe bingle\\Downloads\\boardguard_testing\\.godot\\imported\\pawn.obj-67e0359734749799be1fd610501e780d.mesh"

output_file = "C:\\Users\\Joe bingle\\Downloads\\test\\output.obj"


def little_endian_4(f):
    return struct.unpack_from("<i",f.read(4))[0]


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
    vert_buffer = None
    vert_count = 0
    index_buffer = None
    index_count = 0
    is_weird_vertex = False
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
        
        # process junk 
        f.read(8)
        read_delimited_string(f)

        f.read(8)
        if read_delimited_string(f) != "ArrayMesh":
            print("not the right format!!!")
            return
        f.read(0x14)

        component_count = little_endian_4(f)
        for i in range(component_count):
            unk_0000_0005 = little_endian_4(f)
            match read_delimited_string(f):
                case "format":
                    is_weird_vertex = ((f.read(12)[7] & 32) != 0)
                case "primitive":
                    f.read(8)
                case "vertex_data":
                    vert_format = little_endian_4(f)
                    vert_buffer_size = little_endian_4(f)
                    vert_buffer = f.read(vert_buffer_size) # 19040 = 1586 verts
                case "vertex_count":
                    f.read(4)
                    vert_count = little_endian_4(f) # 952
                case "attribute_data": # codeword for UV? or just unnamed data buffer block?
                    attribute_format = little_endian_4(f)
                    attribute_buffer_size = little_endian_4(f)
                    f.read(attribute_buffer_size) # 7616 = 1269
                case "aabb":
                    f.read(28)
                case "uv_scale":
                    f.read(20)
                case "index_data":
                    index_format = little_endian_4(f)
                    index_buffer_size = little_endian_4(f)
                    index_buffer = f.read(index_buffer_size) # 7632 = 954 triangles
                case "index_count":
                    f.read(4)
                    index_count = little_endian_4(f) # 3816
                case "name":
                    count3 = little_endian_4(f)
                    name = read_delimited_string(f)

    # now convert to obj file
    with open(output_file, 'w') as file:
        file.write('o Cube\n')

        #vert_count = len(vert_buffer) / 12
        for i in range(vert_count):
            if is_weird_vertex == False:
                vert_offset = i * 12
                vert = struct.unpack_from("fff",vert_buffer[vert_offset:vert_offset+12])
                file.write('v '+ str(vert[0]) +' '+ str(vert[1]) +' '+ str(vert[2]) +'\n')
            else:
                # documentation says: 
                #
                # Flag used to mark that a mesh is using compressed attributes (vertices, normals, tangents, UVs). 
                # When this form of compression is enabled, vertex positions will be packed into an RGBA16UNORM attribute and scaled in the vertex shader. 
                # The normal and tangent will be packed into an RG16UNORM representing an axis, and a 16-bit float stored in the A-channel of the vertex. 
                # UVs will use 16-bit normalized floats instead of full 32-bit signed floats. 
                # When using this compression mode you must use either vertices, normals, and tangents or only vertices. 
                # You cannot use normals without tangents. Importers will automatically enable this compression if they can.

                # godot's code implies that each thingo of vertices should be 8 bytes long, opposed to the 12 bytes of uncompressed vertex buffer stride thing
                vert_offset = (i * 8) # + 2
                test2 = vert_buffer[vert_offset:vert_offset+8]

                vert = struct.unpack_from("HHH",test2)
                file.write('v '+ str(vert[0]/0xffff) +' '+ str(vert[1]/0xffff) +' '+ str(vert[2]/0xffff) +'\n')


        file.write('s 0\n')

        #tri_count = len(index_buffer) / 6
        for i in range(index_count//3):
            tri_offset = i * 6
            index = struct.unpack_from("hhh",index_buffer[tri_offset:tri_offset+6])
            file.write('f '+ str(index[0]+1) +' '+ str(index[1]+1) +' '+ str(index[2]+1) +'\n')


        


doody_mode()