### TODO
# Go here for instructions: https://www.w3.org/TR/PNG/
# Look at sect 5.6 "Chunk Ordering" for links to all subs

import struct

f = open("test.png", 'rb')
raw_data = f.read()

print("\n\nRaw PNG data:")
i = 0
while i < 749:
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
		print("CRC 1: " + str(crc1_dc))
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
		print("CRC 2: " + str(crc2_dc))
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
	elif i < 58:
		white_x = raw_data[i:i+4]
		white_x_dc = int.from_bytes(white_x, byteorder='big')
		print("White X: " + str(white_x_dc))
		i += 4
	elif i < 62:
		white_y = raw_data[i:i+4]
		white_y_dc = int.from_bytes(white_y, byteorder='big')
		print("White Y: " + str(white_y_dc))
		i += 4
	elif i < 66:
		red_x = raw_data[i:i+4]
		red_x_dc = int.from_bytes(red_x, byteorder='big')
		print("Red X: " + str(red_x_dc))
		i += 4
	elif i < 70:
		red_y = raw_data[i:i+4]
		red_y_dc = int.from_bytes(red_y, byteorder='big')
		print("Red Y: " + str(red_y_dc))
		i += 4
	elif i < 74:
		green_x = raw_data[i:i+4]
		green_x_dc = int.from_bytes(green_x, byteorder='big')
		print("Green X: " + str(green_x_dc))
		i += 4
	elif i < 78:
		green_y = raw_data[i:i+4]
		green_y_dc = int.from_bytes(green_y, byteorder='big')
		print("Green Y: " + str(green_y_dc))
		i += 4
	elif i < 82:
		blue_x = raw_data[i:i+4]
		blue_x_dc = int.from_bytes(blue_x, byteorder='big')
		print("Blue X: " + str(blue_x_dc))
		i += 4
	elif i < 86:
		blue_y = raw_data[i:i+4]
		blue_y_dc = int.from_bytes(blue_y, byteorder='big')
		print("Blue Y: " + str(blue_y_dc))
		i += 4
	elif i < 90:
		crc3 = raw_data[i:i+4]
		crc3_dc = int.from_bytes(crc3, byteorder='big')
		print("CRC 3: " + str(crc3_dc))
		i += 4
	elif i < 94:
		header4_leng = raw_data[i:i+4]
		header4_leng_dc = int.from_bytes(header4_leng, byteorder='big')
		print("Chunk 4 Length: " + str(header4_leng_dc))
		i += 4
	elif i < 98:
		header4_name = raw_data[i:i+4]
		header4_name = header4_name.decode('ascii')
		print("Chunk 4 name: " + header4_name)
		i += 4
	elif i < 166:
		exif_data = raw_data[i:i+68]
		#exif_data = exif_data.decode('ascii')
		print("eXIf data: " + str(exif_data))
		i += 68
	elif i < 170:
		crc4 = raw_data[i:i+4]
		crc4_dc = int.from_bytes(crc4, byteorder='big')
		print("CRC 4: " + str(crc4_dc))
		i += 4
	elif i < 174:
		header5_leng = raw_data[i:i+4]
		header5_leng_dc = int.from_bytes(header5_leng, byteorder='big')
		print("Chunk 5 Length: " + str(header5_leng_dc))
		i += 4
	elif i < 178:
		header5_name = raw_data[i:i+4]
		header5_name = header5_name.decode('ascii')
		print("Chunk 5 name: " + header5_name)
		i += 4
	elif i < 736:
		itxt_data = raw_data[i:i+558]
		itxt_data = itxt_data.decode('ascii')
		print("iTXt data: " + itxt_data)
		i += 558
	elif i < 740:
		crc5 = raw_data[i:i+4]
		crc5_dc = int.from_bytes(crc5, byteorder='big')
		print("CRC 5: " + str(crc5_dc))
		i += 4
	elif i < 744:
		header6_leng = raw_data[i:i+4]
		header6_leng_dc = int.from_bytes(header6_leng, byteorder='big')
		print("Chunk 6 Length: " + str(header6_leng_dc))
		i += 4
	elif i < 748:
		header6_name = raw_data[i:i+4]
		header6_name = header6_name.decode('ascii')
		print("Chunk 6 name: " + header6_name)
		i += 4
	else:
		print("Byte " + str(i) + ": " + str(raw_data[i]))
		i += 1


idat_index = raw_data.find(b"IDAT")
idat_info = False
if idat_info:
	print("\n" + "Chunk loc: " + str(idat_index))
	print("Chunk name: " + str(raw_data[idat_index:idat_index + 4]))
	print("Chunk size: " + str(int.from_bytes(raw_data[idat_index - 4:idat_index], byteorder='big')))
	print("Length of all data: " + str(len(raw_data)))
	print("Start of IDAT: " + str(idat_index))
	print("End of IDAT: " + str(raw_data.find(b"IEND")))

#i = idat_index + 4
#while i < idat_index + 60:
#	print("Sample " + str(i) + ": " + str(raw_data[i]) + " " + str(raw_data[i + 1]) + " " + str(raw_data[i + 2]))
#	i += 3

print("\n\n")
#print(raw_data)
