class Roles:
    ADMIN = 'admin'
    USERS = 'users'
    SUPER_ADMIN = 'super_admin'

ROLES_WEIGHT = {
    Roles.SUPER_ADMIN: 3,
    Roles.ADMIN: 2,
    Roles.USERS: 1
}
    

class RolesMethod:
    CREATE = 'CREATE'
    READ = 'READ'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'