import struct, zlib

f = open("w.png", 'wb')

# Opening bytes of PNG
byte_arr = [137, 80, 78, 71, 13, 10, 26, 10]
bin_format = bytearray(byte_arr)
f.write(bin_format)

# IHDR length
header_length_i = 13
header_length_b = header_length_i.to_bytes(4, 'big')
f.write(header_length_b)

# IHDR name
ihdr_name_s = "IHDR"
ihdr_section = ihdr_name_s.encode('ascii')

# PNG Width (4 bytes)
width_i = 3
ihdr_section += width_i.to_bytes(4, 'big')

# PNG Height (4 bytes)
height_i = 3
ihdr_section += height_i.to_bytes(4, 'big')

# Bit depth (1 byte) 8
bit_depth_i = 8
ihdr_section += bit_depth_i.to_bytes(1, 'big')

# Color type (1 byte) 6
color_type_i = 6
ihdr_section += color_type_i.to_bytes(1, 'big')

# Compression (1 byte) 0
compression_i = 0
ihdr_section += compression_i.to_bytes(1, 'big')

# Filter (1 byte) 0
filter_i = 0
ihdr_section += filter_i.to_bytes(1, 'big')

# Interlace (1 byte) 0
interlace_i = 0
ihdr_section += interlace_i.to_bytes(1, 'big')
f.write(ihdr_section)

# IHDR CRC (4 bytes)
ihdr_crc_i = zlib.crc32(ihdr_section)
ihdr_crc_b = ihdr_crc_i.to_bytes(4, 'big')
f.write(ihdr_crc_b)


# IDAT section (data length, IDAT name, data, CRC)
# IDAT data
idat_byte_arr = [0, 80, 130, 255, 255, 0, 0, 0, 255, 80, 130, 255, 255]
idat_byte_arr += [0, 0, 0, 0, 255, 80, 130, 255, 255, 0, 0, 0, 255]
idat_byte_arr += [0, 80, 130, 255, 255, 0, 0, 0, 255, 80, 130, 255, 255]
idat_byte_b = bytearray(idat_byte_arr)
idat_byte_comp = zlib.compress(idat_byte_b)

# IDAT length
data_length_i = len(idat_byte_comp)
data_length_b = data_length_i.to_bytes(4, 'big')
f.write(data_length_b)

# IDAT name
data_name_s = "IDAT"
data_section = data_name_s.encode('ascii')
data_section += idat_byte_comp
f.write(data_section)

# IDAT CRC
idat_crc_i = zlib.crc32(data_section)
idat_crc_b = idat_crc_i.to_bytes(4, 'big')
f.write(idat_crc_b)


# IEND section (data length, IEND name, CRC)
# IEND length
iend_length_i = 0
iend_length_b = iend_length_i.to_bytes(4, 'big')
f.write(iend_length_b)

# IEND name
iend_name_s = "IEND"
iend_name_b = iend_name_s.encode('ascii')
f.write(iend_name_b)

# IEND CRC
iend_crc_i = zlib.crc32(iend_name_b)
iend_crc_b = iend_crc_i.to_bytes(4, 'big')
f.write(iend_crc_b)


f.close()
