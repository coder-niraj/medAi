from datetime import datetime, timezone, timedelta
from repository.guest.index import GuestRepo
from db.session import sessionLocal


def run():
    db = sessionLocal()
    guest_repo = GuestRepo(db)
    print("clean guest table")
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    deleted = guest_repo.delete_guest(date=cutoff)
    print(deleted, " guests are deleted")
    return deleted
