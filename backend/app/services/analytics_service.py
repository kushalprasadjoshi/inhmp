from sqlalchemy.orm import Session
from sqlalchemy import text

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_disease_summary(self):
        sql = text("""
            SELECT h.district, v.diagnosis_code, COUNT(*) as cases
            FROM visit v
            JOIN hospital h ON v.hospital_id = h.id
            WHERE v.visit_date >= CURDATE() - INTERVAL 7 DAY
            GROUP BY h.district, v.diagnosis_code
            ORDER BY cases DESC
            LIMIT 20
        """)
        result = self.db.execute(sql)
        return [{"district": row[0], "diagnosis_code": row[1], "cases": row[2]} for row in result]

    def get_trends(self):
        sql = text("""
            SELECT WEEK(v.visit_date) as week, COUNT(*) as cases
            FROM visit v
            WHERE v.diagnosis_code LIKE 'J%'  -- respiratory
              AND v.visit_date >= DATE_SUB(NOW(), INTERVAL 12 WEEK)
            GROUP BY WEEK(v.visit_date)
            ORDER BY week
        """)
        result = self.db.execute(sql)
        return [{"week": row[0], "cases": row[1]} for row in result]

    def get_outbreak_alerts(self):
        sql = text("""
            SELECT h.district, DATE(v.visit_date) as date, COUNT(*) as daily_cases,
                   AVG(COUNT(*)) OVER (PARTITION BY h.district ORDER BY v.visit_date ROWS 4 PRECEDING) as avg_4day
            FROM visit v
            JOIN hospital h ON v.hospital_id = h.id
            WHERE v.visit_date >= CURDATE() - INTERVAL 14 DAY
            GROUP BY h.district, DATE(v.visit_date)
            HAVING daily_cases > avg_4day * 2
            ORDER BY date DESC
        """)
        result = self.db.execute(sql)
        return [{"district": row[0], "date": row[1], "daily_cases": row[2], "avg_4day": float(row[3])} for row in result]