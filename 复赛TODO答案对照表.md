# 复赛19个TODO答案对照表

## 比赛说明
- **总时间**：90分钟 | **总分**：100分
- **平台**：智能感知综合实验平台（ROS2 + Flask + 机械臂 + 深度相机）
- **规则**：只可修改 Python 文件，不可改前端/脚本/底层驱动
- **核心技巧**：每个TODO的上方被注释掉的"原代码"就是答案！

---

## 模块A：大模型目标分类（15分钟·20分）

**文件**：`src/large_models/large_models/llm_waste_classification_push.py`
**参考**：`src/large_models/large_models/llm_waste_classification.py`（完整版，行188-213）

### A1 — 读取大模型返回的动作字符串（4分）
- **位置**：process()函数，约204行
- **TODO代码**：`text = ____A1_____`
- **答案**：`text = result['action']`
- **解释**：`result` 是 `eval()` 解析LLM返回的JSON字符串得到的字典，`result['action']` 取出类似 `"garbage_classification('food_waste')"` 的字符串
- **参考证明**：`llm_waste_classification.py:188` — `text = result['action']`

### A2 — 从params提取垃圾类别列表（5分）
- **位置**：process()函数，约212行
- **TODO代码**：`objects = ____A2_____`
- **答案**：`objects = re.findall(r"['\"]([^'\"]+)['\"]", params)`
- **解释**：`params` 是正则匹配括号内内容得到的字符串，如 `'food_waste', 'hazardous_waste'`，用 `re.findall` 提取引号内的垃圾类别名
- **参考证明**：`llm_waste_classification.py:198` — `objects = re.findall(r"['\"]([^'\"]+)['\"]", params)`

### A3 — 设置语音回复文本（5分）
- **位置**：process()函数，约238行
- **TODO代码**：`msg.data = ____A3_____`
- **答案**：`msg.data = result['response']`
- **解释**：`result['response']` 是LLM生成的回复文本（如"收到，我马上收拾"），填入ROS2 String消息发布给TTS节点播报
- **参考证明**：`llm_waste_classification.py:213` — `msg.data = result['response']`

### A4 — 关闭机械臂使能开关（6分）
- **位置**：process()函数，约215行
- **TODO代码**：`enable_sorting = ____A4_____`
- **答案**：`enable_sorting = False`
- **解释**：A模块单独测试时，机械臂不能动作，必须保持 `False`。只有D模块最终联调时才改为 `True`
- **参考证明**：任务书原文"A模块关闭，D模块最终联调时打开"；push版现有值已是 `False`

---

## 模块B：视觉模块/目标筛选（20分钟·20分）

**文件**：`src/app/app/waste_classification_push.py`
**参考**：`src/app/app/waste_classification.py`（完整版）

### B1 — 补齐可回收物识别类别（5分）
- **位置**：WASTE_CLASSES字典，约45行
- **TODO代码**：`'recyclable_waste': (____B1____),`
- **答案**：`'recyclable_waste': ('PlasticBottle', 'Toothbrush', 'Umbrella'),`
- **解释**：将三大类可回收物（塑料瓶、牙刷、雨伞）对应的YOLO标签填入元组
- **参考证明**：`waste_classification.py:33` — `'recyclable_waste': ('PlasticBottle', 'Toothbrush', 'Umbrella')`

### B2 — 按垃圾大类展开识别类别（5分）
- **位置**：set_target_srv_callback()，约276行
- **TODO代码**：`target_list.extend(list(____B2_____.get(i, [])))`
- **答案**：`target_list.extend(list(WASTE_CLASSES.get(i, [])))`
- **解释**：`request.data` 中是垃圾大类名（如 `['recyclable_waste']`），从 `WASTE_CLASSES` 字典查出对应的YOLO标签列表
- **参考证明**：`waste_classification.py:248` — `target_list.extend(list(WASTE_CLASSES.get(i, [])))`

