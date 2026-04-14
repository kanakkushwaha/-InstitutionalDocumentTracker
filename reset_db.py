from app import create_app, db
from app.seed import ensure_seed_data

app = create_app()
ctx = app.app_context()
ctx.push()

try:
    print("Dropping all tables with TRUNCATE...")

    tables = [
        'documents', 'users', 'departments', 'admin',
        'students', 'teachers', 'placements', 'scholarships'
    ]

    with db.engine.connect() as conn:
        trans = conn.begin()

        conn.execute(db.text("SET FOREIGN_KEY_CHECKS=0"))

        for table in tables:
            try:
                conn.execute(db.text(f"DROP TABLE IF EXISTS {table}"))
                print(f"  ✓ Dropped {table}")
            except Exception as e:
                print(f"  - {table}: {e}")

        conn.execute(db.text("SET FOREIGN_KEY_CHECKS=1"))
        trans.commit()

    print("\nCreating all tables...")
    db.create_all()
    print("✓ Tables created")

    print("\nSeeding database...")
    ensure_seed_data(app)
    print("✓ Database seeded")

    print("\n✓✓✓ Database reset and seeded successfully! ✓✓✓")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()