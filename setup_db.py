import pymysql
import sys

# Connection details from main.py
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'orma'

def run_setup():
    print(f"Attempting to connect to MySQL at {DB_HOST}...")
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
        cursor = conn.cursor()
        print("Connected.")
        
        # Create Database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.select_db(DB_NAME)
        
        # Read SQL file
        with open('orma.sql', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Filter comments and empty lines
        clean_lines = []
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith('--') or line_stripped.startswith('/*'):
                continue
            clean_lines.append(line)
            
        # Join execution content
        sql_content = ''.join(clean_lines)
        statements = sql_content.split(';')
        
        count = 0
        for stmt in statements:
            stmt = stmt.strip()
            if not stmt:
                continue
            
            try:
                cursor.execute(stmt)
                count += 1
            except Exception as e:
                # Check for "Table already exists" (error 1050)
                if '1050' in str(e):
                    print(f"Skipping existing table: {stmt[:30]}...")
                else:
                    print(f"Error executing: {stmt[:50]}...\nReason: {e}")
                    
        conn.commit()
        print(f"Successfully executed {count} statements.")
        
        # Verify
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"Final Tables in '{DB_NAME}': {tables}")
        
        conn.close()
        
    except Exception as e:
        print(f"Setup Error: {e}")

if __name__ == "__main__":
    run_setup()
