import sqlite3
from module.lib import read_json_file, show_menu, check_login, create_db_and_table, import_data, show_data, add_data, modi_data, check_phone, delete_data

def main():
    # Connect to DB
    conn = sqlite3.connect("wanghong.db")
    
    # 讀取登入資訊
    account  = input("請輸入帳號：")
    password = input("請輸入密碼：")
    password_list = read_json_file('pass.json')
    if not check_login(account, password, password_list):
        print("=>帳密錯誤，程式結束")
        exit(1)
    
    # Show 選單讀取用戶輸入
    while True:
        show_menu()
        user_select = input("請輸入您的選擇  [0-7]:")
        if user_select == "0": break
        elif user_select == "1": create_db_and_table(conn)
        elif user_select == "2": import_data(conn)
        elif user_select == "3": show_data(conn)
        elif user_select == "4": add_data(conn)    
        elif user_select == "5": modi_data(conn)
        elif user_select == "6": check_phone(conn)
        elif user_select == "7": delete_data(conn)
        else: 
            print("=>無效的選擇\n")
    
    # 關閉連綫
    conn.close()
#with a 

if __name__ == "__main__":
    main()
