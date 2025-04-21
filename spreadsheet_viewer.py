import json
from openpyxl import load_workbook, Workbook
from encryption_module import decrypt_data


def _load_acm_from_workbook(wb):
    acm_sheet = wb["_ACM"]
    headers = [cell.value for cell in next(acm_sheet.iter_rows(min_row=1, max_row=1))]
    roles = {}
    for row in acm_sheet.iter_rows(min_row=2):
        role = row[0].value
        perms = {}
        for i, cell in enumerate(row[1:], start=1):
            sheet = headers[i]
            if cell.value:
                perms[sheet] = cell.value
        roles[role] = perms
    return roles


def get_accessible_sheets(acm, role):
    return [sheet for sheet, access in acm.get(role, {}).items() if "read" in access.lower()]


def view_sdc(role, input_file):
    output_file = input_file.replace(".xlsx", f"_decrypted_{role}.xlsx")

    # Load external key file
    key_file = input_file.replace(".xlsx", "_keys.json")
    with open(key_file, "r") as f:
        keys = json.load(f)

    # Load workbook and ACM
    wb = load_workbook(input_file)
    acm = _load_acm_from_workbook(wb)
    accessible_sheets = get_accessible_sheets(acm, role)

    decrypted_wb = Workbook()
    decrypted_wb.remove(decrypted_wb.active)

    for sheet in accessible_sheets:
        if sheet not in wb.sheetnames:
            continue
        ws = wb[sheet]
        new_ws = decrypted_wb.create_sheet(sheet)

        key = bytes.fromhex(keys.get(sheet))
        for row in ws.iter_rows():
            new_row = []
            for cell in row:
                if cell.value:
                    try:
                        decrypted_value = decrypt_data(key, cell.value)
                        new_row.append(decrypted_value)
                    except:
                        new_row.append("[DECRYPT_ERROR]")
                else:
                    new_row.append("")
            new_ws.append(new_row)

    decrypted_wb.save(output_file)
    print(f"Decrypted SDC for role '{role}' saved to: {output_file}")
