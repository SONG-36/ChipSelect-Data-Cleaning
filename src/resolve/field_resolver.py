# src/resolve/field_resolver.py

import math
from typing import List, Dict, Optional

# ---------- 工具 ----------

def _to_kb(value: float, unit: str) -> Optional[int]:
    unit = unit.lower()
    if unit.startswith("k"):
        return int(round(value))
    if unit.startswith("m"):
        return int(round(value * 1024))
    return None

def _safe_float(x: str) -> Optional[float]:
    try:
        return float(x)
    except:
        return None

# ---------- 字段收敛策略 ----------

def resolve_max_freq(cands: List[Dict]) -> Optional[int]:
    """取最大 MHz，排除明显非 CPU 场景（如 context 含 rtc）"""
    vals = []
    for c in cands:
        if "rtc" in c["context"].lower():
            continue
        v = _safe_float(c["candidate"])
        if v:
            vals.append(v)
    return int(max(vals)) if vals else None

def resolve_mem_kb(cands: List[Dict]) -> Optional[int]:
    """Flash/RAM：单位归一 → 取最大"""
    vals = []
    for c in cands:
        num = _safe_float(c["candidate"])
        if num is None:
            continue
        # 从上下文推断单位（kbyte/mbyte）
        ctx = c["context"].lower()
        if "mbyte" in ctx or "mb" in ctx:
            kb = _to_kb(num, "m")
        elif "kbyte" in ctx or "kb" in ctx:
            kb = _to_kb(num, "k")
        else:
            continue
        if kb:
            vals.append(kb)
    return max(vals) if vals else None

def resolve_vdd_range(cands: List[Dict]) -> (Optional[float], Optional[float]):
    """电压：取 min/max"""
    vals = []
    for c in cands:
        v = _safe_float(c["candidate"])
        if v:
            vals.append(v)
    if not vals:
        return None, None
    return round(min(vals), 2), round(max(vals), 2)

def resolve_package(cands: List[Dict]) -> Optional[str]:
    """封装：白名单 + 取出现频率最高"""
    allow = ("lqfp", "qfn", "bga")
    freq = {}
    for c in cands:
        p = c["candidate"].upper()
        if p.lower().startswith(allow):
            freq[p] = freq.get(p, 0) + 1
    if not freq:
        return None
    return sorted(freq.items(), key=lambda x: -x[1])[0][0]

def resolve_temp(cands: List[Dict]) -> Optional[str]:
    """温度等级：标准化输出"""
    # 直接取出现次数最多的区间
    freq = {}
    for c in cands:
        t = c["candidate"].replace(" ", "")
        freq[t] = freq.get(t, 0) + 1
    if not freq:
        return None
    return sorted(freq.items(), key=lambda x: -x[1])[0][0]

# ---------- 总调度 ----------

def resolve_fields(group: Dict[str, List[Dict]]) -> Dict:
    out = {}

    out["max_freq_mhz"] = resolve_max_freq(group.get("max_freq_mhz", []))
    out["flash_kb"] = resolve_mem_kb(group.get("flash_kb", []))
    out["ram_kb"] = resolve_mem_kb(group.get("ram_kb", []))

    vmin, vmax = resolve_vdd_range(group.get("vdd", []))
    out["vdd_min"] = vmin
    out["vdd_max"] = vmax

    out["package"] = resolve_package(group.get("package", []))
    out["temp_grade"] = resolve_temp(group.get("temp_grade", []))

    return out
