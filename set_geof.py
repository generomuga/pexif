from lib import Utils
import os
import sys
from pexif import JpegFile

def read_gpx(filename):
    #Read gpx files
    file_input = open(filename, 'r')

    list_gpx = []
    for i, line in enumerate(file_input):
        if i > 0:
            id, lon, lat = line.strip().split(',')
            list_gpx.append((id, lon, lat))

    return list_gpx

def read_id(filename):
    #Read pic id
    file_input = open(filename, 'r')

    list_id = []
    for i, line in enumerate(file_input):
        if i > 0:
            pid, gid = line.strip().split(',')
            list_id.append((pid, gid))

    return list_id

def get_photo_id_gid(list_gpx, list_id):
    list_photo_id_gid = []
    for i in range(len(list_gpx)):
        for a in range(len(list_id)):
            if str(list_gpx[i][0]) == str(list_id[a][1]):
                list_photo_id_gid.append((list_id[a][0], list_id[a][1]))

    return list_photo_id_gid

def get_filename(dir):
    #Return filenames in directory
    list_fnames = []
    for items in os.listdir(dir):
        if items.endswith('.jpg'):
            list_fnames.append(items)

    return list_fnames

def set_coordinates(dir, list_pid_coordinates, list_fnames):
    for id, lon, lat in list_pid_coordinates:
        for fname in list_fnames:
            try:
                fid, year, mot, day, ph = fname.strip().split('_')
                if str(id) == str(fid):
                    print (id, lon, lat)
                    set_gps(dir+fname, lat, lon)
            except:
                pass

def set_gps(filename, lat, lon):
    try:
        print (filename)
        ef = JpegFile.fromFile(filename)
        ef.set_geo(float(lat), float(lon))
    except IOError:
        type, value, traceback = sys.exc_info()
        print >> sys.stderr, "Error opening file:", value
    except JpegFile.InvalidFile:
        type, value, traceback = sys.exc_info()
        print >> sys.stderr, "Error opening file:", value

    try:
        ef.writeFile(filename)
        print ('Done')
    except IOError:
        type, value, traceback = sys.exc_info()
        print >> sys.stderr, "Error saving file:", value

def get_coordinates(list_gpx, list_photo_id_gid):
    #Get photo id, lon, lat
    list_pid_coordinates = []
    for i in range(len(list_photo_id_gid)):
        for a in range(len(list_gpx)):
            if str(list_photo_id_gid[i][1]) == str(list_gpx[a][0]):
                list_pid_coordinates.append((list_photo_id_gid[i][0], list_gpx[a][1], list_gpx[a][2]))

    return list_pid_coordinates

if __name__ == '__main__':
    list_gpx = read_gpx('E:\\Projects\\Python\\pexif\\input\\gpx_ref.csv')
    list_id = read_id('E:\\Projects\\Python\\pexif\\input\\id_ref.csv')
    list_photo_id_gid = get_photo_id_gid(list_gpx, list_id)

    dir_pic = 'E:\\Projects\\Python\\pexif\\input\\RNR\\'
    list_fnames = get_filename(dir_pic)
    list_pid_coordinates = get_coordinates(list_gpx, list_photo_id_gid)
    set_coordinates(dir_pic, list_pid_coordinates, list_fnames)

    #set_gps('E:\\Projects\\Python\\pexif\\input\\RNR\\10526_2019_3_10_1.jpg', 13.273, 121.786)
