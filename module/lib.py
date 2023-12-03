import json
import sqlite3

conn = sqlite3.connect('wanghong.db')
cursor = conn.cursor()

def read_json_file(file_path) -> list | None:
    """
    Read and load data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Loaded JSON data.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None

def check_login(acc, pwd, password_list) -> bool:
    is_login_success = False
    for account in password_list:
        if account["帳號"] == acc and account["密碼"] == pwd:
            is_login_success = True
            break
    return is_login_success

def import_data(conn: sqlite3.Connection) -> None:
    """
    Args: 
        None
    Returns:
        int: success or error for 0 or 1
    """
    with open("members.txt",encoding='utf-8') as file:
        all_lines = file.read().strip().split('\n')
        for line in all_lines:
            mname, msex, mphone = line.split(",")
            conn.execute(f"INSERT INTO members (mname, msex, mphone) VALUES ('{mname}', '{msex}', '{mphone}')")
        conn.commit()
        
        print(f"=>異動 {all_lines.__len__()} 筆記錄\n")
            
def show_data(conn: sqlite3.Connection) -> None:
    try:
        fetch_results = conn.execute("SELECT * FROM members").fetchall()
        
        if fetch_results.__len__() == 0: raise sqlite3.OperationalError()
        """
        姓名　　　　性別　手機
-----------------------------
        辦公室小野　 F　　0912-345678
        阿神　　　　 M　　0923-456789
        老高　　　　 M　　0934-567890
        黃明志　　　 M　　0945-678901
        蔡阿嘎　　　 F　　0956-789012
        簡單哥　　　 M　　0967-890123
        """
        print("姓名\t\t性別\t手機")
        print("-"*30)
        for id,name,sex,phone in fetch_results:
            print(f"{name:6s}\t{sex}\t{phone}\n")
        # print("\n")

    except sqlite3.OperationalError:
        print("=>查無資料\n")
        
def add_data(conn: sqlite3.Connection) -> None:
    name = input("請輸入姓名: ")
    sex = input("請輸入性別: ")
    phone = input("請輸入手機: ")
    
    cursor = conn.cursor()  # 获取游标对象
    
    try:
        cursor.execute("INSERT INTO members(mname, msex, mphone) VALUES (?, ?, ?)", (name, sex, phone))
        conn.commit()
        print("=>異動 1 筆記錄\n")
    except sqlite3.Error as e:
        print(f"Error inserting record: {e}")

def modi_data(conn: sqlite3.Connection) -> None:
    """
    Args:
        conn (sqlite3.Connection): SQLite 连接对象
        record_id (int): 要修改的记录 ID
        new_name (str): 新姓名
        new_sex (str): 新性别
        new_phone (str): 新电话号码
    Returns:
        None
        record_id: int, new_name: str, new_sex: str, new_phone: str
    """
    cursor = conn.cursor()  # 获取游标对象
    old_name = input("請輸入想修改記錄的姓名:")
    # print("ooooo:" + old_name + "123")
    if old_name != (None or ''):
        cursor.execute(f"SELECT * FROM members WHERE mname=\"{old_name}\"")
        conn.commit()
        db = cursor.fetchall()[0]
        # print(f"DB:{db}")
        if db == None:
            print("=>必須指定姓名才可修改記錄")
        else:
            sex = input("請輸入要改變的性別:")
            phone= input("請輸入要改變的手機:")
            try:
                
                # print(type(db))
                # print(len(db))
                # print(db)
                print("原資料：")
                print(f"\t姓名:{db[1]:4s},性別:{db[2]:2s},手機{db[3]:3s}")
                cursor.execute("UPDATE members SET msex=?, mphone=? WHERE mname=?", (sex, phone,old_name))
                conn.commit()
                print("=>異動 1 筆記錄")
                print("修改後資料：")
                print(f"\t姓名:{db[1]:4s},性別:{sex:2s},手機{phone:3s}\n")
                # print("Record modified successfully.")

            except sqlite3.Error as e:
                print(f"Error modifying record: {e}")
    else:
        print("=>必須指定姓名才可修改記錄\n")
        
    cursor.close()  # 关闭游标

def check_phone(conn: sqlite3.Connection) -> None:
    """
    Args:
        conn (sqlite3.Connection): SQLite 连接对象
    Returns:
        None
    """
    cursor = conn.cursor()  # 获取游标对象
    
    phone = input("請輸入想查詢記錄的手機: ")
    
    try:
        cursor.execute("SELECT * FROM members WHERE mphone=?", (phone,))
        records = cursor.fetchall()
        
        if not records:
            print("No record found with the given phone number.")
        else:
            print("姓名\t\t性別\t手機")
            print("-"*30)
            for id,name,sex,phone in records:
                print(f"\n{name:6s}\t{sex}\t{phone}\n")
    except sqlite3.Error as e:
        print(f"Error searching records: {e}")
    
    cursor.close()  # 关闭游标
            
def delete_data(conn: sqlite3.Connection) -> None:
    """
    Args:
        conn (sqlite3.Connection): SQLite 连接对象
    Returns:
        None
    """
    cursor = conn.cursor()  # 获取游标对象
    
    #confirmation = input("Are you sure you want to delete all records? (yes/no): ")
    
    try:
        #if confirmation.lower() == "yes":
            cursor.execute("SELECT COUNT (*) FROM members")
            conn.commit()
            rowcount = cursor.fetchone()[0]
            # print ("1321321321:" + str(rowcount))       
            cursor.execute("DELETE FROM members")
            conn.commit()
            print(f"=>異動{rowcount}筆記錄\n")
        #else:
            #print("Deletion cancelled.")
    except sqlite3.Error as e:
        print(f"Error deleting records: {e}")
    
    cursor.close()  # 关闭游标

def create_db_and_table(conn: sqlite3.Connection) -> sqlite3.Connection:
    conn.execute('''CREATE TABLE IF NOT EXISTS members(
                    iid    INTEGER    PRIMARY KEY    AUTOINCREMENT,
                    mname  TEXT    NOT NULL,
                    msex   TEXT    NOT NULL,
                    mphone TEXT    NOT NULL
                )''')
    conn.commit()
    print("=>資料庫已建立\n")
    return conn

def show_menu():
    print("---------- 選單 ----------")
    print("0 / Enter 離開")
    print("1 建立資料庫與資料表")
    print("2 匯入資料")
    print("3 顯示所有紀錄")
    print("4 新增記錄")
    print("5 修改記錄")
    print("6 查詢指定手機")
    print("7 刪除所有記錄")     
    print("--------------------------")