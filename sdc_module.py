import os
import json
from openpyxl import Workbook, load_workbook
from encryption_module import encrypt_data
from acm_module import generate_acm

DATA_DIR = "data"
DEFAULT_SDC_PATH = os.path.join(DATA_DIR, "SecureDataContainer.xlsx")


def _embed_acm_in_workbook(wb: Workbook, acm: dict):
    acm_ws = wb.create_sheet("_ACM")
    acm_ws.sheet_state = "hidden"

    roles = list(acm.keys())
    sheets = sorted({sheet for perms in acm.values() for sheet in perms})

    acm_ws.append(["Role"] + sheets)

    for role in roles:
        #row = [role] + [acm[role].get(sheet, "") for sheet in sheets]
        row = [role] + [("read" if sheet in acm[role] else "") for sheet in sheets]
        acm_ws.append(row)


def create_sdc(output_file=DEFAULT_SDC_PATH):
    os.makedirs(DATA_DIR, exist_ok=True)
    wb = Workbook()
    sheet_names = ["Sheet1", "Sheet2", "Sheet3", "Sheet4", "Sheet5"]
    ws = wb.active
    ws.title = sheet_names[0]

    for name in sheet_names[1:]:
        wb.create_sheet(title=name)

    for sheet in wb.sheetnames:
        if sheet != "_ACM":
            ws = wb[sheet]
            for row in range(1, 6):
                ws[f"A{row}"] = f"This is {sheet} - Row {row}"

    # Encrypt each sheet with a unique key
    keys = {}
    for sheet in sheet_names:
        ws = wb[sheet]
        key = os.urandom(32)
        keys[sheet] = key.hex()
        for row in ws.iter_rows():
            for cell in row:
                if cell.value:
                    cell.value = encrypt_data(key, str(cell.value))

    # Save keys externally
    key_file = output_file.replace(".xlsx", "_keys.json")
    with open(key_file, "w") as f:
        json.dump(keys, f)

    # Generate and embed ACM
    acm = generate_acm(sheet_names)
    _embed_acm_in_workbook(wb, acm)

    wb.save(output_file)
    print(f"Blank SDC created at: {output_file}")


def encrypt_existing_excel(file_path, sdc_name="default_sdc"):
    sdc_dir = f"data/sdcs/{sdc_name}"
    os.makedirs(sdc_dir, exist_ok=True)

    output_file = os.path.join(sdc_dir, "SecureDataContainer.xlsx")
    wb = load_workbook(file_path)
    keys = {}

    for sheet in wb.sheetnames:
        if sheet.startswith("_"):
            continue
        ws = wb[sheet]
        key = os.urandom(32)
        keys[sheet] = key.hex()
        for row in ws.iter_rows():
            for cell in row:
                if cell.value:
                    cell.value = encrypt_data(key, str(cell.value))

    # Save keys externally
    key_file = output_file.replace(".xlsx", "_keys.json")
    with open(key_file, "w") as f:
        json.dump(keys, f)

    # Generate and embed ACM
    acm = generate_acm(wb.sheetnames)
    _embed_acm_in_workbook(wb, acm)

    wb.save(output_file)
    print(f"Encrypted SDC saved to: {output_file}")
