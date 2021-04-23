from pwnc.pwnc import query
desired_symbols = ["system", "strcat"]
known_symbols = {"strncpy": "0xdb0", "strcat": "0xd800"}
results = query(desired_symbols, known_symbols)
print(f"System = {hex(int(results['system'], 16))}")
print(f"Strcat = {hex(int(results['strcat'], 16))}")
