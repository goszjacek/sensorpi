import json
import functools

ANGLE = 'angle'
DIST = 'dist'
DATE = 'date'
TIME = 'time'
ROTATION = 'rotation_no'

def create_simple_readout(angle, dist):
  readout = dict()
  readout[ANGLE] = angle
  readout[DIST] = dist
  return readout

# old provide_data_from_file
def get_readouts_from_file(file_name):
  if file_name:
    with open(file_name, 'r') as f:
      file_str = f.read()
      # print(file_str)
      data_to_parse = '[' + file_str + ']'
      # print(data_to_parse)
      datastore = json.loads(data_to_parse)
      # print(datastore)
  return datastore

def split_readouts_on_rotations(readouts):
  rotations = []
  def get_rotation_no(readout):
    return readout['rotation_no']
  i = 0
  last_stamp = 0
  if get_rotation_no(readouts[0]) == get_rotation_no(readouts[1]):
    i+=1
  else:
    rotations.append([readouts[0]])
    last_stamp = 1
    i = 2

  while i < len(readouts): 
    if get_rotation_no(readouts[i]) == get_rotation_no(readouts[i-1]):
      i += 1
    else:
      #split rotationsls
      rotations.append(readouts[last_stamp:i])
      last_stamp = i
      i += 1
  return rotations
      

def reduce_readouts(acc, elem):
  def get_rotation_no(readout):
    return readout['rotation_no']
  rotations, rotation = acc
  if rotation == []:
    rotation.append(elem)
  else:
    if get_rotation_no(elem) == get_rotation_no(rotation[0]):
      rotation.append(elem)
    else:
      rotations.append(rotation)
      rotation = [elem]
  return (rotations,rotation)

def split_fold_readouts_on_rotations(readouts):
  rotations,rotation =  functools.reduce(reduce_readouts, readouts, ([],[]))
  if rotation != []:
    rotations.append(rotation)
  return rotations


def get_rotations_from_file(file_name):
  readouts = get_readouts_from_file(file_name)
  return split_fold_readouts_on_rotations(readouts)


def get_points(items):
  data = [ item[DIST] for item in items ]
  theta = [ item[ANGLE] for item in items ]
  return (data,theta)

def filterAngles(rotation, last_angle, tmp_angle):
  #? include one edge? 
  angle_a, angle_b = last_angle, tmp_angle
  if angle_a > angle_b:
    angle_a, angle_b = angle_b, angle_a
  print(angle_a, angle_b)
  def f(readout):
    return readout[ANGLE] <= angle_a or readout[ANGLE] >= angle_b

  filtered = list(filter(f, rotation))
  return filtered



if __name__ == "__main__":

 
  readouts = get_readouts_from_file('full_data.json')

  rotations = split_fold_readouts_on_rotations(readouts)
  rotation = rotations[3] 
  print(rotation)
  print()
  print(filterAngles(rotation, 1.20, 0.2))

