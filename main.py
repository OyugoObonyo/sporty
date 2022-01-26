from app import create_app, db

app = create_app()
if db is None:
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
