# NLP-to-EDSQL-Compiler

Introduction: 
Yeh project ek Bridge ki tarah kaam karta hai jo English sentences ko samajhta hai aur unhe edSQL (English-driven SQL) mein badal kar execute karta hai.

Examples:
Search: "show students younger than 21"

Average: "find average of marks"

Count: "how many students are in the database?"

Delete: "remove student with id 10"

⚙️ Compiler Design: Phases & Working
Is project ka core logic Compiler Design ke principles par tika hai. Yeh 4 main phases mein kaam karta hai:

Lexical Analysis (Scanning): Sentence ko tukdon (tokens) mein todna aur keywords jaise find, average, id ko pehchanna.

Semantic Analysis (Logic): Tokens ka matlab nikalna (e.g., "older than" ka matlab math mein > operator hota hai).

Intermediate Code Generation: English sentence ko ek SQL-like string mein badalna (e.g., SELECT AVG(marks) FROM students;).

Code Execution: Is logic ko actual Python/Pandas command mein convert karke CSV file par chalana aur result dena.

🛠️ Technology Stack & Libraries
Yeh project puri tarah se Python ecosystem par bana hai:

Flask: Web interface aur server-side logic handle karne ke liye.

Pandas: CSV file ko as a database treat karne aur data manipulation/calculations ke liye.

Regex (re): NLP (Natural Language Processing) aur pattern matching ke liye.

HTML/CSS (Bootstrap): Ek modern aur responsive "Dark Mode" UI banane ke liye.

JavaScript: Frontend par dynamically data display karne ke liye.

🔮 Present vs Future: Kitna Useful Hai?
Present Use (Aaj ki Zarurat):
Non-Tech Users: Managers ya normal users jo database query nahi likh sakte, woh iska use karke reports nikaal sakte hain.

Quick Prototyping: Chote businesses ke liye jahan heavy SQL servers ki zarurat nahi hai, wahan CSV based data management aasaan ho jata hai.

Future Scope (Aage Kya Ho Sakta Hai?):
Voice Integration: Bhavishya mein hum isme "Speech-to-Text" add karke database se "baat" kar sakenge.

Complex Databases: Abhi yeh CSV par hai, aage chalke ise MySQL ya PostgreSQL se connect kiya ja sakta hai.

LLM Integration: OpenAI ya Google Gemini jaise models ke saath ise connect karke aur bhi complex "human-like" queries ko handle kiya ja sakta hai.

How to Run?
Python install karein.

pip install flask pandas command chalayein.

app.py ko run karein aur browser mein localhost:5000
