ROLES = (
    SYSTEM_ROLE,
    PARENT_ROLE,
    CHILD_ROLE
    ) = (
        (ACCESS_LEVEL_SYSTEM_ROLE, NAME_SYSTEM_ROLE),
        (ACCESS_LEVEL_PARENT_ROLE, NAME_PARENT_ROLE),
        (ACCESS_LEVEL_CHILD_ROLE, NAME_CHILD_ROLE)
    ) = (
        (0, 'system'),
        (1, 'parent'),
        (2, 'child'))

LEAST_PRIVILEGED_ROLE = ROLES[-1]
GUEST_ROLE = (LEAST_PRIVILEGED_ROLE[0] + 1, 'guest')


class InvalidRole(Exception):
    pass


def find_role_by_access_level(access_level):
    role = None
    try:
        role = next((role for role in ROLES if role[0] == access_level))
    except StopIteration:
        raise InvalidRole(
            "Can't find role with {0} access level".format(access_level))

    return role


def find_role_by_name(name):
    role = None
    try:
        role = next((role for role in ROLES if role[1] == name))
    except StopIteration:
        raise InvalidRole(
            "Can't find role with {0} name".format(name))

    return role


def find_role(criteria):
    role = None
    try:
        sanitized_criteria = (tuple(criteria) if isinstance(criteria, list)
                              else criteria)
        ROLES.index(sanitized_criteria)
        role = sanitized_criteria
    except ValueError:
        if isinstance(criteria, basestring):
            role = find_role_by_name(criteria)
        elif isinstance(criteria, int):
            role = find_role_by_access_level(criteria)
        else:
            raise InvalidRole(
                "Can't find role with {0} criteria".format(criteria))

    return role


def is_more_privileged_than(left, right):
    return find_role(left) <= find_role(right)


def is_less_privileged_than(left, right):
    return not is_more_privileged_than(left, right)
