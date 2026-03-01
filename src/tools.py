# src/tools.py
from langchain.tools import BaseTool
from typing import Optional, Type

class FaultCodeTool(BaseTool):
    """故障码查询工具"""
    name: str = "故障码查询"
    description: str = "输入故障码（如P0300），返回故障含义和解决方案"
    
    def _run(self, fault_code: str):
        """实际执行逻辑"""
        fault_db = {
            "P0300": {
                "meaning": "检测到发动机缺火",
                "causes": ["火花塞老化", "点火线圈故障", "燃油系统压力不足"],
                "steps": [
                    "1. 检查火花塞状态，必要时更换",
                    "2. 检查点火线圈电阻",
                    "3. 检查燃油压力调节器"
                ]
            },
            "P0171": {
                "meaning": "燃油系统过稀（第1排）",
                "causes": ["进气系统泄漏", "氧传感器故障", "燃油压力低"],
                "steps": [
                    "1. 检查真空管路是否泄漏",
                    "2. 检查氧传感器信号",
                    "3. 测量燃油压力"
                ]
            },
            "P0420": {
                "meaning": "催化转换器效率低",
                "causes": ["催化转换器老化", "氧传感器故障", "发动机燃烧不良"],
                "steps": [
                    "1. 检查后氧传感器信号",
                    "2. 检查催化转换器温度",
                    "3. 必要时更换催化转换器"
                ]
            }
        }
        
        code = fault_code.upper().strip()
        if code in fault_db:
            data = fault_db[code]
            return f"故障码 {code}: {data['meaning']}\n可能原因: {', '.join(data['causes'])}\n排查步骤:\n" + "\n".join(data['steps'])
        else:
            return f"未找到故障码 {code} 的信息，请确认故障码格式"
    
    async def _arun(self, fault_code: str):
        return self._run(fault_code)

class MaintenanceTool(BaseTool):
    """保养建议工具"""
    name: str = "保养建议"
    description: str = "输入里程数（如5000公里），返回保养项目建议"
    
    def _run(self, query: str):
        # 简单规则引擎
        if "5000" in query or "五千" in query:
            return "5000公里保养项目：\n- 更换机油、机滤\n- 检查轮胎气压\n- 检查刹车片厚度"
        elif "10000" in query or "一万" in query:
            return "10000公里保养项目：\n- 更换机油、机滤、空滤\n- 轮胎换位\n- 检查空调滤芯"
        elif "20000" in query or "两万" in query:
            return "20000公里保养项目：\n- 更换机油、机滤、空滤、空调滤\n- 检查刹车片\n- 检查火花塞"
        else:
            return "请提供具体里程数（如5000公里、10000公里）"
    
    async def _arun(self, query: str):
        return self._run(query)

class VehicleInfoTool(BaseTool):
    """车型信息查询工具"""
    name: str = "车型信息查询"
    description: str = "输入车型名称（如深蓝SL03），返回技术参数"
    
    def _run(self, model: str):
        models = {
            "深蓝SL03": {
                "engine": "后置永磁同步电机",
                "power": "190kW",
                "battery": "58.1kWh 磷酸铁锂",
                "range": "515km"
            },
            "赛力斯SF5": {
                "engine": "1.5T 四缸增程器",
                "motor": "前后双电机",
                "power": "405kW",
                "range": "1000km+"
            }
        }
        
        for key in models:
            if key in model:
                data = models[key]
                return f"{key} 技术参数：\n- 动力：{data['engine']}\n- 功率：{data['power']}\n- 电池：{data.get('battery', 'N/A')}\n- 续航：{data.get('range', 'N/A')}"
        
        return f"未找到 {model} 的信息，请确认车型名称"
    
    async def _arun(self, model: str):
        return self._run(model)