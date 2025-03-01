import argparse
import xml.etree.ElementTree as ET

from constants import LENGTH, WIDTH

parser = argparse.ArgumentParser()
parser.add_argument('--s', action='store_true')
parser.add_argument('--u', action='store_true')
parser.add_argument('--d', action='store_true')

args = vars(parser.parse_args())
set = args['s']
update = args['u']
delete = args['d']

# site
RIGHT_FINGER_LINK_PATH = 'assets/vx300s_right.xml'
RIGHT_FINGER_LINK = 'vx300s_right/right_finger_link'
LEFT_FINGER_LINK_PATH = 'assets/vx300s_left.xml'
LEFT_FINGER_LINK = 'vx300s_left/right_finger_link'

# task
EE_TRANSFER_PATH = 'assets/bimanual_viperx_ee_transfer_cube.xml'
EE_INSERTION_PATH = 'assets/bimanual_viperx_ee_insertion.xml'
TRANSFER_PATH = 'assets/bimanual_viperx_transfer_cube.xml'
INSERTION_PATH = 'assets/bimanual_viperx_insertion.xml'

length = LENGTH
width = WIDTH

# sensor_pos = [0.0240, 0.0220, 0.0050]
sensor_pos = [0.0210, 0.0220, 0.0100]
radius = 0.0020
box_length = 0.0090 # 同末端执行器x轴方向
box_width = 0.0020 # 同末端执行器y轴方向
box_height = 0.0090


if delete:
    tree = ET.parse(RIGHT_FINGER_LINK_PATH)
    root = tree.getroot()
    parent = root.find(f'.//body[@name="{RIGHT_FINGER_LINK}"]')
    if parent is not None:
        for site in parent.findall('site'):
            parent.remove(site)
        tree.write(RIGHT_FINGER_LINK_PATH)
    
    tree = ET.parse(LEFT_FINGER_LINK_PATH)
    root = tree.getroot()
    parent = root.find(f'.//body[@name="{LEFT_FINGER_LINK}"]')
    if parent is not None:
        for site in parent.findall('site'):
            parent.remove(site)
        tree.write(LEFT_FINGER_LINK_PATH)

    tree_sensor = ET.parse(EE_TRANSFER_PATH)
    root_sensor = tree_sensor.getroot()
    if root_sensor is not None:
        sensor = root_sensor.find('sensor')
        for touch in sensor.findall('touch'):
            sensor.remove(touch)
        tree_sensor.write(EE_TRANSFER_PATH)
    tree_sensor = ET.parse(EE_INSERTION_PATH)
    root_sensor = tree_sensor.getroot()
    if root_sensor is not None:
        sensor = root_sensor.find('sensor')
        for touch in sensor.findall('touch'):
            sensor.remove(touch)
        tree_sensor.write(EE_INSERTION_PATH)

    tree_sensor = ET.parse(TRANSFER_PATH)
    root_sensor = tree_sensor.getroot()
    if root_sensor is not None:
        sensor = root_sensor.find('sensor')
        for touch in sensor.findall('touch'):
            sensor.remove(touch)
        tree_sensor.write(TRANSFER_PATH)
    tree_sensor = ET.parse(INSERTION_PATH)
    root_sensor = tree_sensor.getroot()
    if root_sensor is not None:
        sensor = root_sensor.find('sensor')
        for touch in sensor.findall('touch'):
            sensor.remove(touch)
        tree_sensor.write(INSERTION_PATH)


