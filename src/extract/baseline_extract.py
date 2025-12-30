import re

def extract_baseline_fields(text: str) -> dict:
    result = {
        "max_freq_mhz": None,
        "flash_kb": None,
        "ram_kb": None,
        "can": None,
        "vdd_min": None,
        "vdd_max": None,
    }

    freq = re.search(r"(\d+)\s*MHz", text, re.IGNORECASE)
    if freq:
        result["max_freq_mhz"] = int(freq.group(1))

    flash = re.search(r"(\d+)\s*KB\s*Flash", text, re.IGNORECASE)
    if flash:
        result["flash_kb"] = int(flash.group(1))

    ram = re.search(r"(\d+)\s*KB\s*RAM", text, re.IGNORECASE)
    if ram:
        result["ram_kb"] = int(ram.group(1))

    if re.search(r"\bCAN\b", text):
        result["can"] = True

    vdd = re.search(r"(\d\.\d+)\s*V\s*to\s*(\d\.\d+)\s*V", text)
    if vdd:
        result["vdd_min"] = float(vdd.group(1))
        result["vdd_max"] = float(vdd.group(2))

    return result
