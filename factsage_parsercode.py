import re
import sys
import os

# Helper: scientific notation → float

def sci(text):
    try:
        return float(text.replace('E', 'e').replace('D', 'e'))
    except:
        return 0.0


# Parse one temperature block

def parse_block(block_text, temperature):

    result = {
        "T_C": temperature,
        "mol_H2_gas": 0.0,
        "mol_H2O_gas": 0.0,
        "mol_serpentine": 0.0,
        "mol_magnetite": 0.0,
        "mol_brucite": 0.0,
        "mol_talc": 0.0,
        "mol_SiO2": 0.0,
        "mol_H2O_remaining": 0.0,
        "mol_olivine": 0.0,
        "H2_yield_mL_g": 0.0,
    }

    #  GAS PHASE 
    gas_block = re.search(r'PHASE:\s*gas_ideal(.*?)(?=PHASE:|$)', block_text, re.DOTALL)

    if gas_block:
        gb = gas_block.group(1)

        h2 = re.search(r'^\s*H2\s+([\d.E+\-]+)', gb, re.MULTILINE)
        h2o = re.search(r'^\s*H2O\s+([\d.E+\-]+)', gb, re.MULTILINE)

        if h2:
            result["mol_H2_gas"] = sci(h2.group(1))

        if h2o:
            result["mol_H2O_gas"] = sci(h2o.group(1))

    # fallback for H2
    if result["mol_H2_gas"] == 0.0:
        m = re.search(r'\(\s*([\d.E+\-]+)\s+H2\b', block_text)
        if m:
            result["mol_H2_gas"] = sci(m.group(1))

    # SOLID FINDER 
    def find(patterns):
        for p in patterns:
            m = re.search(p, block_text, re.IGNORECASE)
            if m:
                return sci(m.group(1))
        return 0.0

    # phases
    result["mol_serpentine"] = find([
        r'([\d.E+\-]+)\s+mol\s+Mg3Si2O5\(OH\)4',
        r'Mg3Si2O5\(OH\)4.*\(s\)\s+([\d.E+\-]+)',
    ])

    result["mol_magnetite"] = find([
        r'([\d.E+\-]+)\s+mol\s+Fe3O4',
        r'Fe3O4\(s\)\s+([\d.E+\-]+)',
    ])

    result["mol_brucite"] = find([
        r'([\d.E+\-]+)\s+mol\s+Mg\(OH\)2',
        r'Mg\(OH\)2.*\(s\)\s+([\d.E+\-]+)',
    ])

    result["mol_talc"] = find([
        r'([\d.E+\-]+)\s+mol\s+Mg3Si4O10',
        r'Mg3Si4O10.*\(s\)\s+([\d.E+\-]+)',
    ])

    result["mol_SiO2"] = find([
        r'([\d.E+\-]+)\s+mol\s+SiO2',
        r'SiO2.*\(s\)\s+([\d.E+\-]+)',
    ])

    # H2O FIX (IMPORTANT) 
    h2o_liq = find([
        r'([\d.E+\-]+)\s+mol\s+H2O_liquid',
        r'H2O_liquid\(liq\)\s+([\d.E+\-]+)',
    ])

    result["mol_H2O_remaining"] = h2o_liq + result["mol_H2O_gas"]

    # OLIVINE 
    olivine_block = re.search(r'PHASE:\s*Olivine(.*?)(?=PHASE:|$)', block_text, re.DOTALL)

    if olivine_block:
        t = re.search(r'TOTAL:\s+([\d.E+\-]+)', olivine_block.group(1))
        if t:
            result["mol_olivine"] = sci(t.group(1))

    if result["mol_olivine"] == 0.0:
        m = re.search(r'([\d.E+\-]+)\s+mol\s+Olivine', block_text)
        if m:
            result["mol_olivine"] = sci(m.group(1))

    # H2 YIELD 
    ROCK_MASS = 77.136
    result["H2_yield_mL_g"] = round(result["mol_H2_gas"] * 22400 / ROCK_MASS, 4)

    return result

# Split blocks by temperature
def split_into_blocks(text):

    pattern = re.compile(r'T\s*=\s*(\d+)\s*C')
    matches = list(pattern.finditer(text))

    blocks = []

    for i, m in enumerate(matches):
        start = m.start()
        temp = int(m.group(1))
        end = matches[i+1].start() if i+1 < len(matches) else len(text)

        blocks.append((temp, text[start:end]))

    return blocks



# MAIN

def main(filepath):

    if not os.path.exists(filepath):
        print("File not found")
        return

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    blocks = split_into_blocks(content)

    rows = [parse_block(b, t) for t, b in blocks]

    #  HEADER (YOUR FORMAT) 
    header = (
        f"{'T (°C)':>8} | {'mol H₂(g)':>12} | {'mol Serpentine':>16} | "
        f"{'mol Magnetite Fe₃O₄':>22} | {'mol Brucite Mg(OH)₂':>22} | "
        f"{'mol Talc':>10} | {'mol SiO₂':>10} | "
        f"{'mol H₂O remaining':>18} | {'mol Olivine remaining':>20} | "
        f"{'H₂ yield mL/g rock':>20}"
    )

    print("\n" + "=" * len(header))
    print(header)
    print("=" * len(header))

    for r in rows:
        print(
            f"{r['T_C']:>8} | "
            f"{r['mol_H2_gas']:>12.6f} | "
            f"{r['mol_serpentine']:>16.6f} | "
            f"{r['mol_magnetite']:>22.6f} | "
            f"{r['mol_brucite']:>22.6f} | "
            f"{r['mol_talc']:>10.6f} | "
            f"{r['mol_SiO2']:>10.6f} | "
            f"{r['mol_H2O_remaining']:>18.6f} | "
            f"{r['mol_olivine']:>20.6f} | "
            f"{r['H2_yield_mL_g']:>20.4f}"
        )

    print("=" * len(header))


# YAYY
if __name__ == "__main__":
    file = sys.argv[1] if len(sys.argv) > 1 else "factsage_output.txt"
    main(file)