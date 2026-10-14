import clinics
def build():
    S = {}
    S.update(clinics.build_for(['patterns-clinic'], 'pa'))
    return S
