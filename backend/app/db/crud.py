from typing import List, Optional
from sqlmodel import Session, select
from app.models.db_models import ScanRecordDB

def save_scan(session: Session, record: ScanRecordDB) -> ScanRecordDB:
    """Save a scan record to the database."""
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

def get_recent_scans(session: Session, limit: int = 20) -> List[ScanRecordDB]:
    """Retrieve the most recent scan records, ordered by creation time descending."""
    statement = select(ScanRecordDB).order_by(ScanRecordDB.createdAt.desc()).limit(limit)
    results = session.exec(statement)
    return list(results.all())

def get_scan_by_id(session: Session, scan_id: str) -> Optional[ScanRecordDB]:
    """Retrieve a single scan record by its unique ID."""
    statement = select(ScanRecordDB).where(ScanRecordDB.id == scan_id)
    result = session.exec(statement).first()
    return result

def update_report_text(session: Session, scan_id: str, report_text: str) -> Optional[ScanRecordDB]:
    """Update the reportText field of an existing scan record. Overwrites if already set."""
    record = get_scan_by_id(session, scan_id)
    if not record:
        return None
    record.reportText = report_text
    session.add(record)
    session.commit()
    session.refresh(record)
    return record
