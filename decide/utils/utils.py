
def get_ids(ids):
    return [int(i) for i in ids.split(",") if str.isdigit(i)]
