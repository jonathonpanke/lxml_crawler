from time import gmtime, strftime
import codecs

class Logger:

	'''
	Logger contructor has one parameter which is the string representation
	of the name of the file to write the log information to. If a filename
	isn't given the default is log. The second value is a reference to the
	actual file once it has been created. 
	'''
	def __init__(self, filename="log"):

		self.filename = filename
		self.f = None

	'''
	Creates the file that the information is to be written to.
	The method appends a log number to the desired filename, and
	recursively tries to create a new file if the filename and log 
	number already exists.
	'''
	def create_log_file(self, log_number=1):
		
		self.f = self.filename + str(log_number) + ".txt"

		try:
			with open(self.f):
				self.create_log_file(log_number + 1)
		except IOError:
			writer = codecs.open(self.f, "w", "utf-8-sig")
			temp_string = "Log Time: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n\n"
			writer.write(temp_string)
			writer.close()

	'''
	Log method is used to log information to the log file. 
	'''
	def log(self, info):

		writer = codecs.open(self.f, "a", "utf-8-sig")
		try:
			writer.write(str(info))
		except UnicodeEncodeError:
			writer.write( "UnicodeEncodeError: Error in encoding info\n\n" )
		writer.close()