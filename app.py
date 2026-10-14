import streamlit as st
import requests
import time
from urllib.parse import urlparse, unquote

# ==========================================
# تم ربط مفتاح الـ API الخاص بك مباشرة هنا
# ==========================================
API_KEYS_LIST = [
    "AIzaSyC-CwysTNGs92t08Bzt6QOJDOgG-StjghY",
    "AIzaSyC-CwysTNGs92t08Bzt6QOJD0gG-StjghY"
]

st.set_page_config(
    page_title="فاحص قنوات اليوتيوب الاحترافي",
    page_icon="👁️",
    layout="centered"
)

# تصميم نيون ودارك مود احترافي مع أنيميشن علامة العين
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    .stApp {
        background-color: #090d16;
        color: #ffffff;
        direction: rtl;
        text-align: right;
    }
    .main-title {
        text-align: center;
        color: #00ffcc;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.5);
        font-weight: 900;
        font-size: 2.2rem;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #a0aec0;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff007f, #7928ca, #00d4ff);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 14px 24px;
        font-weight: 900;
        font-size: 1.2rem;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.8);
        transform: scale(1.01);
    }
    .scanner-box {
        background-color: #111827;
        border: 2px solid #00ffcc;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.25);
        margin: 20px 0;
    }
    .eye-icon {
        font-size: 4.5rem;
        animation: pulse 1.2s infinite alternate;
        display: inline-block;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); filter: drop-shadow(0 0 5px #00ffcc); }
        100% { transform: scale(1.15); filter: drop-shadow(0 0 25px #ff007f); }
    }
    .report-card {
        background-color: #111827;
        border: 1px solid #2d3748;
        border-right: 5px solid #00ffcc;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    .report-label {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }
    .report-value {
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: 700;
    }
    .badge-ok {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid #10b981;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: bold;
        margin-right: 10px;
        display: inline-block;
    }
    .badge-bad {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid #ef4444;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: bold;
        margin-right: 10px;
        display: inline-block;
    }
    .bad-video-item {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 12px;
        margin-top: 10px;
        direction: rtl;
    }
    .bad-video-item a {
        color: #38bdf8;
        font-weight: bold;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>👁️ نظام الفحص والتدقيق الذكي لقنوات اليوتيوب</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>فحص شامل للمشتركين، الفيديوهات الطويلة، الشورتس، وكشف تزويد السيرفرات بدقة</div>", unsafe_allow_html=True)

channel_input = st.text_input("🔗 ضع رابط القناة أو اليوزر نيم (@username) أو الـ ID هنا:", placeholder="مثال: https://www.youtube.com/@ChannelName")


def yt_get(url, params):
    """إرسال الطلب باستخدام مفتاح الـ API مع تبديل تلقائي في حال تشابه حرف O و 0"""
    last_res = {}
    for key in API_KEYS_LIST:
        p = dict(params)
        p["key"] = key
        res = requests.get(url, params=p).json()
        if "error" not in res:
            return res
        last_res = res
        err_msg = str(res.get("error", {}).get("message", ""))
        if "API key not valid" not in err_msg:
            return res
    return last_res


def resolve_channel(user_input):
    """استخراج بيانات القناة من أي رابط أو يوزر نيم أو معرف"""
    text = unquote(user_input.strip())
    handle = None
    channel_id = None
    username = None

    if "youtube.com" in text or "youtu.be" in text:
        parsed = urlparse(text if text.startswith("http") else "https://" + text)
        path = parsed.path.strip("/")
        parts = path.split("/")
        if parts:
            if parts[0].startswith("@"):
                handle = parts[0]
            elif parts[0] == "channel" and len(parts) > 1:
                channel_id = parts[1]
            elif parts[0] in ["c", "user"] and len(parts) > 1:
                username = parts[1]
            else:
                handle = parts[0]
    else:
        if text.startswith("@"):
            handle = text
        elif text.startswith("UC") and len(text) == 24:
            channel_id = text
        else:
            handle = "@" + text

    base_url = "https://www.googleapis.com/youtube/v3/channels"

    # 1. البحث بالـ Channel ID المباشر
    if channel_id:
        r = yt_get(base_url, {"part": "snippet,statistics,contentDetails", "id": channel_id})
        if "error" in r:
            return None, r["error"].get("message", "خطأ في مفتاح الـ API")
        if r.get("items"):
            return r["items"][0], None

    # 2. البحث بالـ Handle (@username)
    if handle:
        for h in [handle, handle.lstrip("@")]:
            r = yt_get(base_url, {"part": "snippet,statistics,contentDetails", "forHandle": h})
            if "error" in r:
                return None, r["error"].get("message", "خطأ في مفتاح الـ API")
            if r.get("items"):
                return r["items"][0], None

    # 3. البحث بالـ Username القديم
    if username:
        r = yt_get(base_url, {"part": "snippet,statistics,contentDetails", "forUsername": username})
        if r.get("items"):
            return r["items"][0], None

    # 4. بحث عام احتياطي للوصول للقناة
    q_term = handle or username or text
    search_r = yt_get("https://www.googleapis.com/youtube/v3/search", {
        "part": "snippet",
        "type": "channel",
        "q": q_term,
        "maxResults": 1
    })
    if "error" in search_r:
        return None, search_r["error"].get("message", "خطأ في مفتاح الـ API")
    if search_r.get("items"):
        found_id = search_r["items"][0]["snippet"]["channelId"]
        r = yt_get(base_url, {"part": "snippet,statistics,contentDetails", "id": found_id})
        if r.get("items"):
            return r["items"][0], None

    return None, "لم يتم العثور على القناة، تأكد من الرابط أو الاسم."


def get_long_videos_only(channel_id):
    """
    سحب الفيديوهات الطويلة فقط الموجودة في قسم (الفيديوهات) على القناة
    واستبعاد أي فيديو موجود في قسم (الشورتس Shorts) تماماً
    """
    uulf_playlist_id = "UULF" + channel_id[2:]
    video_ids = []
    next_page_token = None

    while True:
        params = {
            "part": "contentDetails",
            "playlistId": uulf_playlist_id,
            "maxResults": 50
        }
        if next_page_token:
            params["pageToken"] = next_page_token

        res = yt_get("https://www.googleapis.com/youtube/v3/playlistItems", params)

        # إذا لم تكن القائمة موجودة فهذا يعني عدم وجود فيديوهات طويلة في قسم الفيديوهات (كلها شورتس أو فارغة)
        if "error" in res:
            break

        for item in res.get("items", []):
            vid = item.get("contentDetails", {}).get("videoId")
            if vid:
                video_ids.append(vid)

        next_page_token = res.get("nextPageToken")
        if not next_page_token or len(video_ids) >= 150:
            break

    long_videos_data = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        v_res = yt_get("https://www.googleapis.com/youtube/v3/videos", {
            "part": "snippet,statistics",
            "id": ",".join(batch)
        })

        for v in v_res.get("items", []):
            stats = v.get("statistics", {})
            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))
            title = v.get("snippet", {}).get("title", "فيديو بدون عنوان")

            long_videos_data.append({
                "id": v["id"],
                "title": title,
                "views": views,
                "likes": likes,
                "comments": comments,
                "url": f"https://www.youtube.com/watch?v={v['id']}"
            })

    return long_videos_data


if st.button("👁️ ابدأ الفحص الشامل للقناة الآن"):
    if not channel_input.strip():
        st.error("⚠️ من فضلك ضع رابط القناة أو اسمها أولاً!")
    else:
        # صندوق الفحص الاحترافي بعلامة العين لمدة 12 ثانية (بين 10 إلى 15 ثانية)
        scanner_placeholder = st.empty()
        progress_bar = st.progress(0)
        start_time = time.time()

        scan_steps = [
            "جاري الاتصال بسيرفرات يوتيوب وسحب بيانات لمحة القناة...",
            "جاري فحص عدد المشتركين ومقارنته بإجمالي مشاهدات اللمحة...",
            "جاري استبعاد قسم الشورتس (Shorts) واعتمادها كتزويد حقيقي...",
            "جاري سحب الفيديوهات الطويلة من قسم الفيديوهات وتطبيق شروط الـ 100 مشاهدة...",
            "جاري حساب معادلة التفاعل ((الكومنتات × 2) + اللايكات) / المشاهدات...",
            "جاري تجهيز التقرير النهائي وكشف حالة القناة..."
        ]

        scanner_placeholder.markdown(f"""
            <div class='scanner-box'>
                <div class='eye-icon'>👁️</div>
                <h3 style='color:#00ffcc; margin-top:15px;'>جاري الفحص العميق للقناة...</h3>
                <p style='color:#cbd5e1; font-size:1.1rem;'>{scan_steps[0]}</p>
                <p style='color:#64748b; font-size:0.9rem;'>يرجى الانتظار (يستغرق الفحص الدقيق من 10 إلى 15 ثانية)</p>
            </div>
        """, unsafe_allow_html=True)

