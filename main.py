import sqlite3
import streamlit as st
import datetime
import random

# データベース接続
conn = sqlite3.connect('kemcokan.db')
cur = conn.cursor()


# ユーザー認証
def authenticate_user(username, password):
  cur.execute("""SELECT * 
                 FROM users
                 WHERE Username=? AND Password=?;""",
                 (username, password))
  return cur.fetchone()


# カスタムアダプターを作成
def adapt_datetime(dt):
  return dt.isoformat(' ')  # ISO形式の文字列に変換

# カスタムアダプターを登録
sqlite3.register_adapter(datetime.datetime, adapt_datetime)



# login
# というkeyがない
if 'login' not in st.session_state:
  st.title("KEMCOKAN")
  
  # ログイン画面
  with st.form('login_form'):
    username = st.text_input('ユーザーID')
    password = st.text_input('パスワード', type='password')
    submit_btn = st.form_submit_button('ログイン')
  if submit_btn:
    user = authenticate_user(username, password)
    if user:
      #st.session_state.login = user[0]
      st.session_state.login = 'login'
      st.session_state.username = user[1]
      st.rerun()	# LOGIN先へ切り替え
    else:
      st.error('IDまたはパスワードが間違っています。')

#elif st.session_state.login > 1:
elif st.session_state.login == 'login':
	st.title("売上分析")
	st.write("こんにちは、", st.session_state.username, "さん。")
  
	# ログアウト
	btn_logout = st.button('ログアウト')
	if btn_logout:
		keys = list(st.session_state.keys())
		for key in keys:
			del st.session_state[key]
		st.rerun()

	# ここから、ログイン後の処理
	st.write('OK!')


# 接続の切断
conn.close()
