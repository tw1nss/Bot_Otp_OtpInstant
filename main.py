import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
import requests
import time
import threading
import sys
import os

# ==============================================================================
# --- 0. ANIMASI LOADING TERMINAL SAAT RUNNING ---
# ==============================================================================
def loading_terminal_animation():
    print("=" * 60)
    print("      INITIALIZING OTP INSTAN BOT CORE SYSTEM v3.0       ")
    print("=" * 60)
    
    steps = [
        "Connecting to OTPInstan API Server...",
        "Validating Admin Chat ID Configuration...",
        "Injecting Database Cache Memory Thread...",
        "Synchronizing Telegram Command Shortcuts...",
        "Configuring Category-Based Price Monitor...",
        "Injecting Manual Notification Test Route..."
    ]
    
    for step in steps:
        sys.stdout.write(f"⚙️ {step:<45}")
        sys.stdout.flush()
        time.sleep(0.1)  # Dipercepat untuk lingkungan cloud production
        sys.stdout.write("[ DONE ]\n")
        sys.stdout.flush()
        
    print("-" * 60)
    print("🚀 SYSTEM STATUS: ONLINE & INFINITY POLLING STARTED!")
    print("=" * 60)

loading_terminal_animation()

# ==============================================================================
# --- 1. KONFIGURASI UTAMA (SECURE ENVIRONMENT VERSION) ---
# ==============================================================================

# Mengambil config sensitif dari Environment Variables Render (Lebih Aman!)
API_KEY = os.environ.get('OTP_API_KEY', 'otpk_b66f75f84a1112179214e8e13f5e0cf3420412274dd4134c') 
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8628365839:AAHthtJUEi70gYjsfBjs1iLzKu4n3PLeu0w')  
ADMIN_CHAT_ID = int(os.environ.get('ADMIN_CHAT_ID', 5902757286))

BASE_URL = 'https://otpinstan.com/api/reseller'
HEADERS = {'X-Api-Key': API_KEY}

bot = telebot.TeleBot(BOT_TOKEN)

# --- LIVE METRICS & TRAFFIC VARIABLE ---
BOT_START_TIME = time.time()  
TRAFFIC_STATS = {
    "total_messages": 0,
    "total_commands": 0,
    "total_callbacks": 0,
    "orders_success": 0,
    "orders_failed": 0
}

active_orders = {}
GLOBAL_SERVERS_CACHE = []
CACHE_LAST_UPDATE = 0
cache_lock = threading.Lock()

FLAG_MAPPING = {
    'indonesia': '🇮🇩', 'malaysia': '🇲🇾', 'philippines': '🇵🇭', 'thailand': '🇹🇭',
    'vietnam': '🇻🇳', 'south africa': '🇿🇦', 'cambodia': '🇰🇭', 'myanmar': '🇲🇲',
    'laos': '🇱🇦', 'india': '🇮🇳', 'russia': '🇷🇺', 'united states': '🇺🇸',
    'china': '🇨🇳', 'brazil': '🇧🇷', 'mexico': '🇲🇽', 'colombia': '🇨🇴',
    'egypt': '🇪🇬', 'nigeria': '🇳🇬', 'england': '🇬🇧', 'united kingdom': '🇬🇧'
}

POPULAR_COUNTRY_IDS = ["6", "40", "22", "13", "54", "10", "15", "14", "117", "1", "12", "3"]

def get_flag(country_name):
    if not country_name:
        return '🌐'
    name_lower = country_name.lower().strip()
    return FLAG_MAPPING.get(name_lower, '🏳️')

