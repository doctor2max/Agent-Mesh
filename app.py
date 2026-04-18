
import time
import threading
import uuid
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from telebot import types
from contextlib import contextmanager
import os
from dotenv import load_dotenv
import telebot
# ==========================================
# 1. الإعدادات العامة (Configuration)
# ==========================================


# تحميل المتغيرات من ملف .env
load_dotenv()

# استدعاء المفتاح باستخدام os
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# التأكد من أن المفتاح تم تحميله بنجاح
if not API_TOKEN:
    print("❌ خطأ: لم يتم العثور على TELEGRAM_BOT_TOKEN في ملف .env")
else:
    bot = telebot.TeleBot(API_TOKEN)
    print("✅ تم تحميل مفتاح البوت بنجاح من البيئة.")

app = Flask(__name__)
CORS(app)
# السماح بجميع الاتصالات (مهم لتجنب مشاكل CORS مع React)
socketio = SocketIO(app, cors_allowed_origins="*")


# ==========================================
# 2. كلاس الوكيل (Agent Entity)
# ==========================================
class Agent:
    def __init__(self, name, role, gender, color, agent_id=None):
        self.id = str(agent_id) if agent_id else str(uuid.uuid4())[:6]
        self.name = name
        self.role = role
        self.gender = gender
        self.color = color
        self.status = "sleeping"

    def set_status(self, status):
        """تحديث حالة الوكيل وبثها فوراً لكل الواجهات المتصلة"""
        self.status = status
        socketio.emit('ui_command', {
            "agent_id": self.id,
            "action": status  # الواجهة تتوقع 'working', 'sleeping', 'thinking'
        })

    def to_dict(self):
        """تحضير الكائن للإرسال عبر الشبكة كـ JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "gender": self.gender,
            "color": self.color,
            "status": self.status
        }


# ==========================================
# 3. مدير الشبكة (Mesh Manager)
# ==========================================
class AgentMeshManager:
    def __init__(self):
        self.agents = {}  # مخزن الذاكرة المركزي

    def create_agent(self, name, role, gender, color, agent_id=None):
        """إنشاء الكائن في الذاكرة وإرساله للواجهة"""
        new_agent = Agent(name, role, gender, color, agent_id)
        self.agents[new_agent.id] = new_agent
        socketio.emit('add_agent', new_agent.to_dict())
        return new_agent

    def get_agent(self, agent_id):
        return self.agents.get(str(agent_id))

    def log(self, text, msg_type="info"):
        """إرسال سجل للوحة الجانبية في الواجهة"""
        socketio.emit('server_log', {'text': text, 'type': msg_type})

    def connect_visual(self, source_id, target_id, log_msg=None):
        """رسم خط اتصال بين وكيلين"""
        socketio.emit('ui_command', {
            "agent_id": str(source_id),
            "target_id": str(target_id),
            "action": "connection"
        })
        if log_msg:
            self.log(log_msg)

    @contextmanager
    def task(self, agent_id):
        """مدير سياق (Context Manager) للتحكم التلقائي بحالة الوكيل"""
        agent = self.get_agent(agent_id)
        if agent:
            agent.set_status("working")
            try:
                yield agent
            finally:
                agent.set_status("sleeping")
        else:
            self.log(f"تحذير: الوكيل {agent_id} غير متوفر!", "error")
            yield None


# نسخة عالمية من المدير
mesh = AgentMeshManager()


# ==========================================
# 4. التوليد الأولي للوكلاء (Initialization)
# ==========================================
def initialize_system_agents():
    """
    هذه الدالة تعمل مرة واحدة فقط عند إقلاع السيرفر.
    نقوم هنا بتعريف الـ IDs بشكل ثابت لكي لا تتكرر الكائنات.
    """
    print("[نظام] جاري تهيئة وكلاء الشبكة الأساسيين...")
    if not mesh.agents:  # التأكد من أن الذاكرة فارغة
        mesh.create_agent("المنسق MAX", "System Core", "male", "#6366f1", "core_1")
        mesh.create_agent("المحلل الذكي", "Data Engine", "male", "#10b981", "data_1")
        mesh.create_agent("الأمن السيبراني", "Security", "female", "#ec4899", "sec_1")
        mesh.create_agent("I.T", "Security", "female", "#ec4899", "sec_2")
    print("✅ تم تحميل الوكلاء في الذاكرة بنجاح.")


# ==========================================
# 5. نقاط اتصال SocketIO (Endpoints)
# ==========================================
@socketio.on('connect')
def handle_connect():
    """عند فتح الواجهة (React)، نرسل لها كل الكائنات الموجودة في الذاكرة"""
    print("--- [شبكة] واجهة جديدة اتصلت ---")
    current_agents = [a.to_dict() for a in mesh.agents.values()]
    emit('set_agents', current_agents)  # استخدام set_agents لاستبدال القائمة بالكامل
    mesh.log("تم مزامنة حالة الذاكرة مع الواجهة", "success")


# ==========================================
# 6. مهام وعمليات الذكاء الاصطناعي (Tasks)
# ==========================================
def start_coordinated_process(chat_id):
    """
    مهمة متكاملة: تستدعي الوكلاء (ولا تنشئهم) لتنفيذ العمليات.
    يمكنك تكرار هذه الدالة مئة مرة دون أن يتضاعف الوكلاء.
    """
    mesh.log("بدء دورة المعالجة الذكية...", "info")

    try:
        # استخدام المعرفات الثابتة التي أنشأناها في دالة initialize_system_agents
        with mesh.task("core_1"):
            mesh.log("المنسق يقوم بفحص الطلب...")
            time.sleep(1.5)

            # اتصال بصرى
            mesh.connect_visual("core_1", "data_1", "توجيه البيانات للمحلل")

            with mesh.task("data_1"):
                mesh.log("جاري معالجة البيانات وتحليلها...")
                time.sleep(2.5)

            # اتصال بصرى
            mesh.connect_visual("data_1", "sec_1", "فحص التشفير والأمان")

            with mesh.task("sec_1"):
                mesh.log("تأمين المخرجات...")
                time.sleep(1.5)

            # اتصال بصرى
            mesh.connect_visual("sec_2", "core_1", "فحص السيرفر")

            with mesh.task("core_1"):
                mesh.log(" فحص السيرفر تم...")
                time.sleep(1.5)

        mesh.log("اكتملت جميع العمليات بنجاح", "success")
        bot.send_message(chat_id, "✅ اكتملت الدورة الذكية بنجاح! راجع لوحة التحكم.")

    except Exception as e:
        mesh.log(f"حدث خطأ في النظام: {str(e)}", "error")


def run_five_seconds_test(chat_id):
    """مهمة مؤقتة لاختبار وكيل واحد"""
    agent_id = "core_1"
    mesh.log(f"بدء اختبار 5 ثواني للوكيل {agent_id}", "info")

    with mesh.task(agent_id):
        time.sleep(5)

    mesh.log("انتهى الاختبار وعاد الوكيل للسبات.", "success")
    bot.send_message(chat_id, "⏱️ انتهى اختبار الـ 5 ثواني.")


# ==========================================
# 7. أوامر بوت التيليجرام (Telegram Handlers)
# ==========================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('تشغيل الشبكة ⚡'), types.KeyboardButton('اختبار 5 ثواني ⏱️'))
    bot.reply_to(message, "مرحباً دكتور MAX! نظام AgentMesh جاهز ومستقر.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "تشغيل الشبكة ⚡")
def handle_run(message):
    bot.send_message(message.chat.id, "🚀 جاري تفعيل الوكلاء وإرسال المهام...")
    threading.Thread(target=start_coordinated_process, args=(message.chat.id,), daemon=True).start()


@bot.message_handler(func=lambda message: message.text == "اختبار 5 ثواني ⏱️")
def handle_test(message):
    bot.send_message(message.chat.id, "⏳ تشغيل اختبار المهمة المؤقتة...")
    threading.Thread(target=run_five_seconds_test, args=(message.chat.id,), daemon=True).start()


# ==========================================
# 8. تشغيل النظام (Main Entry Point)
# ==========================================
if __name__ == '__main__':
    # 1. توليد الوكلاء في الذاكرة أولاً (مرة واحدة فقط)
    initialize_system_agents()

    # 2. تشغيل بوت التيليجرام في الخلفية
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()

    print("\n🚀 [AgentMesh] السيرفر يعمل على: http://127.0.0.1:5000\n")

    # 3. تشغيل سيرفر الـ SocketIO
    socketio.run(app, host='127.0.0.1', port=5000, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)