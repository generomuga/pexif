from pexif import JpegFile
import exifread
import os

def get_tags(filename):
  #print ('read', filename)
  image = open(filename, 'rb')
  tags = exifread.process_file(image)
  return tags

def get_exif_location(exif_data):
    lat = None
    lon = None

    gps_latitude = _get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = _get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return lat, lon

def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None

def _convert_to_degress(value):
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


if __name__ == '__main__':
  file_out = open('output\\Raw_geotag.csv', 'w')
  file_out.write('FILENAME, LAT, LON'+'\n')
  dir = 'E:\\Projects\\Python\pexif\input\RNR_v2\\'
  for item in os.listdir(dir):
      if item.endswith('.jpg'):
          tags = get_tags(dir+item)
          try:
              lat,lon = get_exif_location(tags)
              file_out.write(item+','+str(lat)+','+str(lon)+'\n')
          except:
              print ('NO Exif', item)