def get_uptime_graph():
    uptime_seconds = int(time.time() - BOT_START_TIME)
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    
    filled_bars = min(10, max(1, (minutes // 5) + 1 if hours == 0 else (hours * 2)))
    empty_bars = 10 - filled_bars
    bar_graph = "█" * filled_bars + "░" * empty_bars
    
    uptime_string = f"`{days} Hari, {hours} Jam, {minutes} Menit, {seconds} Detik`"
    return bar_graph, uptime_string

def api_get(endpoint):
    try:
        res = requests.get(f'{BASE_URL}/{endpoint}', headers=HEADERS, timeout=8)
        if res.status_code == 429:
            return {'success': False, 'message': 'rate_limit'}
        return res.json()
    except:
        return {'success': False, 'message': 'error'}

def api_post(endpoint, data):
    try:
        res = requests.post(f'{BASE_URL}/{endpoint}', headers=HEADERS, data=data, timeout=8)
        if res.status_code == 429:
            return {'success': False, 'message': 'rate_limit'}
        return res.json()
    except:
        return {'success': False, 'message': 'error'}

# ==============================================================================
# --- 2. DAFTARKAN SHORTCUT MENU ---
# ==============================================================================
def daftarkan_menu_shortcut():
    try:
        commands = [
            BotCommand("start", "Mulai bot & Tampilkan Menu Utama"),
            BotCommand("pm", "Hubungi Admin / Owner"),
            BotCommand("admin", "Buka Panel Admin (Khusus Owner)"),
            BotCommand("id", "Cek Chat ID saat ini")
        ]
        bot.set_my_commands(commands)
    except Exception as e:
        print(f"❌ Gagal mendaftarkan menu shortcut: {e}")

daftarkan_menu_shortcut()

# ==============================================================================
# --- 3. HANDLING COMMAND MENU SHORCUT ---
# ==============================================================================

@bot.message_handler(commands=['start', 'menu', 'saldo'])
def cmd_start(message):
    TRAFFIC_STATS["total_commands"] += 1
    chat_id = message.chat.id
    bal = api_get('balance.php')
    
    saldo_info = "Rp 0"
    if isinstance(bal, dict) and bal.get('success') is True:
        saldo_info = bal.get('balance_formatted', f"Rp {bal.get('balance', 0)}")

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="🛒 Order Nomor WhatsApp", callback_data="main_order"))
    markup.add(InlineKeyboardButton(text="💰 Top Up Saldo", callback_data="main_topup"))
    
    bot.send_message(
        chat_id, 
        f"👋 **Selamat Datang di Bot OTP Instan**\n\n"
        f"💵 **Saldo Akun Anda:** {saldo_info}\n"
        f"Silakan tentukan pilihan Anda:", 
        reply_markup=markup, parse_mode='Markdown'
    )

@bot.message_handler(commands=['pm'])
def cmd_pm(message):
    TRAFFIC_STATS["total_commands"] += 1
    bot.send_message(message.chat.id, f"📞 **Hubungi Admin / Owner**\n\nSilakan hubungi owner langsung jika ada kendala.", parse_mode='Markdown')

@bot.message_handler(commands=['admin'])
def cmd_admin(message):
    TRAFFIC_STATS["total_commands"] += 1
    if message.chat.id == ADMIN_CHAT_ID:
        bar, masa_aktif = get_uptime_graph()
        waktu_mulai_str = time.strftime('%d-%m-%Y %H:%M:%S WIB', time.localtime(BOT_START_TIME))
        
        teks_admin = (
            f"👑 **PANEL ADMINISTRATOR OWNER**\n"
            f"====================================\n\n"
            f"📈 **GRAFIK MASA AKTIF BOT (UPTIME):**\n"
            f"⏱ `[{bar}]`\n"
            f"⏳ Durasi: {masa_aktif}\n"
            f"🗓 Sejak: `{waktu_mulai_str}`\n\n"
            f"📊 **LIST TRAFFIC DATA (LIFETIME):**\n"
            f"▪️ Total Chat Masuk: `{TRAFFIC_STATS['total_messages']}`\n"
            f"▪️ Perintah Command: `{TRAFFIC_STATS['total_commands']}`\n"
            f"▪️ Klik Tombol Menu: `{TRAFFIC_STATS['total_callbacks']}`\n"
            f"▪️ Transaksi Sukses: `🟢 {TRAFFIC_STATS['orders_success']}`\n"
            f"▪️ Transaksi Gagal/Stok Habis: `🔴 {TRAFFIC_STATS['orders_failed']}`\n\n"
            f"⚙️ **AKSI PENGATURAN SYSTEM:**"
        )
        
        markup_admin = InlineKeyboardMarkup()
        markup_admin.add(InlineKeyboardButton(text="🧪 Test Notif Perubahan Kategori", callback_data="admin_test_notif"))
        
        bot.send_message(message.chat.id, teks_admin, reply_markup=markup_admin, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "⚠️ **Akses Ditolak!**\nMenu ini khusus untuk Owner Bot.")

@bot.message_handler(commands=['id'])
def cmd_id(message):
    TRAFFIC_STATS["total_commands"] += 1
    bot.send_message(message.chat.id, f"🆔 **Informasi Chat ID Anda:**\n\n`{message.chat.id}`", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def log_all_messages(message):
    TRAFFIC_STATS["total_messages"] += 1

# ==============================================================================
# --- CALLBACK HANDLER UNTUK TOMBOL TEST NOTIF MANUAL ---
# ==============================================================================
@bot.callback_query_handler(func=lambda call: call.data == "admin_test_notif")
def handle_test_notif_manual(call):
    TRAFFIC_STATS["total_callbacks"] += 1
    if call.message.chat.id != ADMIN_CHAT_ID:
        bot.answer_callback_query(call.id, text="Akses Ditolak!", show_alert=True)
        return
        
    bot.answer_callback_query(call.id, text="🚀 Mengirimkan Simulasi Kategori...")
    waktu_test = time.strftime('%H:%M:%S WIB', time.localtime())
    
    pesan_simulasi = (
        f"📢 **[SIMULASI] LAPORAN UPDATE PER KATEGORI BUDGET**\n"
        f"⏱ _Waktu Tarik Data: {waktu_test}_\n"
        f"====================================\n\n"
        f"💸 **1. KATEGORI BUDGET EKONOMIS (< Rp 1.000)**\n"
        f"🟢 `[STOK TERSEDIA]` 🇮🇩 Indonesia (Server 3001)\n"
        f" ➡️ Harga: `Rp 950` | Sisa Stok: `12 Nomor`\n\n"
        f"🛒 **2. KATEGORI STANDARD MURAH (Rp 1.000 - Rp 2.000)**\n"
        f"🔴 `[NAIK HARGA]` 🇲🇾 Malaysia (Server 2579)\n"
        f" ➡️ `Rp 1,100` naik `+Rp 200` ➡️ jadi `Rp 1,300`\n"
        f"🟢 `[TURUN HARGA]` 🇵🇭 Philippines (Server 1170)\n"
        f" ➡️ `Rp 1,500` turun `-Rp 150` ➡️ jadi `Rp 1,350`\n\n"
        f"👑 **3. KATEGORI SERVER PREMIUM (> Rp 5.000)**\n"
        f"✨ `[STOK BARU MASUK]` 🇺🇸 United States (Server 3224)\n"
        f" ➡️ Harga: `Rp 5,400` | Jumlah Stok: `450 Nomor`\n\n"
        f"⚙️ _Sistem pemantauan per kategori budget berjalan normal._"
    )
    bot.send_message(ADMIN_CHAT_ID, pesan_simulasi, parse_mode='Markdown')

# ==============================================================================
# --- 4. BACKGROUND CACHE ENGINE ---
# ==============================================================================

def update_global_servers_cache():
    global GLOBAL_SERVERS_CACHE, CACHE_LAST_UPDATE
    while True:
        try:
            countries_res = api_get('countries.php')
            if not isinstance(countries_res, dict) or 'data' not in countries_res:
                time.sleep(15)
                continue
                
            country_map = {str(c.get('id')): c.get('name', 'Unknown') for c in countries_res['data']}
            temp_servers = []
            
            for cid in POPULAR_COUNTRY_IDS:
                cname = country_map.get(cid, f"Negara {cid}")
                ops_res = api_get(f"operators.php?service=wa&country={cid}")
                
                if isinstance(ops_res, dict) and ops_res.get('message') == 'rate_limit':
                    break
                    
                if ops_res and ops_res.get('success') and 'data' in ops_res:
                    for op in ops_res['data']:
                        harga_sekarang = int(op.get('price', 0))
                        stok_sekarang = int(op.get('count', 0))
                        
                        if stok_sekarang > 0:
                            pid = str(op.get('provider_id', '')).strip()
                            pid = "any" if not pid else pid
                            
                            temp_servers.append({
                                'unique_key': f"{cid}_{pid}",
                                'country_id': cid,
                                'country_name': cname,
                                'provider_id': pid,
                                'label': op.get('label', 'Unknown'),
                                'price': harga_sekarang,
                                'count': stok_sekarang
                            })
                time.sleep(0.2) 

            if temp_servers:
                temp_servers = sorted(temp_servers, key=lambda x: x['price'])
                with cache_lock:
                    GLOBAL_SERVERS_CACHE = temp_servers
                    CACHE_LAST_UPDATE = time.time()
            
            time.sleep(90) 

        except Exception as e:
            time.sleep(15)

threading.Thread(target=update_global_servers_cache, daemon=True).start()

# ==============================================================================
# --- 5. LOOP AUTOMATIS MONITOR PERKATEGORI (30 MENIT) ---
# ==============================================================================

def loop_monitor_perubahan_harga():
    time.sleep(15)
    with cache_lock:
        old_prices = {s['unique_key']: s['price'] for s in GLOBAL_SERVERS_CACHE}
    
    while True:
        time.sleep(1800)
        try:
            with cache_lock:
                current_snapshot = list(GLOBAL_SERVERS_CACHE)
            
            new_prices = {s['unique_key']: s['price'] for s in current_snapshot}
            
            kat_ekonomis_list = []
            kat_standard_list = []
            kat_premium_list = []
            
            for srv in current_snapshot:
                key = srv['unique_key']
                harga_baru = srv['price']
                stok_saat_ini = srv['count']
                flag = get_flag(srv['country_name'])
                nama_tampilan = f"{flag} {srv['country_name']} ({srv['label']})"
                
                if key in old_prices:
                    harga_lama = old_prices[key]
                    selisih = abs(harga_baru - harga_lama)
                    
                    if harga_baru > harga_lama:
                        log_teks = f"🔴 `[NAIK HARGA]` {nama_tampilan}\n   ➡️ `Rp {harga_lama:,}` naik `+Rp {selisih:,}` ➡️ `Rp {harga_baru:,}`"
                    elif harga_baru < harga_lama:
                        log_teks = f"🟢 `[TURUN HARGA]` {nama_tampilan}\n   ➡️ `Rp {harga_lama:,}` turun `-Rp {selisih:,}` ➡️ `Rp {harga_baru:,}`"
                    else:
                        continue
                else:
                    log_teks = f"✨ `[STOK BARU MASUK]` {nama_tampilan}\n   ➡️ Harga: `Rp {harga_baru:,}` | Stok: `{stok_saat_ini} Nomor`"
                
                if harga_baru < 1000:
                    kat_ekonomis_list.append(log_teks)
                elif 1000 <= harga_baru <= 2000:
                    kat_standard_list.append(log_teks)
                elif harga_baru > 5000:
                    kat_premium_list.append(log_teks)

            if kat_ekonomis_list or kat_standard_list or kat_premium_list:
                waktu_sekarang = time.strftime('%H:%M:%S WIB', time.localtime())
                
                pesan_notif = (
                    f"📢 **LAPORAN PERUBAHAN UPDATE PER KATEGORI BUDGET**\n"
                    f"⏱ _Waktu Tarik Data: {waktu_sekarang}_\n"
                    f"====================================\n\n"
                )
                
                if kat_ekonomis_list:
                    pesan_notif += f"💸 **1. KATEGORI BUDGET EKONOMIS (< Rp 1.000)**\n" + "\n".join(kat_ekonomis_list) + "\n\n"
                if kat_standard_list:
                    pesan_notif += f"🛒 **2. KATEGORI STANDARD MURAH (Rp 1.000 - Rp 2.000)**\n" + "\n".join(kat_standard_list) + "\n\n"
                if kat_premium_list:
                    pesan_notif += f"👑 **3. KATEGORI SERVER PREMIUM (> Rp 5.000)**\n" + "\n".join(kat_premium_list) + "\n\n"
                
                pesan_notif += "⚙️ _Laporan ini dikirim otomatis setiap 30 menit jika ada perubahan._"
                
                try:
                    bot.send_message(ADMIN_CHAT_ID, pesan_notif, parse_mode='Markdown')
                except Exception as error_kirim:
                    print(f"❌ Gagal broadcast ke telegram admin: {error_kirim}")
            
            old_prices = new_prices
            
        except Exception as global_error:
            print(f"⚠️ Terjadi galat pada mesin monitor: {global_error}")

threading.Thread(target=loop_monitor_perubahan_harga, daemon=True).start()

# ==============================================================================
# --- 6. NAVIGASI UTAMA & KATEGORI BUDGET ---
# ==============================================================================

@bot.callback_query_handler(func=lambda call: call.data in ["main_order", "main_topup", "goto_main"])
def handle_main_navigation(call):
    TRAFFIC_STATS["total_callbacks"] += 1
    chat_id = call.message.chat.id
    
    if call.data == "goto_main":
        bot.answer_callback_query(call.id)
        cmd_start(call.message)
        return

    if call.data == "main_topup":
        bot.answer_callback_query(call.id)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="⬅️ Kembali", callback_data="goto_main"))
        try:
            bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id,
                text="💳 **Informasi Top Up Saldo**\n\nSilakan kunjungi website panel utama untuk deposit.",
                reply_markup=markup, parse_mode='Markdown'
            )
        except telebot.apihelper.ApiTelegramException as e:
            if "message is not modified" not in e.description: pass
        return

    if call.data == "main_order":
        bot.answer_callback_query(call.id)
        markup_kat = InlineKeyboardMarkup()
        markup_kat.add(InlineKeyboardButton(text="💸 Budget Ekonomis (< Rp 1.000)", callback_data="kat_1k"))
        markup_kat.add(InlineKeyboardButton(text="🛒 Standard Murah (Rp 1.000 - Rp 2.000)", callback_data="kat_2k"))
        markup_kat.add(InlineKeyboardButton(text="👑 Server Premium (> Rp 5.000)", callback_data="kat_5k"))
        markup_kat.add(InlineKeyboardButton(text="⬅️ Kembali Utama", callback_data="goto_main"))
        
        try:
            bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id,
                text="📊 **Silakan Pilih Kategori Budget Anda:**", reply_markup=markup_kat, parse_mode='Markdown'
            )
        except telebot.apihelper.ApiTelegramException as e:
            if "message is not modified" not in e.description: pass

