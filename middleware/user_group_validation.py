
def is_customer(user):
    if not user.groups.all():
        return True
    else:
        return False


def is_staff(user, group):
    if user.groups.all() and user.groups.all()[0].name == group:
        return True
    else:
        return False
