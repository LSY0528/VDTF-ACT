from dm_control import mujoco
import numpy as np
import matplotlib.pyplot as plt

physics = mujoco.Physics.from_xml_path("assets/bimanual_viperx_insertion.xml")

# 渲染深度信息
depth = physics.render(camera_id="top", depth=True, height=480, width=640)


# 限制深度范围
"""near1 = 0.1
far1 = 0.7"""
near = 0.1#0.1
far = 0.8 # 0.6
depth_clipped = np.clip(depth, near, far)

# 归一化深度图以显示灰度部分
depth_normalized = (depth_clipped - near) / (far - near)

# 保存深度图片
plt.imsave('depth_image.png', depth_normalized, cmap='gray')
print("Depth size: ", depth_normalized.shape)
print("Depth max: ", np.max(depth_normalized))
print("Depth min: ", np.min(depth_normalized))