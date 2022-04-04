import struct

f = open("test.png", 'rb')
raw_data = f.read()

print("\n\nRaw PNG data:")
i = 0
while i < 30:
	if i < 8:
		print("Header Byte " + str(i) + ": " + str(raw_data[i]))
		i += 1
	elif i < 9:
		header1_leng = raw_data[i:i+4]
		header1_leng_dc = int.from_bytes(header1_leng, byteorder='big')
		print("Length: " + str(header1_leng_dc))
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
		chunk2_leng = raw_data[i:i+4]
		chunk2_leng_dc = int.from_bytes(chunk2_leng, byteorder='big')
		print("Chunk 2 Length: " + str(chunk2_leng_dc))
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
