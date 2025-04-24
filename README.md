# gekkobot
Simple AI chatbot for [Gekko](https://www.betterdays.ngo), packaged as an .exe file for Windows.

Uses Gemini Flash 2.0 model to leverage long-context.

Works as a tool for students to improve prompting skills and get a first experience with AI chatbots.

# How to configure
- Set your API key in `.env`.
- Set/Update your system prompt in `system_prompt.txt`.

# Easy Installation
1. Install [python3.11](https://www.python.org/downloads/release/python-3110/) on your computer.
2. Download the `.zip` project on [Github](https://github.com/k-schubert/gekkobot).
3. After you download `package.zip`, right-click it, choose Properties → Unblock → OK.
4. Unzip file.
5. Doubleclick `install.bat` and follow instructions.
6. Doubleclick `configure_key.bat` and follow instructions (get Gemini API key [here](https://ai.google.dev/gemini-api/docs/api-key)).
7. Go to `dist` and doubleclick on `gekkobot.exe`.
8. Go to `http://127.0.0.1:8000` in your browser.

# Dev Installation
1. Install [python3.11](https://www.python.org/downloads/release/python-3110/) on your computer.
2. Update your python PATH:
    - `Windows + S`
    - Search for `Environment Variables`
    - Add new Environment variables for `Path` (Update *YourUsername* accordingly)
        - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\`
        - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\Scripts\`
3. Open Powershell as admin and run:
    - `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
4. Clone project:
    ```
    git clone https://github.com/K-Schubert/gekkobot.git
    cd gekkobot
    ````
5. Create venv:
    ```
    python -m venv venv
    .\venv\Scripts\activate
    ```
6. Install requirements:
    ```
    pip install -r requirements.txt
    ```
7. Set API key:
    ```
    copy .env.example .env
    notepad .env # set api key
    ```
8. Run app:
    ```
    python main.py # Browse to http://127.0.0.1:8000
    ```
9. To build .exe on a Windows machine:
    ```
    pyinstaller --onefile --name gekkobot --add-data "frontend;frontend" --collect-submodules uvicorn --collect-submodules starlette main.py
    cd dist
    copy ..\.env .
    copy ..\.system_prompt .
    ```
    You can now run the executable in `dist\gekkobot.exe`.

    **Note**: the `.env` and `system_prompt.txt` must be in the `dist` folder at the same level as `gekkobot.exe` to run the executable.
