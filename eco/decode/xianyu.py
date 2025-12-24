"""
闲鱼签名/解密 唯一入口
必须实现：sign(inputs:dict)->str
"""
import hashlib, time, requests

def sign(inputs: dict) -> str:
    """
    inputs = {
        "token": "7d47eba4b01301b0e1fa82e71dcc2c6d",
        "t": "1765955649510",
        "appKey": "34839810",
        "data": '{"itemId":"","pageSize":30,...}'
    }
    """
    raw = f"{inputs['token']}&{inputs['t']}&{inputs['appKey']}&{inputs['data']}"
    return hashlib.md5(raw.encode()).hexdigest()

def refresh_inputs(inputs: dict) -> dict:
    # 1. 刷新 Cookie
    rs = requests.get("https://www.goofish.com", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }, timeout=10)
    token = rs.cookies.get("_m_h5_tk", "").split("_")[0] or inputs["token"]
    # 2. 新时间戳
    t = str(int(time.time() * 1000))
    # 3. 新签名
    new_inputs = {**inputs, "token": token, "t": t}
    new_inputs["sign"] = sign(new_inputs)
    # 4. 连带返回新 Cookie，方便中间件统一更新
    new_inputs["cookies"] = {k: v for k, v in rs.cookies.items()}
    return new_inputs