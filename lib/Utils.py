from pexif import JpegFile

class Utils:

    def __init__(self):
        pass

    def set_coordinates(**kwargs):
        try:
    	    ef = JpegFile.fromFile(kwargs['filename'])
    	    ef.set_geo(float(kwargs['lat']), float(kwargs['lon']))
    	except IOError:
    	    type, value, traceback = sys.exc_info()
    	    print >> sys.stderr, "Error opening file:", value
    	except JpegFile.InvalidFile:
    	    type, value, traceback = sys.exc_info()
    	    print >> sys.stderr, "Error opening file:", value

    	try:
    	    ef.writeFile(filename)
    	except IOError:
    	    type, value, traceback = sys.exc_info()
    	    print >> sys.stderr, "Error saving file:", value

if __name__ == '__main__':
    pass
