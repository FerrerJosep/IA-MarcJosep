def infer_memory(title):
    match = re.search(r"\b(1|32|64|128|256|512|1024)\s?(GB|TB)\b", title, re.IGNORECASE)
    if match:
        if(match.group(2).upper()=="TB"):
            memory = match.group(1)*1024
        else:
            memory = match.group(1)
        return memory
    return "null"