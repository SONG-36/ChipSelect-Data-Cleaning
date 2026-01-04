def resolve_max_freq(candidates):
    """
    candidates: list of dicts with keys:
      - value (int/float)
      - context (str)
    """
    if not candidates:
        return None

    accepted_keywords = [
        "main feature", "general description", "overview", "key feature"
    ]
    rejected_keywords = [
        "low power", "sleep", "typical", "example",
        "test", "peripheral", "bus"
    ]

    accepted = []
    for c in candidates:
        ctx = (c.get("context") or "").lower()
        if any(rk in ctx for rk in rejected_keywords):
            continue
        if any(ak in ctx for ak in accepted_keywords):
            accepted.append(c)

    if not accepted:
        return None

    return max(c["value"] for c in accepted)
