
def sort_fleet_offers(offers):
    """Sort fleet offers function."""
    return sorted(offers, key=lambda g: g.total_price)[:20]
