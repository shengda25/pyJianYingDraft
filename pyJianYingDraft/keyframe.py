import uuid

from enum import Enum
from typing import Dict, List, Any

class Keyframe:
    """一个关键帧（关键点）, 目前只支持线性插值"""

    kf_id: str
    """关键帧全局id, 自动生成"""
    time_offset: int
    """相对于素材起始点的时间偏移量"""
    values: List[float]
    """关键帧的值, 似乎一般只有一个元素"""

    def __init__(self, time_offset: int, value: float):
        """给定时间偏移量及关键值, 初始化关键帧"""
        self.kf_id = uuid.uuid4().hex

        self.time_offset = time_offset
        self.values = [value]

    def export_json(self) -> Dict[str, Any]:
        return {
            # 默认值
            "curveType": "Line",
            "graphID": "",
            "left_control": {"x": 0.0, "y": 0.0},
            "right_control": {"x": 0.0, "y": 0.0},
            # 自定义属性
            "id": self.kf_id,
            "time_offset": self.time_offset,
            "values": self.values
        }

class Keyframe_property(Enum):
    """关键帧所控制的属性类型"""

    position_x = "KFTypePositionX"
    position_y = "KFTypePositionY"
    rotation = "KFTypeRotation"

    scale_x = "KFTypeScaleX"
    """单独控制X轴缩放比例"""
    scale_y = "KFTypeScaleY"
    """单独控制Y轴缩放比例"""
    uniform_scale = "UNIFORM_SCALE"
    """同时控制X轴及Y轴缩放比例"""

    alpha = "KFTypeAlpha"
    saturation = "KFTypeSaturation"
    contrast = "KFTypeContrast"
    brightness = "KFTypeBrightness"

class Keyframe_list:
    """关键帧列表, 记录与某个特定属性相关的一系列关键帧"""

    list_id: str
    """关键帧列表全局id, 自动生成"""
    keyframe_property: Keyframe_property
    """关键帧对应的属性"""
    keyframes: List[Keyframe]
    """关键帧列表"""

    def __init__(self, keyframe_property: Keyframe_property):
        """为给定的关键帧属性初始化关键帧列表"""
        self.list_id = uuid.uuid4().hex

        self.keyframe_property = keyframe_property
        self.keyframes = []

    def add_keyframe(self, time_offset: int, value: float):
        """给定时间偏移量及关键值, 向此关键帧列表中添加一个关键帧"""
        keyframe = Keyframe(time_offset, value)
        self.keyframes.append(keyframe)
        self.keyframes.sort(key=lambda x: x.time_offset)

    def export_json(self) -> Dict[str, Any]:
        return {
            "id": self.list_id,
            "keyframe_list": [kf.export_json() for kf in self.keyframes],
            "material_id": "",
            "property_type": self.keyframe_property.value
        }