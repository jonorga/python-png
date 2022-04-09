import struct, zlib

class png_obj:
	def __init__(self, png_file):
		# Read file
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

		i = 28
		self.chunks_in_file = []

		chunk2_leng = self.raw_data[33:37]
		chunk2_leng_dc = int.from_bytes(chunk2_leng, byteorder='big')
		print(chunk2_leng_dc)
		#while i < len(self.raw_data):



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


img = png_obj("test.png")