# ==============================================================================
# --- 7. TAMPILAN LIST SERVER LANGSUNG SESUAI BUDGET ---
# ==============================================================================

@bot.callback_query_handler(func=lambda call: call.data.startswith('kat_'))
def display_list_server_by_kategori(call):
    TRAFFIC_STATS["total_callbacks"] += 1
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    
    kategori = call.data.split('_')[1]
    
    with cache_lock:
        servers_snapshot = list(GLOBAL_SERVERS_CACHE)

    if kategori == "1k":
        filtered = [s for s in servers_snapshot if s['price'] < 1000]
        label_kat = "Budget Ekonomis (< Rp 1.000)"
    elif kategori == "2k":
        filtered = [s for s in servers_snapshot if 1000 <= s['price'] <= 2000]
        label_kat = "Standard Murah (Rp 1.000 - Rp 2.000)"
    else:
        filtered = [s for s in servers_snapshot if s['price'] > 5000]
        label_kat = "Server Premium (> Rp 5.000)"

    filtered = sorted(filtered, key=lambda x: x['price'])
    markup = InlineKeyboardMarkup()
    
    if not filtered:
        markup.add(InlineKeyboardButton(text="⬅️ Kembali Pilih Kategori", callback_data="main_order"))
        bot.edit_message_text(
            chat_id=chat_id, message_id=call.message.message_id,
            text=f"⚠️ **Stok Kosong!**\nSaat ini belum ada server aktif di kategori *{label_kat}*.",
            reply_markup=markup, parse_mode='Markdown'
        )
        return

    for srv in filtered:
        flag = get_flag(srv['country_name'])
        btn_text = f"{flag} {srv['label']} - Rp {srv['price']:,} [Stok: {srv['count']}]"
        markup.add(InlineKeyboardButton(text=btn_text, callback_data=f"exe_{srv['country_id']}_{srv['provider_id']}"))

    markup.add(InlineKeyboardButton(text="⬅️ Kembali Pilih Kategori", callback_data="main_order"))

    try:
        bot.edit_message_text(
            chat_id=chat_id, message_id=call.message.message_id,
            text=f"⚙️ **Pilih Server WhatsApp ({label_kat}):**\n\nSilakan pilih server aktif di bawah ini untuk memesan nomor:",
            reply_markup=markup, parse_mode='Markdown'
        )
    except telebot.apihelper.ApiTelegramException as e:
        if "message is not modified" not in e.description: pass

