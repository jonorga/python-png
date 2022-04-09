### TODO
# Go here for instructions: https://www.w3.org/TR/PNG/
# Look at sect 5.6 "Chunk Ordering" for links to all subs
# Add the other filter methods
# Add zlib CRC stuff: https://www.geeksforgeeks.org/zlib-crc32-in-python/

import struct, zlib

f = open("test.png", 'rb')
raw_data = f.read()

red_arr = []
green_arr = []
blue_arr = []
alpha_arr = []

print("\n\nRaw PNG data:")
i = 0
while i < 813:
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
		width = width_leng_dc
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
		print("CRC minus length: " + str(zlib.crc32(raw_data[12:29])))
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
		if crc2_dc == zlib.crc32(raw_data[37:45]):
			print("CRC 2: " + str(crc2_dc) + "(OK)")
		else:
			print("CRC 2: " + str(crc2_dc) + "(ERROR)")
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
	elif i < 796:
		compressed_idat = raw_data[i:i+48]
		decompressed_idat = zlib.decompress(compressed_idat)
		print("Decomped length: " + str(len(decompressed_idat)))
		# First byte is a filter for the row
		# Ref: https://stackoverflow.com/questions/49017937/png-decompressed-idat-chunk-how-to-read
		# If the next few rows are filtered, you will need to unfilter them
		# Filter methods: https://www.w3.org/TR/PNG/#9FtIntro
		j = 0
		col = 0
		filter_method = -1
		cur_pixel = 0
		while j < 124:
			if col == 0:
				if decompressed_idat[j] == 0:
					print("Filter method: None (0)")
				elif decompressed_idat[j] == 1:
					print("Filter method: Sub (1)")
				elif decompressed_idat[j] == 2:
					print("Filter method: Up (2)")
				elif decompressed_idat[j] == 3:
					print("Filter method: Average (3)")
				elif decompressed_idat[j] == 4:
					print("Filter method: Paeth (4)")
				filter_method = decompressed_idat[j]
				j += 1
			if filter_method == 0:
				red_arr.append(decompressed_idat[j])
				green_arr.append(decompressed_idat[j+1])
				blue_arr.append(decompressed_idat[j+2])
				alpha_arr.append(decompressed_idat[j+3])
				print("Recon Pixel " + str(cur_pixel) + ": " + str(red_arr[cur_pixel]) + " " + str(green_arr[cur_pixel]) + " " + str(blue_arr[cur_pixel]) + " " + str(alpha_arr[cur_pixel]))
			elif filter_method == 2:
				if decompressed_idat[j] + red_arr[cur_pixel - width] < 256:
					red_arr.append(decompressed_idat[j] + red_arr[cur_pixel - width])
				else:
					red_arr.append(decompressed_idat[j] + red_arr[cur_pixel - width] - 256)
				if decompressed_idat[j+1] + green_arr[cur_pixel - width] < 256:
					green_arr.append(decompressed_idat[j+1] + green_arr[cur_pixel - width])
				else:
					green_arr.append(decompressed_idat[j+1] + green_arr[cur_pixel - width] - 256)
				if decompressed_idat[j+2] + blue_arr[cur_pixel - width] < 256:
					blue_arr.append(decompressed_idat[j+2] + blue_arr[cur_pixel - width])
				else:
					blue_arr.append(decompressed_idat[j+2] + blue_arr[cur_pixel - width] - 256)
				if decompressed_idat[j+3] + alpha_arr[cur_pixel - width] < 256:
					alpha_arr.append(decompressed_idat[j+3] + alpha_arr[cur_pixel - width])
				else:
					alpha_arr.append(decompressed_idat[j+3] + alpha_arr[cur_pixel - width] - 256)
				print("Recon Pixel " + str(cur_pixel) + ": " + str(red_arr[cur_pixel]) + " " + str(green_arr[cur_pixel]) + " " + str(blue_arr[cur_pixel]) + " " + str(alpha_arr[cur_pixel]))
			elif filter_method == 4:
				pix_a = red_arr[cur_pixel - 1]
				pix_b = red_arr[cur_pixel - width]
				pix_c = red_arr[cur_pixel - width - 1]
				paeth = pix_a + pix_b - pix_c
				paeth_a = abs(paeth - pix_a)
				paeth_b = abs(paeth - pix_b)
				paeth_c = abs(paeth - pix_c)
				if paeth_a <= paeth_b and paeth_a <= paeth_c:
					paeth_r = pix_a
				elif paeth_b <= paeth_c:
					paeth_r = pix_b
				else:
					paeth_r = pix_c
				if decompressed_idat[j] + paeth_r < 256:
					red_arr.append(decompressed_idat[j] + paeth_r)
				else:
					red_arr.append(decompressed_idat[j] + paeth_r - 256)

				pix_a = green_arr[cur_pixel - 1]
				pix_b = green_arr[cur_pixel - width]
				pix_c = green_arr[cur_pixel - width - 1]
				paeth = pix_a + pix_b - pix_c
				paeth_a = abs(paeth - pix_a)
				paeth_b = abs(paeth - pix_b)
				paeth_c = abs(paeth - pix_c)
				if paeth_a <= paeth_b and paeth_a <= paeth_c:
					paeth_r = pix_a
				elif paeth_b <= paeth_c:
					paeth_r = pix_b
				else:
					paeth_r = pix_c
				if decompressed_idat[j+1] + paeth_r < 256:
					green_arr.append(decompressed_idat[j+1] + paeth_r)
				else:
					green_arr.append(decompressed_idat[j+1] + paeth_r - 256)

				pix_a = blue_arr[cur_pixel - 1]
				pix_b = blue_arr[cur_pixel - width]
				pix_c = blue_arr[cur_pixel - width - 1]
				paeth = pix_a + pix_b - pix_c
				paeth_a = abs(paeth - pix_a)
				paeth_b = abs(paeth - pix_b)
				paeth_c = abs(paeth - pix_c)
				if paeth_a <= paeth_b and paeth_a <= paeth_c:
					paeth_r = pix_a
				elif paeth_b <= paeth_c:
					paeth_r = pix_b
				else:
					paeth_r = pix_c
				if decompressed_idat[j+2] + paeth_r < 256:
					blue_arr.append(decompressed_idat[j+2] + paeth_r)
				else:
					blue_arr.append(decompressed_idat[j+2] + paeth_r - 256)

				pix_a = alpha_arr[cur_pixel - 1]
				pix_b = alpha_arr[cur_pixel - width]
				pix_c = alpha_arr[cur_pixel - width - 1]
				paeth = pix_a + pix_b - pix_c
				paeth_a = abs(paeth - pix_a)
				paeth_b = abs(paeth - pix_b)
				paeth_c = abs(paeth - pix_c)
				if paeth_a <= paeth_b and paeth_a <= paeth_c:
					paeth_r = pix_a
				elif paeth_b <= paeth_c:
					paeth_r = pix_b
				else:
					paeth_r = pix_c
				if decompressed_idat[j+3] + paeth_r < 256:
					alpha_arr.append(decompressed_idat[j+3] + paeth_r)
				else:
					alpha_arr.append(decompressed_idat[j+3] + paeth_r - 256)

				print("Recon Pixel " + str(cur_pixel) + ": " + str(red_arr[cur_pixel]) + " " + str(green_arr[cur_pixel]) + " " + str(blue_arr[cur_pixel]) + " " + str(alpha_arr[cur_pixel]))
			else:
				print("Filtered Pixel " + str(cur_pixel) + ": " + str(decompressed_idat[j]) + " " + str(decompressed_idat[j+1]) + " " + str(decompressed_idat[j+2]) + " " + str(decompressed_idat[j+3]))
			j += 4
			cur_pixel += 1
			if col == 5:
				col = 0
			else:
				col += 1
		i += 48
	elif i < 800:
		crc5 = raw_data[i:i+4]
		crc5_dc = int.from_bytes(crc5, byteorder='big')
		print("CRC 5: " + str(crc5_dc))
		i += 4
	elif i < 804:
		header7_leng = raw_data[i:i+4]
		header7_leng_dc = int.from_bytes(header7_leng, byteorder='big')
		print("Chunk 7 Length: " + str(header7_leng_dc))
		i += 4
	elif i < 808:
		header7_name_b = raw_data[i:i+4]
		header7_name_s = header7_name_b.decode('ascii')
		print("Chunk 7 name: " + header7_name_s)
		i += 4
	elif i < 812:
		crc7 = raw_data[i:i+4]
		crc7_dc = int.from_bytes(crc7, byteorder='big')
		if crc7_dc == zlib.crc32(header7_name_b):
			print("CRC 7: " + str(crc7_dc) + " (OK)")
		else:
			print("CRC 7: " + str(crc7_dc) + " (ERROR)")
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
#	print("Sample " + str(i) + ": " + str(raw_data[i]) + " " + str(raw_data[i + 1]) + " " + str(raw_data[i + 2]) + " " + str(raw_data[i + 3]))
#	i += 4

print("\n\n")
#print(raw_data)