### B3 — 判断识别类别是否在目标列表中（5分）
- **位置**：get_object_callback()，约522行
- **TODO代码**：`if ____B3_____:`
- **答案**：`if i.class_name in self.target_list:`
- **解释**：YOLO检测到的每个物体的 `class_name`（如"PlasticBottle"）只有存在于 `self.target_list` 中才作为候选目标
- **参考证明**：`waste_classification.py:423` — `if i.class_name in self.target_list:`

### B4 — 深拷贝保存候选目标信息（5分）
- **位置**：get_object_callback()，约534行
- **TODO代码**：`self.target_object_info = _____B4_____(local_target_object_info)`
- **答案**：`self.target_object_info = copy.deepcopy(local_target_object_info)`
- **解释**：必须用 `copy.deepcopy()` 深拷贝，防止后续对 `local_target_object_info` 的修改影响已保存的目标信息
- **参考证明**：`waste_classification.py:437` — `self.target_object_info = copy.deepcopy(local_target_object_info)`

---

## 模块C：Python数据可视化接口（25分钟·30分）

**文件**：`src/my_sensors/ai-warehouse/app.py` + `models/warehouse.py`

### C1 — 从传感器服务获取超声波数据（5分）
- **位置**：get_ultrasonic_data()，约264行
- **TODO代码**：`ultrasonic_data = ____C1___`
- **答案**：`ultrasonic_data = self.sensor_service.get_ultrasonic_data()`
- **解释**：调用已初始化的 `self.sensor_service` 的 `get_ultrasonic_data()` 方法获取真实传感器数据
- **参考证明**：`app.py:263` 注释掉的 `# ultrasonic_data = self.sensor_service.get_ultrasonic_data()`

### C2 — JSON返回超声波距离值（5分）
- **位置**：get_ultrasonic_data()，约271行
- **TODO代码**：`'distance': ___C2__`
- **答案**：`'distance': ultrasonic_data['distance']`
- **解释**：从C1获取的字典中取出 `distance` 字段
- **参考证明**：`app.py:270` 注释掉的 `# 'distance': ultrasonic_data['distance']`

### C3 — 从传感器服务获取DHT11温湿度数据（5分）
- **位置**：get_dht11_data()，约235行
- **TODO代码**：`dht11_data = ___C3___`
- **答案**：`dht11_data = self.sensor_service.get_dht11_data()`
- **解释**：同上，调用 `self.sensor_service.get_dht11_data()` 获取真实DHT11传感器数据
- **参考证明**：`app.py:234` 注释掉的 `# dht11_data = self.sensor_service.get_dht11_data()`

### C4-1 — JSON返回温度值（5分中的2.5分）
- **位置**：get_dht11_data()，约242行
- **TODO代码**：`'temperature': _______, # TODO C4-1`
- **答案**：`'temperature': dht11_data['temperature']`
- **解释**：从C3获取的字典中取出 `temperature`
- **参考证明**：`app.py:241` 注释掉的 `# 'temperature': dht11_data['temperature']`

### C4-2 — JSON返回湿度值（5分中的2.5分）
- **位置**：get_dht11_data()，约245行
- **TODO代码**：`'humidity': ______ # TODO C4-2`
- **答案**：`'humidity': dht11_data['humidity']`
- **解释**：从C3获取的字典中取出 `humidity`
- **参考证明**：`app.py:244` 注释掉的 `# 'humidity': dht11_data['humidity']`

### C5 — 计算仓库占用率（5分）
- **位置**：warehouse.py，get_status()，约34行
- **TODO代码**：`'usage_rate': _______ # TODO C5`
- **答案**：`'usage_rate': round((self._data[i] / self._capacity) * 100, 1) if self._capacity else 0`
- **解释**：当前数量/容量×100得到百分比，`round(..., 1)` 保留一位小数，防除零保护
- **参考证明**：`warehouse.py:33` 注释掉的 `# 'usage_rate': round((self._data[i] / self._capacity) * 100, 1) if self._capacity else 0`

### C6 — SSE广播仓库更新事件（5分，4个子字段）
- **位置**：update_warehouse_quantity()，约369-379行
- **TODO代码**：4个子字段
- **答案**：
  - `'warehouses': warehouse_list`
  - `'updated_warehouse': warehouse_id`
  - `'old_quantity': old_quantity`
  - `'new_quantity': quantity`