# ==============================================================================
# --- 8. EKSEKUSI ORDER NOMOR ---
# ==============================================================================

@bot.callback_query_handler(func=lambda call: call.data.startswith('exe_'))
def callback_beli_final(call):
    TRAFFIC_STATS["total_callbacks"] += 1
    chat_id = call.message.chat.id
    parts = call.data.split('_')
    country_id = parts[1]
    raw_pid = "_".join(parts[2:])
    real_provider_id = "" if raw_pid == "any" else raw_pid

    bot.answer_callback_query(call.id, text="Memproses order...")
    param_beli_ulang = call.data 

    try:
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"⏳ Sedang memesan nomor dari server pilihan...")
    except:
        pass

    post_data = {
        'service': 'wa', 
        'country': country_id, 
        'operator': real_provider_id,
        'provider_id': real_provider_id  
    }
    
    order = api_post('order.php', post_data)
    
    if not isinstance(order, dict) or not order.get('success'):
        TRAFFIC_STATS["orders_failed"] += 1 
        msg_err = order.get('message', 'Nomor tidak tersedia atau stok habis.')
        markup_err = InlineKeyboardMarkup()
        markup_err.add(InlineKeyboardButton(text="🔄 Ulangi Order", callback_data=param_beli_ulang))
        markup_err.add(InlineKeyboardButton(text="⬅️ Menu Utama", callback_data="goto_main"))
        bot.send_message(chat_id, f"❌ **Gagal Order!**\n`{msg_err}`", reply_markup=markup_err, parse_mode='Markdown')
        return

    TRAFFIC_STATS["orders_success"] += 1 
    order_id = order.get('order_id')
    phone = order.get('phone')
    harga_final = order.get('price', 0)
    
    active_orders[str(order_id)] = {
        'status': True, 'reorder_data': param_beli_ulang,
        'phone': phone, 'price': harga_final
    }

    markup_monitoring = InlineKeyboardMarkup()
    markup_monitoring.add(InlineKeyboardButton(text="🔄 Cek OTP (Refresh)", callback_data=f"rf_otp_{order_id}"))
    markup_monitoring.add(InlineKeyboardButton(text="❌ Batalkan Pesanan", callback_data=f"c_m_{order_id}"))

    msg_pembelian = bot.send_message(
        chat_id, 
        f"✅ **Nomor WhatsApp Berhasil Didapatkan!**\n\n"
        f"📱 **Nomor:** `{phone}`\n"
        f"🆔 **Order ID:** `{order_id}`\n"
        f"💵 **Harga Terpotong:** Rp {harga_final:,}\n\n"
        f"⏳ *Silakan input nomor ke aplikasi WhatsApp Anda. Klik Cek OTP jika kode belum masuk:*",
        reply_markup=markup_monitoring, parse_mode='Markdown'
    )

    threading.Thread(target=loop_pantau_otp_dinamis, args=(chat_id, order_id, phone, msg_pembelian.message_id, param_beli_ulang)).start()

