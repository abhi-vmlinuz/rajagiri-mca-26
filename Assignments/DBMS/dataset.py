import pandas as pd
import oracledb

# --- CONFIGURATION ---
EXCEL_FILE = "Dataset.xlsx"  # Change to .xlsx if your file ends with .xlsx
DB_USER = "mca"   # e.g., "system" or your created user
DB_PASS = "mca"
DB_DSN = "localhost:1521/FREEPDB1"  # Adjust PDB service name if needed

def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)

def find_sheet(excel, target_names):
    """Finds a sheet name in the workbook ignoring case and whitespace."""
    for sheet in excel.sheet_names:
        clean_sheet = str(sheet).strip().lower()
        for target in target_names:
            if clean_sheet == target.lower():
                return sheet
    raise ValueError(f"Could not find sheet matching {target_names}. Available sheets: {excel.sheet_names}")

def clean_val(val):
    """Utility to convert pandas NaN / NaT into None for SQL NULL."""
    if pd.isna(val):
        return None
    if isinstance(val, pd.Timestamp):
        return val.to_pydatetime().date()
    return str(val).strip() if isinstance(val, str) else val

def get_col_val(row, possible_keys):
    """Finds first matching column key in row, returns clean_val."""
    for key in possible_keys:
        for col in row.index:
            if str(col).strip().upper() == key.upper():
                return clean_val(row[col])
    return None

def import_data():
    excel = pd.ExcelFile(EXCEL_FILE)
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # -------------------------------------------------------------
        # 1. DEPARTMENT TABLE
        # -------------------------------------------------------------
        dept_sheet = find_sheet(excel, ['dept', 'department'])
        print(f"Importing DEPARTMENT (from sheet '{dept_sheet}')...")
        df_dept = excel.parse(dept_sheet, header=1).dropna(how='all')
        
        dept_data = []
        for _, row in df_dept.iterrows():
            dept_no = get_col_val(row, ['DEPTNO', 'DEPT_NO'])
            if not dept_no:
                continue
            dept_data.append((
                dept_no,
                get_col_val(row, ['DEPTNAME', 'DEPT_NAME']),
                None,  # HOD_NAME (Not in Excel)
                get_col_val(row, ['LOCATION'])
            ))
        
        cursor.executemany(
            "INSERT INTO DEPARTMENT (DEPTNO, DEPTNAME, HOD_NAME, LOCATION) VALUES (:1, :2, :3, :4)",
            dept_data
        )
        print(f"-> Inserted {len(dept_data)} departments.")

        # -------------------------------------------------------------
        # 2. EMPLOYEE TABLE
        # -------------------------------------------------------------
        emp_sheet = find_sheet(excel, ['employee', 'emp'])
        print(f"Importing EMPLOYEE (from sheet '{emp_sheet}')...")
        df_emp = excel.parse(emp_sheet, header=1).dropna(how='all')

        def format_phone(val):
            if pd.isna(val) or val is None:
                return None
            if isinstance(val, (float, int)):
                return str(int(val))[:10]
            val_str = str(val).strip().split('.')[0]
            return val_str[:10]

        emp_data = []
        for _, row in df_emp.iterrows():
            emp_no = get_col_val(row, ['EMPNO', 'EMP_NO'])
            if not emp_no:
                continue
            
            hire_date = pd.to_datetime(get_col_val(row, ['HIREDATE', 'HIRE_DATE']), errors='coerce')
            dob = pd.to_datetime(get_col_val(row, ['BIRTHDATE', 'DOB']), errors='coerce')

            emp_data.append((
                emp_no,
                get_col_val(row, ['FIRSTNME', 'EMPNAME', 'FIRSTNAME']),
                get_col_val(row, ['WORKDEPT', 'DEPTNO']),
                format_phone(get_col_val(row, ['PHONENO', 'MOBILE'])),
                clean_val(hire_date),
                get_col_val(row, ['JOB']),
                get_col_val(row, ['EDLEVEL']),
                get_col_val(row, ['GENDER', 'SEX']),
                clean_val(dob),
                get_col_val(row, ['SALARY']),
                get_col_val(row, ['BONUS']),
                get_col_val(row, ['COMM'])
            ))

        cursor.executemany("""
            INSERT INTO EMPLOYEE 
            (EMPNO, EMPNAME, DEPTNO, MOBILE, HIRE_DATE, JOB, EDLEVEL, GENDER, DOB, SALARY, BONUS, COMM) 
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)
        """, emp_data)
        print(f"-> Inserted {len(emp_data)} employees.")

        # -------------------------------------------------------------
        # 3. PROJECT TABLE
        # -------------------------------------------------------------
        proj_sheet = find_sheet(excel, ['project', 'proj'])
        print(f"Importing PROJECT (from sheet '{proj_sheet}')...")
        df_proj = excel.parse(proj_sheet, header=1).dropna(how='all')

        proj_data = []
        for _, row in df_proj.iterrows():
            proj_no = get_col_val(row, ['PROJNO', 'PROJ_NO'])
            if not proj_no:
                continue

            st_date = pd.to_datetime(get_col_val(row, ['PRSTDATE', 'STDATE', 'STARTDATE', 'START_DATE']), errors='coerce')
            end_date = pd.to_datetime(get_col_val(row, ['PRENDATE', 'ENDDATE', 'END_DATE']), errors='coerce')

            proj_data.append((
                proj_no,
                get_col_val(row, ['PROJNAME', 'PROJ_NAME']),
                get_col_val(row, ['DEPTNO', 'WORKDEPT']),
                get_col_val(row, ['RESPEMP', 'RESEMP', 'RESP_EMP']),
                clean_val(st_date),
                clean_val(end_date)
            ))

        cursor.executemany("""
            INSERT INTO PROJECT 
            (PROJNO, PROJNAME, DEPTNO, RESPEMP, STDATE, ENDDATE) 
            VALUES (:1, :2, :3, :4, :5, :6)
        """, proj_data)
        print(f"-> Inserted {len(proj_data)} projects.")

        # -------------------------------------------------------------
        # 4. EMP_PROJ TABLE
        # -------------------------------------------------------------
        empproj_sheet = find_sheet(excel, ['emp_proj', 'emp_proj ', 'empproj', 'emp-proj', 'emp_project'])
        print(f"Importing EMP_PROJ (from sheet '{empproj_sheet}')...")
        df_empproj = excel.parse(empproj_sheet, header=1).dropna(how='all')
        
        empproj_data = []
        for _, row in df_empproj.iterrows():
            proj_no = get_col_val(row, ['PROJNO', 'PROJ_NO'])
            emp_no = get_col_val(row, ['EMPNO', 'EMP_NO'])
            if not proj_no or not emp_no:
                continue

            empproj_data.append((
                proj_no,
                emp_no,
                get_col_val(row, ['EMPTIME', 'EMP_TIME', 'ACTTIME'])
            ))

        cursor.executemany("""
            INSERT INTO EMP_PROJ (PROJNO, EMPNO, EMPTIME) 
            VALUES (:1, :2, :3)
        """, empproj_data)
        print(f"-> Inserted {len(empproj_data)} employee-project assignments.")

        conn.commit()
        print("\nAll datasets imported successfully!")

    except Exception as e:
        conn.rollback()
        print(f"\nImport failed! Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import_data()