### TODO
# Go here for instructions: https://www.w3.org/TR/PNG/
# Look at sect 5.6 "Chunk Ordering" for links to all subs

import struct

f = open("test.png", 'rb')
raw_data = f.read()

print("\n\nRaw PNG data:")
i = 0
while i < 55:
	if i < 8:
		print("Header Byte " + str(i) + ": " + str(raw_data[i]))
		i += 1
	elif i < 9:
		header1_leng = raw_data[i:i+4]
		header1_leng_dc = int.from_bytes(header1_leng, byteorder='big')
		print("Chunk 1 Length: " + str(header1_leng_dc))
		i += 4
	elif i < 13:
		header1_name = raw_data[i:i+4]
		header1_name = header1_name.decode('ascii')
		print("Chunk 1 name: " + header1_name)
		i += 4
	elif i < 17:
		width_leng = raw_data[i:i+4]
		width_leng_dc = int.from_bytes(width_leng, byteorder='big')
		print("Width: " + str(width_leng_dc))
		i += 4
	elif i < 21:
		height_leng = raw_data[i:i+4]
		height_leng_dc = int.from_bytes(height_leng, byteorder='big')
		print("Height: " + str(height_leng_dc))
		i += 4
	elif i < 25:
		print("Bit depth: " + str(raw_data[i]))
		i += 1
	elif i < 26:
		print("Color type: " + str(raw_data[i]))
		i += 1
	elif i < 27:
		print("Compression method: " + str(raw_data[i]))
		i += 1
	elif i < 28:
		print("Filter method: " + str(raw_data[i]))
		i += 1
	elif i < 29:
		print("Interlace method: " + str(raw_data[i]))
		i += 1
	elif i < 30:
		crc1 = raw_data[i:i+4]
		crc1_dc = int.from_bytes(crc1, byteorder='big')
		print("CRC: " + str(crc1_dc))
		i += 4
	elif i < 34:
		header2_leng = raw_data[i:i+4]
		header2_leng_dc = int.from_bytes(header2_leng, byteorder='big')
		print("Chunk 2 Length: " + str(header2_leng_dc))
		i += 4
	elif i < 38:
		header2_name = raw_data[i:i+4]
		header2_name = header2_name.decode('ascii')
		print("Chunk 2 name: " + header2_name)
		i += 4
	elif i < 42:
		gamma_val = raw_data[i:i+4]
		gamma_val_dc = int.from_bytes(gamma_val, byteorder='big')
		print("Gamma value (x10000): " + str(gamma_val_dc))
		i += 4
	elif i < 46:
		crc2 = raw_data[i:i+4]
		crc2_dc = int.from_bytes(crc2, byteorder='big')
		print("CRC: " + str(crc2_dc))
		i += 4
	elif i < 50:
		header3_leng = raw_data[i:i+4]
		header3_leng_dc = int.from_bytes(header3_leng, byteorder='big')
		print("Chunk 3 Length: " + str(header3_leng_dc))
		i += 4
	elif i < 54:
		header3_name = raw_data[i:i+4]
		header3_name = header3_name.decode('ascii')
		print("Chunk 3 name: " + header3_name)
		i += 4
	else:
		print("Byte " + str(i) + ": " + str(raw_data[i]))
		i += 1


idat_index = raw_data.find(b"IDAT")
idat_info = True
if idat_info:
	print("\n" + "Chunk loc: " + str(idat_index))
	print("Chunk name: " + str(raw_data[idat_index:idat_index + 4]))
	print("Chunk size: " + str(int.from_bytes(raw_data[idat_index - 4:idat_index], byteorder='big')))
	print("Length of all data: " + str(len(raw_data)))
	print("Start of IDAT: " + str(idat_index))
	print("End of IDAT: " + str(raw_data.find(b"IEND")))

i = idat_index + 4
while i < idat_index + 60:
	print("Sample " + str(i) + ": " + str(raw_data[i]) + " " + str(raw_data[i + 1]) + " " + str(raw_data[i + 2]))
	i += 3

print("\n\n")
print(raw_data)