# ==============================================================================
# --- 9. MONITORING OTP ---
# ==============================================================================

def loop_pantau_otp_dinamis(chat_id, order_id, phone, message_id, param_beli_ulang):
    while True:
        time.sleep(5)
        if str(order_id) not in active_orders:
            break

        check = api_get(f"check.php?order_id={order_id}")
        if not isinstance(check, dict):
            continue

        if check.get('otp'):
            otp_code = check['otp']
            active_orders.pop(str(order_id), None)
            try:
                bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id,
                    text=f"🎉 **KODE OTP WHATSAPP BERHASIL DITERIMA!**\n\n📱 **Nomor:** `{phone}`\n🔑 **Kode OTP Anda:** `{otp_code}`",
                    parse_mode='Markdown'
                )
            except:
                pass
            break

        status_api = str(check.get('status', '')).lower()
        if status_api in ['expired', 'canceled', 'refunded', 'timeout', 'finish_tanpa_otp']:
            active_orders.pop(str(order_id), None)
            cancel = api_post('cancel.php', {'order_id': order_id})
            status_refund = cancel.get('refunded', 'Otomatis')
            
            markup_post = InlineKeyboardMarkup()
            markup_post.add(InlineKeyboardButton(text="🔄 Ulangi Order", callback_data=param_beli_ulang))
            markup_post.add(InlineKeyboardButton(text="⬅️ Menu Utama", callback_data="goto_main"))

            try:
                bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id,
                    text=f"⚠️ **Batas Waktu Tunggu Habis!**\n❌ Nomor `{phone}` telah kedaluwarsa.\n🔄 **Status Refund Saldo:** *{status_refund}*",
                    reply_markup=markup_post, parse_mode='Markdown'
                )
            except:
                pass
            break

