"""
decode 工厂：spider.name -> decode 模块
约定：文件名=站点名，必须包含 sign(inputs:dict)->str 函数
"""
import importlib

def get_signer(spider_name: str):
    try:
        mod = importlib.import_module(f"eco.decode.{spider_name}")
        return mod
    except ModuleNotFoundError:
        raise ValueError(f"decode 文件未实现：eco/decode/{spider_name}.py")