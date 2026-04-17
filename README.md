🌐 Agent Mesh - Neural Interface Pro V3.0
[ العربية ]
Agent Mesh هو نظام محاكاة متطور لإدارة وتوجيه وكلاء الذكاء الاصطناعي في الوقت الفعلي. يتميز المشروع بواجهة مستخدم مستقبلية (Neon UI) تعتمد على تقنيات الويب الحديثة، مع خادم تحكم مركزي بلغة بايثون يدير تدفق البيانات والأوامر المباشرة بين الوكلاء.
✨ المميزات الرئيسية:
نظام أوامر مباشر: تنفيذ تسلسل محدد من العمليات (تفكير، عمل، نوم، اتصال) بدقة عالية.
واجهة مستخدم ذكية: تدعم وضع "العرض المصغر" (Compact View) لمراقبة عدد كبير من الوكلاء في وقت واحد.
تفاعلات بصرية متقدمة: تغيير ألوان البطاقات ديناميكياً (أخضر للعمل، أزرق للتفكير) مع تأثيرات متحركة للأفاتار.
شبكة اتصالات حية: رسم خطوط بيانات مضيئة بين الوكلاء عند تبادل المعلومات عبر WebSockets.
[ English ]
Agent Mesh is an advanced simulation system for managing and orchestrating AI agents in real-time. The project features a futuristic "Neon UI" built with modern web technologies, controlled by a Python-based C2 server that manages data flow and direct command sequences.
✨ Key Features:
Direct Command Engine: Executes precise sequences (Thinking, Working, Sleeping, Connecting) with 2-second intervals.
Adaptive UI: Includes a "Compact View" mode to monitor dozens of agents simultaneously.
Dynamic Visuals: Cards change background colors based on state (Green for Working, Sky Blue for Thinking).
Live Connectivity: Visualizes real-time data exchange with glowing, animated connection lines between nodes.
🛠 Tech Stack | التقنيات المستخدمة
Frontend: React 18, Tailwind CSS, Lucide Icons.
Backend: Python 3.x, Flask, Flask-SocketIO.
Real-time: WebSockets (Socket.io).
Styling: Custom CSS Animations (Neon Glow, Floating Effects).
🚀 How to Run | طريقة التشغيل
1. Backend Setup (Python)
# Install dependencies
pip install flask flask-socketio flask-cors requests

# Run the server
python app.py


2. Frontend Setup
Simply open index.html in any modern web browser.
Make sure the Python server is running to see the live agent orchestration.
📁 Project Structure | هيكل المشروع
app.py: The brain of the operation (Python Server).
index.html: The futuristic dashboard (React UI).
README.md: Project documentation.
requirements.txt: Python dependencies.
📸 Screenshots | لقطات من المشروع
[![img.png](img.png)]
📜 License
This project is licensed under the MIT License.
