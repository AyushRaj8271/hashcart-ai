class Roles:
    ADMIN = "admin"
    SHOPPER = "shopper"
    BUSINESS = "business"

class Accesses:
    HASHCART = "hashcart"
    EXPENSE_TRACKER = "expense_tracker"
    # CALENDAR = "calendar_events"
    CALENDAR = "calendar"

ROLE_ACCESS = {
    Roles.ADMIN: [Accesses.HASHCART, Accesses.EXPENSE_TRACKER, Accesses.CALENDAR],
    Roles.SHOPPER: [Accesses.HASHCART, Accesses.EXPENSE_TRACKER],
    Roles.BUSINESS: [Accesses.CALENDAR],
}