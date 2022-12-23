import struct, zlib, math, sys

class png_obj:
	def __init__(self, png_file):
		# Read file

		self.file_name = png_file
		f = open(png_file, 'rb')
		self.raw_data = f.read()

		# Check first 8 bytes for PNG header
		header_arr = self.raw_data[0:8]
		header_int_arr = bytes([137, 80, 78, 71, 13, 10, 26, 10])
		header_byte_arr = bytearray(header_int_arr)
		if header_arr != header_int_arr:
			raise Exception("PNG Object can only read PNGs. Header bytes mismatch")

		# IHDR Length/header
		IHDR_leng_raw = self.raw_data[8:12]
		IHDR_leng_dc = int.from_bytes(IHDR_leng_raw, byteorder='big')

		IHDR_name_raw = self.raw_data[12:16]
		IHDR_name_dc = IHDR_name_raw.decode('ascii')

		# IHDR values
		width_raw = self.raw_data[16:20]
		self.width_dc = int.from_bytes(width_raw, byteorder='big')

		height_raw = self.raw_data[20:24]
		self.height_dc = int.from_bytes(height_raw, byteorder='big')

		self.bit_depth = self.raw_data[24]
		self.color_type = self.raw_data[25]
		self.compression_method = self.raw_data[26]
		self.filter_method = self.raw_data[27]
		self.interlace = self.raw_data[28]

		# Read all other chunks
		i = 33
		self.chunks_in_file = ["IHDR"]
		self.red_arr = []
		self.green_arr = []
		self.blue_arr = []
		self.alpha_arr = []

		while i < len(self.raw_data):
			chunk_length_raw = self.raw_data[i:i+4]
			chunk_length_dc = int.from_bytes(chunk_length_raw, byteorder='big')
			i += 4
			chunk_name_raw = self.raw_data[i:i+4]
			chunk_name_dc = chunk_name_raw.decode('ascii')

			self.chunks_in_file.append(chunk_name_dc)

			# IDAT Section
			if chunk_name_dc == "IDAT":
				compressed_idat = self.raw_data[i+4:i+4+chunk_length_dc]
				idat_data = zlib.decompress(compressed_idat)
				j = 0
				column = 0
				cur_filter = -1
				cur_pixel = 0
				first_line = True
				progress = len(idat_data)


				# TODO write something to deal with various bit depths


				# TODO write something to deal with interlace type 1


				# TODO write section to hand color types:
					# Greyscale (0)
					# Truecolour (2)
					# Indexed-colour (3)
					# Greyscale with alpha (4)


				if self.color_type == 6:
					while j < len(idat_data):
						perc = format((j / progress)*100, '.2f')
						print("Reading image... " + str(perc) + "%", end="\r")
						if column == 0:
							cur_filter = idat_data[j]
							j += 1
						if cur_filter == 0:
							self.red_arr.append(idat_data[j])
							self.green_arr.append(idat_data[j+1])
							self.blue_arr.append(idat_data[j+2])
							self.alpha_arr.append(idat_data[j+3])
						elif cur_filter == 1 and len(self.red_arr) != 0:
							if idat_data[j] + self.red_arr[cur_pixel - 1] < 256:
								self.red_arr.append(idat_data[j] + self.red_arr[cur_pixel - 1])
							else:
								self.red_arr.append(idat_data[j] + self.red_arr[cur_pixel - 1] - 256)
							if idat_data[j+1] + self.green_arr[cur_pixel - 1] < 256:
								self.green_arr.append(idat_data[j+1] + self.green_arr[cur_pixel - 1])
							else:
								self.green_arr.append(idat_data[j+1] + self.green_arr[cur_pixel - 1] - 256)
							if idat_data[j+2] + self.blue_arr[cur_pixel - 1] < 256:
								self.blue_arr.append(idat_data[j+2] + self.blue_arr[cur_pixel - 1])
							else:
								self.blue_arr.append(idat_data[j+2] + self.blue_arr[cur_pixel - 1] - 256)
							if idat_data[j+3] + self.alpha_arr[cur_pixel - 1] < 256:
								self.alpha_arr.append(idat_data[j+3] + self.alpha_arr[cur_pixel - 1])
							else:
								self.alpha_arr.append(idat_data[j+3] + self.alpha_arr[cur_pixel - 1] - 256)
						elif cur_filter == 1 and len(self.red_arr) == 0:
							self.red_arr.append(idat_data[j])
							self.green_arr.append(idat_data[j+1])
							self.blue_arr.append(idat_data[j+2])
							self.alpha_arr.append(idat_data[j+3])
						elif cur_filter == 2 and not first_line:
							if idat_data[j] + self.red_arr[cur_pixel - self.width_dc] < 256:
								self.red_arr.append(idat_data[j] + self.red_arr[cur_pixel - self.width_dc])
							else:
								self.red_arr.append(idat_data[j] + self.red_arr[cur_pixel - self.width_dc] - 256)
							if idat_data[j+1] + self.green_arr[cur_pixel - self.width_dc] < 256:
								self.green_arr.append(idat_data[j+1] + self.green_arr[cur_pixel - self.width_dc])
							else:
								self.green_arr.append(idat_data[j+1] + self.green_arr[cur_pixel - self.width_dc] - 256)
							if idat_data[j+2] + self.blue_arr[cur_pixel - self.width_dc] < 256:
								self.blue_arr.append(idat_data[j+2] + self.blue_arr[cur_pixel - self.width_dc])
							else:
								self.blue_arr.append(idat_data[j+2] + self.blue_arr[cur_pixel - self.width_dc] - 256)
							if idat_data[j+3] + self.alpha_arr[cur_pixel - self.width_dc] < 256:
								self.alpha_arr.append(idat_data[j+3] + self.alpha_arr[cur_pixel - self.width_dc])
							else:
								self.alpha_arr.append(idat_data[j+3] + self.alpha_arr[cur_pixel - self.width_dc] - 256)
						elif cur_filter == 2 and first_line:
							self.red_arr.append(idat_data[j])
							self.green_arr.append(idat_data[j+1])
							self.blue_arr.append(idat_data[j+2])
							self.alpha_arr.append(idat_data[j+3])
						elif cur_filter == 3 and not first_line:
							average = (self.red_arr[cur_pixel - 1] + self.red_arr[cur_pixel - self.width_dc])/2
							average = math.floor(average)
							if idat_data[j] + average < 256:
								self.red_arr.append(idat_data[j] + average)
							else:
								self.red_arr.append(idat_data[j] + average - 256)
							average = (self.green_arr[cur_pixel - 1] + self.green_arr[cur_pixel - self.width_dc])/2
							average = math.floor(average)
							if idat_data[j+1] + average < 256:
								self.green_arr.append(idat_data[j+1] + average)
							else:
								self.green_arr.append(idat_data[j+1] + average - 256)
							average = (self.blue_arr[cur_pixel - 1] + self.blue_arr[cur_pixel - self.width_dc])/2
							average = math.floor(average)
							if idat_data[j+2] + average < 256:
								self.blue_arr.append(idat_data[j+2] + average)
							else:
								self.blue_arr.append(idat_data[j+2] + average - 256)
							average = (self.alpha_arr[cur_pixel - 1] + self.alpha_arr[cur_pixel - self.width_dc])/2
							average = math.floor(average)
							if idat_data[j+3] + average < 256:
								self.alpha_arr.append(idat_data[j+3] + average)
							else:
								self.alpha_arr.append(idat_data[j+3] + average - 256)
						elif cur_filter == 3 and first_line:
							self.red_arr.append(idat_data[j])
							self.green_arr.append(idat_data[j+1])
							self.blue_arr.append(idat_data[j+2])
							self.alpha_arr.append(idat_data[j+3])
						elif cur_filter == 4 and not first_line:
							pix_a = self.red_arr[cur_pixel - 1]
							pix_b = self.red_arr[cur_pixel - self.width_dc]
							pix_c = self.red_arr[cur_pixel - self.width_dc - 1]
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
							if idat_data[j] + paeth_r < 256:
								self.red_arr.append(idat_data[j] + paeth_r)
							else:
								self.red_arr.append(idat_data[j] + paeth_r - 256)

							pix_a = self.green_arr[cur_pixel - 1]
							pix_b = self.green_arr[cur_pixel - self.width_dc]
							pix_c = self.green_arr[cur_pixel - self.width_dc - 1]
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
							if idat_data[j+1] + paeth_r < 256:
								self.green_arr.append(idat_data[j+1] + paeth_r)
							else:
								self.green_arr.append(idat_data[j+1] + paeth_r - 256)

							pix_a = self.blue_arr[cur_pixel - 1]
							pix_b = self.blue_arr[cur_pixel - self.width_dc]
							pix_c = self.blue_arr[cur_pixel - self.width_dc - 1]
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
							if idat_data[j+2] + paeth_r < 256:
								self.blue_arr.append(idat_data[j+2] + paeth_r)
							else:
								self.blue_arr.append(idat_data[j+2] + paeth_r - 256)

							pix_a = self.alpha_arr[cur_pixel - 1]
							pix_b = self.alpha_arr[cur_pixel - self.width_dc]
							pix_c = self.alpha_arr[cur_pixel - self.width_dc - 1]
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
							if idat_data[j+3] + paeth_r < 256:
								self.alpha_arr.append(idat_data[j+3] + paeth_r)
							else:
								self.alpha_arr.append(idat_data[j+3] + paeth_r - 256)
						elif cur_filter == 4 and first_line:
							self.red_arr.append(idat_data[j])
							self.green_arr.append(idat_data[j+1])
							self.blue_arr.append(idat_data[j+2])
							self.alpha_arr.append(idat_data[j+3])
						j += 4
						cur_pixel += 1
						if column == self.width_dc - 1:
							column = 0
							first_line = False
						else:
							column += 1

				print("Reading image... Complete")

			if chunk_name_dc == "IEND":
				i += 20
			else:
				i += 8 + chunk_length_dc



	def PrintHeaderValues(self):
		print("Width:", self.width_dc)
		print("Height:", self.height_dc)
		print("Bit depth:", self.bit_depth)
		if self.color_type == 0:
			print("Color type: Greyscale (0)")
		elif self.color_type == 2:
			print("Color type: Truecolor (2)")
		elif self.color_type == 3:
			print("Color type: Indexed-color (3)")
		elif self.color_type == 4:
			print("Color type: Greyscale with Alpha (4)")
		elif self.color_type == 6:
			print("Color type: Truecolor with Alpha (6)")
		print("Compression method:", self.compression_method)
		print("Filter method:", self.filter_method)
		print("Interlace:", self.interlace)

	def PrintChunks(self):
		j = 0
		while j < len(self.chunks_in_file):
			print("Chunk " + str(j+1) + ": " + self.chunks_in_file[j])
			j += 1

	def PrintPixels(self):
		j = 0
		while j < len(self.red_arr):
			print("Pixel " + str(j+1) + ": " + str(self.red_arr[j]) + " " + str(self.green_arr[j]) + " " + str(self.blue_arr[j]) + " " + str(self.alpha_arr[j]))
			j += 1

	def MixPixels(self):
		new_file = self.file_name[:4] + "_new.png"
		f = open(new_file, 'wb')
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
		width_i = self.width_dc
		ihdr_section += width_i.to_bytes(4, 'big')

		# PNG Height (4 bytes)
		height_i = self.height_dc
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
		i = 0
		idat_byte_arr = []
		column = 0
		row = 1
		while i < len(self.red_arr):
			if column == 0:
				idat_byte_arr.append(0)
			if row % 2 == 1 and row != self.height_dc:
				if column % 2 == 0 and column < self.width_dc - 1:
					idat_byte_arr.append(self.red_arr[i + self.width_dc])
					idat_byte_arr.append(self.green_arr[i + self.width_dc])
					idat_byte_arr.append(self.blue_arr[i + self.width_dc])
					idat_byte_arr.append(self.alpha_arr[i + self.width_dc])
				elif column % 2 == 1 and column < self.width_dc - 1:
					idat_byte_arr.append(self.red_arr[i - 1])
					idat_byte_arr.append(self.green_arr[i - 1])
					idat_byte_arr.append(self.blue_arr[i - 1])
					idat_byte_arr.append(self.alpha_arr[i - 1])
				else:
					idat_byte_arr.append(self.red_arr[i])
					idat_byte_arr.append(self.green_arr[i])
					idat_byte_arr.append(self.blue_arr[i])
					idat_byte_arr.append(self.alpha_arr[i])
			elif row % 2 == 0 and row != self.height_dc:
				if column % 2 == 0 and column < self.width_dc - 1:
					idat_byte_arr.append(self.red_arr[i + 1])
					idat_byte_arr.append(self.green_arr[i + 1])
					idat_byte_arr.append(self.blue_arr[i + 1])
					idat_byte_arr.append(self.alpha_arr[i + 1])
				elif column % 2 == 1 and column < self.width_dc - 1:
					idat_byte_arr.append(self.red_arr[i - self.width_dc])
					idat_byte_arr.append(self.green_arr[i - self.width_dc])
					idat_byte_arr.append(self.blue_arr[i - self.width_dc])
					idat_byte_arr.append(self.alpha_arr[i - self.width_dc])
				else:
					idat_byte_arr.append(self.red_arr[i])
					idat_byte_arr.append(self.green_arr[i])
					idat_byte_arr.append(self.blue_arr[i])
					idat_byte_arr.append(self.alpha_arr[i])
			else:
				idat_byte_arr.append(self.red_arr[i])
				idat_byte_arr.append(self.green_arr[i])
				idat_byte_arr.append(self.blue_arr[i])
				idat_byte_arr.append(self.alpha_arr[i])
			i += 1
			if column == self.width_dc - 1:
				column = 0
				row += 1
			else:
				column += 1

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

	def DuplicateImage(self):
		new_file = self.file_name[:-4] + "_dup.png"
		f = open(new_file, 'wb')
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
		width_i = self.width_dc
		ihdr_section += width_i.to_bytes(4, 'big')

		# PNG Height (4 bytes)
		height_i = self.height_dc
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
		i = 0
		idat_byte_arr = []
		column = 0
		total_pix = len(self.red_arr)
		while i < len(self.red_arr):
			if column == 0:
				idat_byte_arr.append(0)
			idat_byte_arr.append(self.red_arr[i])
			idat_byte_arr.append(self.green_arr[i])
			idat_byte_arr.append(self.blue_arr[i])
			idat_byte_arr.append(self.alpha_arr[i])

			perc = format((i / total_pix)*100, '.2f')
			print("Writing image... " + str(perc) + "%", end="\r")

			i += 1
			if column == self.width_dc - 1:
				column = 0
			else:
				column += 1

		print("Writing image... Complete")

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

	def UpSampleImage(self):
		new_file = self.file_name[:-4] + "_up.png"
		f = open(new_file, 'wb')
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
		width_i = self.width_dc
		ihdr_section += width_i.to_bytes(4, 'big')

		# PNG Height (4 bytes)
		height_i = self.height_dc
		ihdr_section += height_i.to_bytes(4, 'big')

		# Bit depth (1 byte) 8
		bit_depth_i = 16
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
		i = 0
		idat_byte_arr = []
		column = 0
		total_pix = len(self.red_arr)
		while i < len(self.red_arr):
			if column == 0:
				idat_byte_arr.append(0)
			idat_byte_arr.append(self.red_arr[i])
			idat_byte_arr.append(self.red_arr[i])
			idat_byte_arr.append(self.green_arr[i])
			idat_byte_arr.append(self.green_arr[i])
			idat_byte_arr.append(self.blue_arr[i])
			idat_byte_arr.append(self.blue_arr[i])
			idat_byte_arr.append(self.alpha_arr[i])
			idat_byte_arr.append(self.alpha_arr[i])

			perc = format((i / total_pix)*100, '.2f')
			print("Writing image... " + str(perc) + "%", end="\r")

			i += 1
			if column == self.width_dc - 1:
				column = 0
			else:
				column += 1

		print("Writing image... Complete")

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

	def FlipColors(self):
		new_file = self.file_name[:-4] + "_new.png"
		f = open(new_file, 'wb')
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
		width_i = self.width_dc
		ihdr_section += width_i.to_bytes(4, 'big')

		# PNG Height (4 bytes)
		height_i = self.height_dc
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
		i = 0
		idat_byte_arr = []
		column = 0
		total_pix = len(self.red_arr)
		while i < len(self.red_arr):
			if column == 0:
				idat_byte_arr.append(0)
			idat_byte_arr.append(self.blue_arr[i])
			idat_byte_arr.append(self.red_arr[i])
			idat_byte_arr.append(self.alpha_arr[i])
			idat_byte_arr.append(self.green_arr[i])

			perc = format((i / total_pix)*100, '.2f')
			print("Writing image... " + str(perc) + "%", end="\r")

			i += 1
			if column == self.width_dc - 1:
				column = 0
			else:
				column += 1

		print("Writing image... Complete")

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

	def ColorScramble(self):
		new_file = self.file_name[:-4] + "_new.png"
		f = open(new_file, 'wb')
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
		width_i = self.width_dc
		ihdr_section += width_i.to_bytes(4, 'big')

		# PNG Height (4 bytes)
		height_i = self.height_dc
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
		i = 0
		idat_byte_arr = []
		column = 0
		total_pix = len(self.red_arr)
		scram = 0
		while i < len(self.red_arr):
			if column == 0:
				idat_byte_arr.append(0)

			if scram == 0:
				idat_byte_arr.append(self.red_arr[i])
				idat_byte_arr.append(self.green_arr[i])
				idat_byte_arr.append(self.blue_arr[i])
				idat_byte_arr.append(self.alpha_arr[i])
			elif scram == 1:
				idat_byte_arr.append(self.alpha_arr[i])
				idat_byte_arr.append(self.red_arr[i])
				idat_byte_arr.append(self.green_arr[i])
				idat_byte_arr.append(self.blue_arr[i])
			elif scram == 2:
				idat_byte_arr.append(self.blue_arr[i])
				idat_byte_arr.append(self.alpha_arr[i])
				idat_byte_arr.append(self.red_arr[i])
				idat_byte_arr.append(self.green_arr[i])
			elif scram == 3:
				idat_byte_arr.append(self.green_arr[i])
				idat_byte_arr.append(self.blue_arr[i])
				idat_byte_arr.append(self.alpha_arr[i])
				idat_byte_arr.append(self.red_arr[i])

			if scram == 3:
				scram = 0
			else:
				scram += 1

			perc = format((i / total_pix)*100, '.2f')
			print("Writing image... " + str(perc) + "%", end="\r")

			i += 1
			if column == self.width_dc - 1:
				column = 0
				if scram == 3:
					scram = 0
				else:
					scram += 1
			else:
				column += 1

		print("Writing image... Complete")

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

