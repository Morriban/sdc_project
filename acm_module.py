# This function creates the ACM based on the inputted sheet names, with each role having access to a different amount.
def generate_acm(sheet_names):
    return {
        "administrator": sheet_names,
        "privileged user": sheet_names[:3],
        "user": sheet_names[:2],
        "guest": [sheet_names[0]]
    }


# This function will return a given the sheets that can be access for a given role in an ACM
def get_accessible_sheets(acm_dict, role):
    return acm_dict.get(role, [])