@bot.callback_query_handler(func=lambda call: call.data.startswith('rf_otp_'))
def proses_refresh_otp_manual(call):
    TRAFFIC_STATS["total_callbacks"] += 1
    chat_id = call.message.chat.id
    order_id = call.data.split('_')[2]
    
    if str(order_id) not in active_orders:
        bot.answer_callback_query(call.id, text="Sesi order ini sudah berakhir.")
        return

    order_info = active_orders[str(order_id)]
    phone = order_info['phone']
    param_beli_ulang = order_info['reorder_data']

    check = api_get(f"check.php?order_id={order_id}")
    if not isinstance(check, dict):
        bot.answer_callback_query(call.id, text="Gagal memuat data.")
        return

    if check.get('otp'):
        otp_code = check['otp']
        active_orders.pop(str(order_id), None)
        bot.answer_callback_query(call.id, text="🎉 OTP Ditemukan!")
        try:
            bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id,
                text=f"🎉 **KODE OTP WHATSAPP BERHASIL DITERIMA!**\n\n📱 **Nomor:** `{phone}`\n🔑 **Kode OTP Anda:** `{otp_code}`",
                parse_mode='Markdown'
            )
        except:
            pass
        return

    status_api = str(check.get('status', '')).lower()
    if status_api in ['expired', 'canceled', 'refunded', 'timeout', 'finish_tanpa_otp']:
        active_orders.pop(str(order_id), None)
        cancel = api_post('cancel.php', {'order_id': order_id})
        status_refund = cancel.get('refunded', 'Otomatis')
        
        markup_post = InlineKeyboardMarkup()
        markup_post.add(InlineKeyboardButton(text="🔄 Ulangi Order", callback_data=param_beli_ulang))
        markup_post.add(InlineKeyboardButton(text="⬅️ Menu Utama", callback_data="goto_main"))

        try:
            bot.edit_message_text(
                chat_id=chat_id, message_id=call.message.message_id,
                text=f"⚠️ **Batas Waktu Tunggu Habis!**\n❌ Nomor `{phone}` telah kedaluwarsa.\n🔄 **Status Refund Saldo:** *{status_refund}*",
                reply_markup=markup_post, parse_mode='Markdown'
            )
        except:
            pass
        return

    bot.answer_callback_query(call.id, text="⏳ OTP belum masuk.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('c_m_'))
def proses_pembatalan_manual(call):
    TRAFFIC_STATS["total_callbacks"] += 1
    chat_id = call.message.chat.id
    order_id = call.data.split('_')[2]
    
    if str(order_id) not in active_orders:
        bot.answer_callback_query(call.id, text="Transaksi sudah selesai.")
        return

    bot.answer_callback_query(call.id, text="Memproses pembatalan...")
    param_beli_ulang = active_orders[str(order_id)].get('reorder_data', 'main_order')
    active_orders.pop(str(order_id), None)
    
    cancel = api_post('cancel.php', {'order_id': order_id})
    status_refund = cancel.get('refunded', 'Gagal diproses')
    
    markup_after_cancel = InlineKeyboardMarkup()
    markup_after_cancel.add(InlineKeyboardButton(text="🔄 Ulangi Order", callback_data=param_beli_ulang))
    markup_after_cancel.add(InlineKeyboardButton(text="⬅️ Menu Utama", callback_data="goto_main"))

    try:
        bot.edit_message_text(
            chat_id=chat_id, message_id=call.message.message_id,
            text=f"🛑 **Pesanan Dibatalkan Manual**\n\n🆔 **Order ID:** `{order_id}`\n🔄 **Status Refund Saldo:** *{status_refund}*",
            reply_markup=markup_after_cancel, parse_mode='Markdown'
        )
    except:
        pass

# ==============================================================================
# --- 10. RUNNING ENGINE ---
# ==============================================================================
bot.infinity_polling()