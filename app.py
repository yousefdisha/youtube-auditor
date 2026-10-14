
import streamlit as st
import requests
import time
from urllib.parse import urlparse, unquote

# مفتاح الـ API الخاص بك مربوط جاهز
API_KEYS_LIST = [
    "AIzaSyC-CwysTNGs92t08Bzt6QOJDOgG-StjghY",
    "AIzaSyC-CwysTNGs92t08Bzt6QOJD0gG-StjghY"
]

st.set_page_config(
    page_title="فاحص قنوات اليوتيوب الاحترافي",
    page_icon="👁️",
    layout="centered"
)

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
        color: #cbd5e1;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }
    .input-label {
        color: #00ffcc;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    /* تصغير مربع الإدخال ليرجع لطبيعته مع الحفاظ على وضوح الخط الأبيض */
    div[data-baseweb="input"] {
        background-color: #111827 !important;
        border: 1.5px solid #00ffcc !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"] input {
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 8px 12px !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff007f, #7928ca, #00d4ff);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-weight: 900;
        font-size: 1.1rem;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.4);
        transition: 0.3s;
        margin-top: 10px;
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

st.markdown("<div class='input-label'>🔗 الصق رابط القناة أو اليوزر نيم (@username) أو اسم القناة هنا:</div>", unsafe_allow_html=True)
channel_input = st.text_input("رابط القناة", placeholder="مثال: https://www.youtube.com/@ChannelName", label_visibility="collapsed")


def yt_get(url, params):
    last_res = {}
    for key in API_KEYS_LIST:
        p = dict(params)
        p["key"] = key
        try:
            res = requests.get(url, params=p, timeout=15).json()
        except Exception as e:
            return {"error": {"message": str(e)}}
        if "error" not in res:
            return res
        last_res = res
        err_msg = str(res.get("error", {}).get("message", ""))
        if "API key not valid" not in err_msg:
            return res
    return last_res


def resolve_channel(user_input):
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

    if channel_id:
        r = yt_get(base_url, {"part": "snippet,statistics,contentDetails", "id": channel_id})
        if r.get("items"):
            return r["items"][0], None

    if handle:
        for h in [handle, handle.lstrip("@")]:
            r = yt_get(base_url, {"part": "snippet,statistics,contentDetails", "forHandle": h})
            if r.get("items"):
                return r["items"][0], None

    if username:
        r = yt_get(base_url, {"part": "snippet,statistics,contentDetails", "forUsername": username})
        if r.get("items"):
            return r["items"][0], None

    q_term = handle or username or text
    search_r = yt_get("https://www.googleapis.com/youtube/v3/search", {
        "part": "snippet",
        "type": "channel",
        "q": q_term,
        "maxResults": 1
    })
    if "error" in search_r:
        return None, search_r["error"].get("message", "خطأ في الاتصال بالـ API")
    if search_r.get("items"):
        found_id = search_r["items"][0]["snippet"]["channelId"]
        r = yt_get(base_url, {"part": "snippet,statistics,contentDetails", "id": found_id})
        if r.get("items"):
            return r["items"][0], None

    return None, "لم يتم العثور على القناة، تأكد من الرابط أو الاسم."


def get_long_videos_only(channel_id):
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
        scanner_placeholder = st.empty()
        progress_bar = st.progress(0)
        start_time = time.time()

        scanner_placeholder.markdown("""
            <div class='scanner-box'>
                <div class='eye-icon'>👁️</div>
                <h3 style='color:#00ffcc; margin-top:15px;'>جاري الفحص العميق والتدقيق...</h3>
                <p style='color:#ff007f; font-size:0.95rem;'>يرجى الانتظار لإصدار التقرير النهائي...</p>
            </div>
        """, unsafe_allow_html=True)

        channel_data, error_msg = resolve_channel(channel_input)

        if error_msg or not channel_data:
            scanner_placeholder.empty()
            progress_bar.empty()
            st.error(f"❌ {error_msg}")
        else:
            channel_id = channel_data["id"]
            long_videos = get_long_videos_only(channel_id)

            target_duration = 12.5
            while True:
                elapsed = time.time() - start_time
                if elapsed >= target_duration:
                    break
                progress_ratio = min(elapsed / target_duration, 0.99)
                progress_bar.progress(int(progress_ratio * 100))
                remaining_sec = max(1, int(target_duration - elapsed))

                scanner_placeholder.markdown(f"""
                    <div class='scanner-box'>
                        <div class='eye-icon'>👁️</div>
                        <h3 style='color:#00ffcc; margin-top:15px;'>جاري الفحص العميق والتدقيق... ({int(progress_ratio * 100)}%)</h3>
                        <p style='color:#ff007f; font-size:0.95rem;'>متبقي {remaining_sec} ثانية لإصدار التقرير النهائي...</p>
                    </div>
                """, unsafe_allow_html=True)
                time.sleep(0.4)

            progress_bar.progress(100)
            time.sleep(0.3)
            scanner_placeholder.empty()
            progress_bar.empty()

            snippet = channel_data.get("snippet", {})
            stats = channel_data.get("statistics", {})

            channel_title = snippet.get("title", "غير متوفر")
            custom_url = snippet.get("customUrl", "")
            published_at_raw = snippet.get("publishedAt", "")
            published_date = published_at_raw[:10] if published_at_raw else "غير متوفر"

            # بناء رابط القناة الكامل والصحيح تماماً
            if custom_url:
                if not custom_url.startswith("@"):
                    custom_url = "@" + custom_url
                full_channel_url = f"https://www.youtube.com/{custom_url}"
            else:
                full_channel_url = f"https://www.youtube.com/channel/{channel_id}"

            subscribers = int(stats.get("subscriberCount", 0))
            total_views = int(stats.get("viewCount", 0))
            total_videos_count = int(stats.get("videoCount", 0))

            if total_views > 0:
                sub_ratio = (subscribers / total_views) * 100
            else:
                sub_ratio = 0.0 if subscribers == 0 else 100.0

            if sub_ratio <= 7.0:
                sub_status_badge = "<span class='badge-ok'>✅ مشتركين حقيقيين (حقيقي)</span>"
            else:
                sub_status_badge = "<span class='badge-bad'>❌ مرفوضة - تزويد مشتركين سيرفر</span>"

            rejected_videos = []
            qualified_long_videos_count = 0

            for vid in long_videos:
                if vid["views"] < 100:
                    continue

                qualified_long_videos_count += 1
                eng_rate = (((vid["comments"] * 2) + vid["likes"]) / vid["views"]) * 100

                if eng_rate < 1.0:
                    rejected_videos.append({
                        "title": vid["title"],
                        "url": vid["url"]
                    })

            if len(long_videos) == 0 or qualified_long_videos_count == 0 or len(rejected_videos) == 0:
                videos_status_badge = "<span class='badge-ok'>✅ مشاهدات حقيقية (حقيقي)</span>"
            else:
                videos_status_badge = "<span class='badge-bad'>❌ تزويد مشاهدات سيرفر</span>"

            st.markdown("---")
            st.subheader("📋 التقرير التفصيلي الكامل للقناة:")

            st.markdown(f"""
                <div class='report-card'>
                    <div class='report-label'>📺 اسم القناة</div>
                    <div class='report-value'>{channel_title}</div>
                </div>
            """, unsafe_allow_html=True)

            # عرض رابط القناة الكامل والصحيح كـ رابط قابل للضغط ومرتب
            st.markdown(f"""
                <div class='report-card'>
                    <div class='report-label'>🔗 رابط القناة الكامل</div>
                    <div class='report-value' style='direction:ltr; text-align:right;'>
                        <a href='{full_channel_url}' target='_blank' style='color: #38bdf8; text-decoration: none;'>{full_channel_url}</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class='report-card'>
                    <div class='report-label'>👥 عدد المشتركين وحالة الفحص</div>
                    <div class='report-value'>
                        {subscribers:,} مشترك
                        {sub_status_badge}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            rejected_html = ""
            if rejected_videos:
                for rv in rejected_videos:
                    rejected_html += f"""
                        <div class='bad-video-item'>
                            <div>🎬 <b>{rv['title']}</b></div>
                            <div style='margin-top:4px;'>
                                🔗 الرابط: <a href='{rv['url']}' target='_blank'>{rv['url']}</a>
                                <span class='badge-bad'>❌ تزويد مشاهدات سيرفر</span>
                            </div>
                        </div>
                    """

            st.markdown(f"""
                <div class='report-card'>
                    <div class='report-label'>🎥 عدد الفيديوهات وحالة المشاهدات</div>
                    <div class='report-value'>
                        {total_videos_count:,} فيديو
                        {videos_status_badge}
                    </div>
                    {rejected_html}
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class='report-card'>
                    <div class='report-label'>📅 تاريخ إنشاء القناة</div>
                    <div class='report-value'>{published_date}</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class='report-card'>
                    <div class='report-label'>👁️ عدد المشاهدات الإجمالي للقناة (مشاهدات اللمحة)</div>
                    <div class='report-value'>{total_views:,} مشاهدة</div>
                </div>
            """, unsafe_allow_html=True)
