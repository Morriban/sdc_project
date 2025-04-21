def generate_acm(sheet_names):
    """
    Generates an Access Control Matrix (ACM) dictionary based on the given sheet names.
    """
    return {
        "administrator": sheet_names,
        "privileged user": sheet_names[:3],
        "user": sheet_names[:2],
        "guest": [sheet_names[0]]
    }

def get_accessible_sheets(acm_dict, role):
    """
    Given a loaded ACM dictionary and role, returns accessible sheet names.
    """
    return acm_dict.get(role, [])
