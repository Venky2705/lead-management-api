from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.schemas import LeadCreate

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Lead API Running"
    }


@app.get("/db-check")
def db_check():

    with engine.connect() as conn:

        result = conn.execute(
            text("SELECT version();")
        )

        version = result.fetchone()

        return {
            "postgres_version": version[0]
        }


@app.get("/leads")
def get_leads():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    id,
                    company,
                    contact_name,
                    email,
                    country,
                    status
                FROM leads
                ORDER BY id
            """)
        )

        rows = result.fetchall()

        return [
            {
                "id": row.id,
                "company": row.company,
                "contact_name": row.contact_name,
                "email": row.email,
                "country": row.country,
                "status": row.status
            }
            for row in rows
        ]


@app.post("/leads")
def create_lead(lead: LeadCreate):

    with engine.connect() as conn:

        conn.execute(
            text("""
                INSERT INTO leads
                (
                    company,
                    contact_name,
                    email,
                    country,
                    status
                )
                VALUES
                (
                    :company,
                    :contact_name,
                    :email,
                    :country,
                    :status
                )
            """),
            {
                "company": lead.company,
                "contact_name": lead.contact_name,
                "email": lead.email,
                "country": lead.country,
                "status": lead.status
            }
        )

        conn.commit()

        return {
            "message": "Lead created successfully"
        }


@app.put("/leads/{lead_id}")
def update_lead(
    lead_id: int,
    lead: LeadCreate
):

    with engine.connect() as conn:

        conn.execute(
            text("""
                UPDATE leads
                SET
                    company = :company,
                    contact_name = :contact_name,
                    email = :email,
                    country = :country,
                    status = :status
                WHERE id = :lead_id
            """),
            {
                "lead_id": lead_id,
                "company": lead.company,
                "contact_name": lead.contact_name,
                "email": lead.email,
                "country": lead.country,
                "status": lead.status
            }
        )

        conn.commit()

        return {
            "message": "Lead updated successfully"
        }


@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: int):

    with engine.connect() as conn:

        conn.execute(
            text("""
                DELETE FROM leads
                WHERE id = :lead_id
            """),
            {
                "lead_id": lead_id
            }
        )

        conn.commit()

        return {
            "message": "Lead deleted successfully"
        }