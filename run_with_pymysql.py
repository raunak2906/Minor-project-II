import pymysql
# Monkey-patch to make pymysql act as MySQLdb
pymysql.install_as_MySQLdb()

# Now import the original main app
# This will execute the app creation and db configuration
try:
    import main
except ImportError as e:
    print(f"Error importing main.py: {e}")
    exit(1)

if __name__ == "__main__":
    print("Starting NovaMart (Orma) Application via PyMySQL Wrapper...")
    # Using port 5001 to avoid potential conflicts with Port 80
    main.app.run(host='0.0.0.0', port=5001, debug=True)