- **解释**：将函数中已有的局部变量填入SSE广播字典，让前端看板实时更新
- **参考证明**：`app.py:362-381` 注释掉的原代码

---

## 模块D：多模态系统集成（30分钟·30分）

**文件**：`llm_waste_classification_push.py` + `waste_classification_push.py` + `app.py`

### D1 — 将目标类别写入set_target请求（6分）
- **位置**：llm_waste_classification_push.py，process()，约221行
- **TODO代码**：`msgs.data = ____D1_____`
- **答案**：`msgs.data = objects`
- **解释**：`objects` 是A2中提取的垃圾类别列表（如 `['recyclable_waste']`），填入ROS2服务请求
- **参考证明**：`llm_waste_classification.py:202` — `msgs.data = objects`

### D2 — 调用set_target服务（6分）
- **位置**：llm_waste_classification_push.py，process()，约224行
- **TODO代码**：`res = ____D2_____`
- **答案**：`res = self.send_request(self.set_target_client, msgs)`
- **解释**：使用节点封装的 `send_request()` 方法异步调用ROS2服务，将目标类别传给视觉分拣节点
- **参考证明**：`llm_waste_classification.py:203` — `res = self.send_request(self.set_target_client, msgs)`

### D3 — 启动真实分拣（6分）
- **位置**：llm_waste_classification_push.py，process()，约232行
- **TODO代码**：`start_msg.data = ____D3_____`
- **答案**：`start_msg.data = True`
- **解释**：将机械臂使能开关设为 `True`，启动真实的视觉→抓取→放置流水线。⚠️ 需教师确认安全后执行
- **参考证明**：`llm_waste_classification.py:209` — `start_msg.data = True`

### D4 — 根据垃圾类别查找仓库编号（6分）
- **位置**：waste_classification_push.py，push_dashboard_data()，约355行
- **TODO代码**：`warehouse_id = _______ # TODO D4`
- **答案**：`warehouse_id = WAREHOUSE_MAPPING[target]`
- **解释**：`target` 是垃圾分类（如 `'recyclable_waste'`），从 `WAREHOUSE_MAPPING` 字典（文件顶部行51-56）查找对应的仓库ID（1-4）
- **参考证明**：push文件自身行354注释 `# warehouse_id = WAREHOUSE_MAPPING[target]`；WAREHOUSE_MAPPING定义在行51-56

### D5 — 返回相机服务真实状态（6分）
- **位置**：app.py，health_check()，约124行
- **TODO代码**：`'camera': _______, # TODO D5`
- **答案**：`'camera': self.camera_service.is_active()`
- **解释**：调用 `camera_service` 的 `is_active()` 方法获取相机真实运行状态（True/False），替代注释掉的 `# 'camera': self.camera_service.is_active()`
- **参考证明**：`app.py:123` 注释掉的 `# 'camera': self.camera_service.is_active()`

---

## 📊 分值分布总结

| 模块 | TODO数 | 分值 | 难度 | 核心考点 |
|------|--------|------|------|----------|
| A | 4 | 20分 | ⭐⭐ | 字典取值、正则表达式、ROS2消息 |
| B | 4 | 20分 | ⭐⭐ | 元组、字典查找、成员判断、深拷贝 |
| C | 6 | 30分 | ⭐⭐⭐ | Flask API、服务调用、百分比计算、SSE |
| D | 5 | 30分 | ⭐⭐⭐ | ROS2服务调用、字典映射、系统集成 |

## 🔑 关键规律

1. **答案就在注释里**：每个TODO上方被注释掉的 `# xxx = ...  # 原代码` 就是标准答案
2. **参考文件就在旁边**：`xxx.py`（完整版）是 `xxx_push.py`（考题版）的参考答案
3. **A4是唯一需要逻辑判断的题**：A模块单独测试= False，D模块联调= True
4. **C6有4个子空**：注意全部填对才拿满分
5. **B4要写完整调用**：`copy.deepcopy(xxx)` 而不是只写 `deepcopy` 或 `copy`
