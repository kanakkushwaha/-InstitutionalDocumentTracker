from app import create_app, db, seed

app = create_app()
ctx = app.app_context()
ctx.push()

try:
    print("Dropping all tables with TRUNCATE...")
    
    # List of all tables (in dependency order)
    tables = [
        'documents', 'users', 'departments', 'admin',
        'students', 'teachers', 'placements', 'scholarships'
    ]
    
    with db.engine.connect() as conn:
        # First, create a transaction and disable FK checks within it
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
    seed.seed_database()
    print("✓ Database seeded")
    
    print("\n✓✓✓ Database reset and seeded successfully! ✓✓✓")
    print("\nNow restart the Flask server and login again with:")
    print("  Email: placement.kabir@institution.edu")
    print("  Password: place-kabir1")
    print("\nOR")
    print("  Email: scholarship.neha@institution.edu")
    print("  Password: schol-neha1")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
