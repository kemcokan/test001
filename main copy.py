import sqlite3
import streamlit as st
import datetime
import random

# データベース接続
conn = sqlite3.connect('kemcokan.db')
cur = conn.cursor()

# # ユーザーテーブルの作成
# cur.execute("""CREATE TABLE IF NOT EXISTS users (
#   User_id INTEGER PRIMARY KEY AUTOINCREMENT,
#   Username TEXT NOT NULL,
#   Password TEXT NOT NULL);""")

# # チャットテーブルの作成
# cur.execute("""CREATE TABLE IF NOT EXISTS chat (
#   Timestamp TEXT NOT NULL,
#   User_id INTEGER NOT NULL,
#   User_message TEXT,
#   Bot_message TEXT);""")


# ユーザー認証
def authenticate_user(username, password):
  cur.execute("""SELECT * 
                 FROM users
                 WHERE Username=? AND Password=?;""",
                 (username, password))
  return cur.fetchone()

# ユーザー登録
# def register_user(username, password):
#   user = authenticate_user(username, password)
#   if user:
#     # すでに登録済みのユーザーです。
#     pass
#   else:
#     cur.execute("""INSERT INTO users
#                    (Username, Password)
#                    VALUES (?, ?);""",
#                    (username, password))
#     conn.commit()

# カスタムアダプターを作成
def adapt_datetime(dt):
  return dt.isoformat(' ')  # ISO形式の文字列に変換

# カスタムアダプターを登録
sqlite3.register_adapter(datetime.datetime, adapt_datetime)

# メッセージ登録
# def register_message(user_id, user_message, bot_message,):
#   # 現在の日時をローカル時間で取得
#   now = datetime.datetime.now()

#   cur.execute("""INSERT INTO chat
#                  VALUES (?, ?, ?, ?);""",
#                  (now, user_id, user_message, bot_message ))
#   conn.commit()

# 全チャットデータの取得
# def get_all_chat(user_id):
#   cur.execute("""SELECT * 
#                  FROM chat
#                  WHERE User_id = ?
#                  ORDER BY Timestamp;""",
#                  (user_id, ))
#   return cur.fetchall()



if 'login' not in st.session_state:
  
  # # テスト用のユーザーとパスワードを作成
  # register_user('ROBO', '1234');
  # register_user('ITO', '1234');
  # register_user('SATO', '1234');

  # タイトル
  st.title("KEMCOKAN")

  # ログイン画面
  with st.form('login_form'):
    username = st.text_input('ユーザーID')
    password = st.text_input('パスワード', type='password')
    submit_btn = st.form_submit_button('ログイン')
  if submit_btn:
    user = authenticate_user(username, password)
    if user:
      st.session_state.login = user[0]
      st.session_state.username = user[1]
      st.rerun() # チャット画面に切り替え
    else:
      st.error('IDまたはパスワードが間違っています。')

elif st.session_state.login > 1:
  st.title("Login完了！")
  st.write("こんにちは、", st.session_state.username, "さん")
  
  # # 過去のチャットを表示
  # all_message = get_all_chat(st.session_state.login)
  # for row in all_message:
  #   with st.chat_message('user'):
  #     st.markdown(row[2])
  #   with st.chat_message('assistant'):
  #     st.markdown(row[3])

  # if prompt := st.chat_input('メッセージを入力してください：'):
  #   bot_message = random.choice(robot_message)
  #   register_message(st.session_state.login, prompt, bot_message)
  #   with st.chat_message('user'):
  #     st.markdown(prompt)
  #   with st.chat_message('assistant'):
  #     st.markdown(bot_message)

# 接続の切断
conn.close()