# 末端执行器的执行为x轴正方向，y轴正方向垂直于抓爪面
# 传感器阵列的行数为width（x轴方向），列数为length（z轴方向）
if set:
    tree = ET.parse(RIGHT_FINGER_LINK_PATH)
    root = tree.getroot()
    parent = root.find(f'.//body[@name="{RIGHT_FINGER_LINK}"]')
    if parent is not None:
        for row in range(0, width):
            for col in range(0, length):
                new_site = ET.Element('site')
                new_site.set('name', 'rgrf_tactile' + f'{row*length+col}')
                new_site.set('type', 'box')
                new_site.set('pos', f'{sensor_pos[0]+2*box_length*row} {sensor_pos[1]} {sensor_pos[2]-2*box_height*col}')
                pos_value = new_site.get('pos').split(' ')
                round_pos = ''.join([str(round(float(value), 4)) + ' ' for value in pos_value])[:-1]
                new_site.set('pos', round_pos)
                new_site.set('size', f'{box_length} {box_width} {box_height}')
                new_site.set('rgba', '0 1 0 0.5')
                parent.append(new_site)
                parent.append(ET.Comment('\n'))
        tree.write(RIGHT_FINGER_LINK_PATH)

    tree = ET.parse(LEFT_FINGER_LINK_PATH)
    root = tree.getroot()
    parent = root.find(f'.//body[@name="{LEFT_FINGER_LINK}"]')
    if parent is not None:
        for row in range(0, width):
            for col in range(0, length):
                new_site = ET.Element('site')
                new_site.set('name', 'lgrf_tactile' + f'{row*length+col}')
                new_site.set('type', 'box')
                new_site.set('pos', f'{sensor_pos[0]+2*box_length*row} {sensor_pos[1]} {sensor_pos[2]-2*box_height*col}')
                pos_value = new_site.get('pos').split(' ')
                round_pos = ''.join([str(round(float(value), 4)) + ' ' for value in pos_value])[:-1]
                new_site.set('pos', round_pos)
                new_site.set('size', f'{box_length} {box_width} {box_height}')
                new_site.set('rgba', '0 1 0 0.5')
                parent.append(new_site)
                parent.append(ET.Comment('\n'))
        tree.write(LEFT_FINGER_LINK_PATH)

    tree_sensor = ET.parse(EE_TRANSFER_PATH)
    root_sensor = tree_sensor.getroot()
    if root_sensor is not None:
        for num in range(0, length*width):
            new_touch = ET.Element('touch')
            new_touch.set('name', 'rgrf_tactile_sensor' + f'{num}')
            new_touch.set('site', 'rgrf_tactile' + f'{num}')
            #new_touch.set('contype', '1')
            #new_touch.set('conaffinity', '1')
            #new_touch.set('condim', '3')
            root_sensor.find('sensor').append(new_touch)
            root_sensor.find('sensor').append(ET.Comment('\n'))
        for num in range(0, length*width):
            new_touch = ET.Element('touch')
            new_touch.set('name', 'lgrf_tactile_sensor' + f'{num}')
            new_touch.set('site', 'lgrf_tactile' + f'{num}')
            #new_touch.set('contype', '1')
            #new_touch.set('conaffinity', '1')
            #new_touch.set('condim', '3')
            root_sensor.find('sensor').append(new_touch)
            root_sensor.find('sensor').append(ET.Comment('\n'))
        tree_sensor.write(EE_TRANSFER_PATH)

    tree_sensor = ET.parse(EE_INSERTION_PATH)
    root_sensor = tree_sensor.getroot()
    if root_sensor is not None:
        for num in range(0, length*width):
            new_touch = ET.Element('touch')
            new_touch.set('name', 'rgrf_tactile_sensor' + f'{num}')
            new_touch.set('site', 'rgrf_tactile' + f'{num}')
            #new_touch.set('contype', '1')
            #new_touch.set('conaffinity', '1')
            #new_touch.set('condim', '3')
            root_sensor.find('sensor').append(new_touch)
            root_sensor.find('sensor').append(ET.Comment('\n'))
        for num in range(0, length*width):
            new_touch = ET.Element('touch')
            new_touch.set('name', 'lgrf_tactile_sensor' + f'{num}')
            new_touch.set('site', 'lgrf_tactile' + f'{num}')
            #new_touch.set('contype', '1')
            #new_touch.set('conaffinity', '1')
            #new_touch.set('condim', '3')
            root_sensor.find('sensor').append(new_touch)
            root_sensor.find('sensor').append(ET.Comment('\n'))
        tree_sensor.write(EE_INSERTION_PATH)

    tree_sensor = ET.parse(TRANSFER_PATH)
    root_sensor = tree_sensor.getroot()
    if root_sensor is not None:
        for num in range(0, length*width):
            new_touch = ET.Element('touch')
            new_touch.set('name', 'rgrf_tactile_sensor' + f'{num}')
            new_touch.set('site', 'rgrf_tactile' + f'{num}')
            #new_touch.set('contype', '1')
            #new_touch.set('conaffinity', '1')
            #new_touch.set('condim', '3')
            root_sensor.find('sensor').append(new_touch)
            root_sensor.find('sensor').append(ET.Comment('\n'))
        for num in range(0, length*width):
            new_touch = ET.Element('touch')
            new_touch.set('name', 'lgrf_tactile_sensor' + f'{num}')
            new_touch.set('site', 'lgrf_tactile' + f'{num}')
            #new_touch.set('contype', '1')
            #new_touch.set('conaffinity', '1')
            #new_touch.set('condim', '3')
            root_sensor.find('sensor').append(new_touch)
            root_sensor.find('sensor').append(ET.Comment('\n'))
        tree_sensor.write(TRANSFER_PATH)

    tree_sensor = ET.parse(INSERTION_PATH)
    root_sensor = tree_sensor.getroot()
    if root_sensor is not None:
        for num in range(0, length*width):
            new_touch = ET.Element('touch')
            new_touch.set('name', 'rgrf_tactile_sensor' + f'{num}')
            new_touch.set('site', 'rgrf_tactile' + f'{num}')
            #new_touch.set('contype', '1')
            #new_touch.set('conaffinity', '1')
            #new_touch.set('condim', '3')
            root_sensor.find('sensor').append(new_touch)
            root_sensor.find('sensor').append(ET.Comment('\n'))
        for num in range(0, length*width):
            new_touch = ET.Element('touch')
            new_touch.set('name', 'lgrf_tactile_sensor' + f'{num}')
            new_touch.set('site', 'lgrf_tactile' + f'{num}')
            #new_touch.set('contype', '1')
            #new_touch.set('conaffinity', '1')
            #new_touch.set('condim', '3')
            root_sensor.find('sensor').append(new_touch)
            root_sensor.find('sensor').append(ET.Comment('\n'))
        tree_sensor.write(INSERTION_PATH)
    

if update:
    tree = ET.parse(RIGHT_FINGER_LINK_PATH)
    root = tree.getroot()
    for num in range(0, length*width):
        pos = "rgrf_tactile" + f"{num}"
        root.find(f'.//site[@name="{pos}"]').set('pos', f"{sensor_pos[0]+2*box_length*(num//length)} {sensor_pos[1]} {sensor_pos[2]-2*box_height*(num%length)}")
    tree.write(RIGHT_FINGER_LINK_PATH)
    tree = ET.parse(LEFT_FINGER_LINK_PATH)
    root = tree.getroot()
    for num in range(0, length*width):
        pos = "lgrf_tactile" + f"{num}"
        root.find(f'.//site[@name="{pos}"]').set('pos', f"{sensor_pos[0]+2*box_length*(num//length)} {sensor_pos[1]} {sensor_pos[2]-2*box_height*(num%length)}")
    tree.write(LEFT_FINGER_LINK_PATH)
