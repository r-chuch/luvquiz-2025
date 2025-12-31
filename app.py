import streamlit as st
import pandas as pd

# --- 網頁配置 ---
st.set_page_config(page_title="2025 沛辰與峪銓的真愛大考驗", page_icon="💖", layout="centered")

# --- 甜蜜風格 CSS (最終強化版：徹底杜絕白色文字) ---
st.markdown("""
    <style>
    /* 1. 強制背景顏色 */
    .stApp {
        background-color: #fff5f7 !important;
    }

    /* 2. 最嚴格的全域文字鎖定：將所有標準文字元素強制設為深灰色 */
    html, body, [data-testid="stAppViewContainer"], .stApp, .stApp p, .stApp span, .stApp label, .stApp li {
        color: #31333f !important;
    }

    /* 3. 標題與重點文字強制鎖定 */
    .main-title {
        color: #ff4b82 !important; /* 主標題用粉紅色 */
        text-align: center;
        font-family: 'Microsoft JhengHei', sans-serif;
        font-weight: bold;
        padding: 20px;
        margin-bottom: 10px;
        display: block;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #31333f !important;
    }

    /* 4. 區塊樣式強制白色背景 */
    .question-box, .feedback-box, .result-card {
        background-color: white !important;
        color: #31333f !important;
    }

    .question-box {
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(255, 75, 130, 0.1);
        margin-bottom: 20px;
        border-left: 10px solid #ffb6c1;
    }

    .feedback-box {
        text-align: center;
        padding: 30px;
        border-radius: 25px;
        border: 3px solid #ffb6c1;
        box-shadow: 0 10px 25px rgba(255, 182, 193, 0.3);
    }

    .category-badge {
        background-color: #ff8fa3 !important;
        color: white !important;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.8em;
        margin-bottom: 10px;
        display: inline-block;
    }

    .hint-text {
        color: #888888 !important;
        font-size: 0.9em;
        font-style: italic;
        margin-bottom: 15px;
    }

    /* 5. 按鈕樣式強制顯色 */
    div.stButton > button {
        background-color: white !important;
        color: #ff4b82 !important;
        border: 2px solid #ffb6c1 !important;
        border-radius: 15px;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background-color: #ffb6c1 !important;
        color: white !important;
    }

    /* 6. 表格內容強制深色 */
    [data-testid="stDataFrame"] * {
        color: #31333f !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 題目資料庫 ---
questions = [
    {"cat": "日常與默契篇", "q": "1. 在2025年的對話中，妳最常出現的身體狀態是什麼？", "o": ["A. 「我餓死了」", "B. 「我睡死/掛了/倒了」", "C. 「我好無聊」", "D. 「我想去跑步」"], "a": "B. 「我睡死/掛了/倒了」", "h": "提示：她常說「剛睡醒」、「補眠」、「睡到現在」"},
    {"cat": "日常與默契篇", "q": "2. 每天早上妳起床後，傳給我的第一句問候語通常是？", "o": ["A. 早安", "B. 寶貝起床沒", "C. 早安安寶貝 (或 早安安唷寶貝)", "D. 餓了吃什麼"], "a": "C. 早安安寶貝 (或 早安安唷寶貝)", "h": "提示：這是她最固定的開場白"},
    {"cat": "日常與默契篇", "q": "3. 峪銓在8月底去考駕照筆試的時候，他考了幾分並很開心地跟妳炫耀？", "o": ["A. 85分", "B. 90分", "C. 95分", "D. 100分"], "a": "D. 100分", "h": "提示：他覺得很簡單，還跟妳說「隨便考都一百」"},
    {"cat": "日常與默契篇", "q": "4. 峪銓的枕頭發生了什麼慘劇，導致他必須把它丟掉換新的？", "o": ["A. 被多米咬爛", "B. 發霉了", "C. 掉進水裡", "D. 被妳搶走"], "a": "B. 發霉了", "h": "提示：房間太潮濕，拿出來看發現黑黑的"},
    {"cat": "生活大事件篇", "q": "5. 今年二月情人節當天，峪銓送妳甚麼你很想要的東西？", "o": ["A. 錢包", "B. 衣服", "C. KANGOL小包", "D. PINO"], "a": "C. KANGOL小包", "h": "提示：他猶豫很久"},
    {"cat": "生活大事件篇", "q": "6. 妳在學校（應數系）最頭痛、常常要讀通宵或覺得會被當的科目是？", "o": ["A. 微積分", "B. 高等微積分 (高微)", "C. 統計學", "D. 線性代數"], "a": "B. 高等微積分 (高微)", "h": "提示：常常讀到睡著或崩潰"},
    {"cat": "生活大事件篇", "q": "7. 1月21日，你們去夢時代逛街前，發生了一個小插曲導致男友有點小不開心，原因是？ ", "o": ["A. 女友睡過頭", "B. 女友起床先回別人留言沒回訊息", "C. 女友忘記帶錢包", "D. 突然下大雨取消行程"], "a": "B. 女友起床先回別人留言沒回訊息", "h": "提示：妳說想等妳清醒一點"},
    {"cat": "生活大事件篇", "q": "8. 7月15日，你們原本要去西子灣附近吃早午餐，結果發生了什麼慘案？", "o": ["A. 車子拋錨", "B. 遇到超大暴雨", "C. 餐廳沒開", "D. 錢包不見了"], "a": "B. 遇到超大暴雨", "h": "提示：那天妳穿的很好看"},
    {"cat": "生活大事件篇", "q": "9. 妳曾經因為「哪個部位」痛到受不了，甚至懷疑自己是不是痛風，連走路都跛腳？", "o": ["A. 膝蓋", "B. 屁股", "C. 脖子", "D. 腰"], "a": "A. 膝蓋", "h": "提示：痛!!"},
    {"cat": "生活大事件篇", "q": "10. 哪一個不是峪銓去日本幫妳買的吉伊卡哇？", "o": ["A. 大地瓜", "B. 小地瓜", "C. 星星", "D. 機場"], "a": "D. 機場", "h": "提示：妳覺得還好的那個"},
    {"cat": "生活大事件篇", "q": "11. 峪銓在暑假的時候幫妳做？", "o": ["A. 洗衣服", "B. 煮飯", "C. 寫程式專案", "D. 搬家"], "a": "D. 搬家", "h": "提示：出了很多力"},
    {"cat": "生活大事件篇", "q": "12. 你們曾經為了吉伊卡哇的某一隻角色（栗子饅頭）的背影，給了他一個很「母湯」的稱號，是什麼？", "o": ["A. 屁股", "B. 奶頭", "C. 雞蛋", "D. 饅頭"], "a": "B. 奶頭", "h": "提示：妳說「回不去了」，男友也覺得很像"},
    {"cat": "細節大考驗", "q": "13. 當男友（峪銓）聽到女朋友又睡過頭、又受傷、或發生什麼離譜的事情時，他的第一個反應詞最常是？", "o": ["A. 「哈哈」", "B. 「挖勒」", "C. 「天啊」", "D. 「傻眼」"], "a": "B. 「挖勒」", "h": "提示：這個詞在對話紀錄中出現了無數次"},
    {"cat": "細節大考驗", "q": "14. 妳曾嘗試過什麼運動但後來覺得太累放棄了？", "o": ["A. 游泳", "B. 跑步", "C. 跳繩", "D. 爬山"], "a": "B. 跑步", "h": "提示：去跑了一次覺得快死了，還穿短袖短褲"},
    {"cat": "細節大考驗", "q": "15. 峪銓想在這個寒假跟妳做甚麼？", "o": ["A. 一直見面", "B. 抱抱", "C. 看電影", "D. 都要"], "a": "D. 都要", "h": "提示：妳男友很貪心"},
    {"cat": "細節大考驗", "q": "16. 最後互道晚安前，最常說的一句甜蜜話語是？", "o": ["A. 拜拜", "B. 我愛你 (或 愛你唷)", "C. 明天見", "D. 晚安"], "a": "B. 我愛你 (或 愛你唷)", "h": "提示：無論發生什麼，結尾常出現的告白"},
    {"cat": "細節大考驗", "q": "17. 在2025年這一年，當妳身體不舒服或是想睡覺時，男朋友「峪銓」最常對妳說的一句話是什麼？", "o": ["A. 快去讀書", "B. 快去休息/抱抱", "C. 不要理妳了", "D. 起來嗨"], "a": "B. 快去休息/抱抱", "h": "提示：他雖然會叫妳讀書，但在妳不舒服時總是叫妳快去躺著"},
    {"cat": "細節大考驗", "q": "18. 最後一題：男朋友峪銓最想對妳說的一句話是什麼？", "o": ["A. 要不要那個", "B. 新年快樂", "C. 想睡覺", "D. 最最最愛妳!!"], "a": "D. 最最最愛妳!!", "h": "提示：不用懷疑的吧"}
]

# --- 狀態管理 ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.is_done = False
    st.session_state.show_feedback = False
    st.session_state.last_result = None 
    st.session_state.history = [] 

# --- UI 邏輯 ---
# 這裡的主標題使用了寫死的 inline style 顏色
st.markdown("<h1 class='main-title' style='color: #ff4b82 !important;'>💖 2025 真愛默契挑戰 💖</h1>", unsafe_allow_html=True)

if not st.session_state.is_done:
    current_q = questions[st.session_state.step]

    # --- 反饋視窗模式 ---
    if st.session_state.show_feedback:
        res = st.session_state.last_result
        st.markdown('<div class="feedback-box">', unsafe_allow_html=True)
        
        # 這裡將 st.write 改為手動 HTML 標籤，確保顏色不會被手機深色模式蓋掉
        if res['correct']:
            st.markdown("<h2 style='color: #4CAF50 !important;'>✅ 答對了！太棒了！</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #31333f !important;'>妳選了：<b>{res['user_pick']}</b></p>", unsafe_allow_html=True)
            st.markdown("<p style='color: #31333f !important;'>不愧是我的寶貝，這都記得！🥰</p>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='color: #f44336 !important;'>❌ 答錯咯～再接再厲！</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #31333f !important;'>妳選了：<b>{res['user_pick']}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #31333f !important;'>正確答案是：<span style='color: #ff4b82; font-weight: bold;'>{res['correct_ans']}</span></p>", unsafe_allow_html=True)
            st.markdown("<p style='color: #31333f !important;'>是不是讀書讀太累了？沒關係抱我一下就沒事了 😋</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("") 
        
        if st.button("下一題 ➡️", key="next_btn"):
            st.session_state.show_feedback = False
            if st.session_state.step < len(questions) - 1:
                st.session_state.step += 1
            else:
                st.session_state.is_done = True
            st.rerun()

    # --- 答題模式 ---
    else:
        st.progress((st.session_state.step) / len(questions))
        st.markdown(f"<p style='color: #31333f !important;'>目前進度：{st.session_state.step + 1} / {len(questions)}</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="question-box">
            <div class="category-badge">{current_q['cat']}</div>
            <h3 style='color: #333 !important;'>{current_q['q']}</h3>
            <p class="hint-text">{current_q['h']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        for option in current_q['o']:
            if st.button(option, key=f"opt_{st.session_state.step}_{option}"):
                is_correct = (option == current_q['a'])
                if is_correct:
                    st.session_state.score += 1
                    st.balloons()
                
                st.session_state.history.append({
                    "題目": current_q['q'][:20] + "...",
                    "妳的回答": option,
                    "正確答案": current_q['a'],
                    "結果": "✅" if is_correct else "❌"
                })

                st.session_state.last_result = {
                    'correct': is_correct,
                    'user_pick': option,
                    'correct_ans': current_q['a']
                }
                st.session_state.show_feedback = True
                st.rerun()

else:
    # --- 結束畫面與統計表 ---
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #31333f !important;'>🎉 挑戰完成 🎉</h1>", unsafe_allow_html=True)
    final_score = st.session_state.score
    st.markdown(f"<h2 style='color: #ff4b82 !important;'>最終得分：{final_score} / {len(questions)}</h2>", unsafe_allow_html=True)
    
    if final_score == len(questions):
        st.markdown("<h3 style='color: #31333f !important;'>🏆 滿分！妳絕對是我的真愛靈魂伴侶！愛妳唷 ❤️</h3>", unsafe_allow_html=True)
    elif final_score >= 12:
        st.markdown("<h3 style='color: #31333f !important;'>✨ 超棒！我們的回憶妳都記得很清楚呢～ 🥰</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color: #31333f !important;'>🧐 哎呀～罰妳重看聊天紀錄，然後親我一下！ 🐶</h3>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: #31333f !important;'>📊 答題戰報回顧</h3>", unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True, hide_index=True)

    if st.button("重新開始挑戰"):
        st.session_state.step = 0
        st.session_state.score = 0
        st.session_state.is_done = False
        st.session_state.show_feedback = False
        st.session_state.history = []
        st.rerun()