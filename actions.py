import webbrowser
import re
import urllib.parse
import subprocess
import os
import html

def play_song(artist=None, song_name=None, service=None, user_message=None):
    """
    Generates HTML for displaying a song card and the assistant's message.
    Default music service is Spotify unless specified otherwise.
    ברירת המחדל של שירות המוזיקה היא ספוטיפיי אלא אם צוין אחרת.
    Args:
        artist (str): Name of the artist.
        song_name (str): Name of the song.
        service (str, optional): Music service to use (e.g., 'Spotify', 'YouTube Music'). Defaults to 'Spotify'.
        user_message (str, optional): The message to display to the user.
    """
    if not service:
        service = "Spotify"
    if not artist:
        artist = "Unknown artist"
    if not song_name:
        song_name = "Unknown song"

    service_icon = {
        "Spotify": '<i class="ph ph-spotify-logo text-green-400 text-xl"></i>',
        "YouTube Music": '<i class="ph ph-youtube-logo text-red-500 text-xl"></i>',
    }.get(service, '')

    service_text = f"נפתח ב-{service}" if service else ""

    assistant_html = f'''
<div class="system-response max-w-[80%] p-3 rounded-xl shadow-md">
  <p>{user_message or "מפעיל שיר..."}</p>
</div>
'''.strip()

    music_html = f'''
<div class="music-action-message flex flex-col sm:flex-row items-start sm:items-center bg-[#23232b] border border-[#3a3a4d] p-4 rounded-2xl shadow-lg gap-4 mt-2 max-w-[80%] action-message">
  <img src="https://placehold.co/100x100/5C2E7E/FFFFFF?text=Song" alt="תמונת אלבום" class="w-20 h-20 rounded-xl object-cover border border-[#444] shadow-md">
  <div class="flex-1 flex flex-col justify-center">
    <div class="font-semibold text-lg text-white mb-1">{song_name}</div>
    <div class="text-sm text-[#bdbdbd] mb-2">{artist}</div>
    <div class="flex items-center gap-2 text-sm text-[#bdbdbd]">
      {service_icon}
      <span>{service_text}</span>
    </div>
  </div>
</div>
'''.strip()

    return [assistant_html, music_html]

def stop_song():
    pass

def increase_volume():
    pass

def open_website(url=None, user_message=None):
    """
    Opens the given website URL in the default web browser and returns an HTML block for display.
    If only a domain is given (e.g., 'google.com'), 'https://' will be added automatically.
    If user_message contains a search query, will perform a search on Google or supported sites with a full search URL.
    """
    if not url:
        return
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    domain = re.sub(r'^https?://', '', url).split('/')[0]
    search_url = url
    search_query = None
    if user_message:
        if user_message.strip().startswith(('חפש', 'search')):
            if ':' in user_message:
                search_query = user_message.split(':', 1)[1].strip()
            else:
                search_query = ' '.join(user_message.split()[1:]).strip()
            if search_query:
                encoded_query = urllib.parse.quote_plus(search_query)
                search_url = (
                    f'https://www.google.com/search?'
                    f'q={encoded_query}'
                    f'&sca_esv=880447038e84d9f5&sxsrf=AE3TifPhcXoEGfjMKq1QDtsqD4PVlCylzQ%3A1750605010148'
                    f'&source=hp&ei=0hxYaIXMBsKqkdUPtKnKmQE&iflsig=AOw8s4IAAAAAaFgq4s4Or31vMeMMp4bNnfIwuPrDVsEP'
                    f'&ved=0ahUKEwiF_ZPup4WOAxVCVaQEHbSUMhMQ4dUDCBc&uact=5&oq={encoded_query}'
                    f'&gs_lp=Egdnd3Mtd2l6Ig3Xnteq158g16TXqNelMgQQIxgnMggQLhiABBixAzIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAESLUUUABY3BBwAHgAkAEAmAG5AaAB0weqAQMwLje4AQPIAQD4AQGYAgegAuYHwgINECMY8AUYgAQYJxiKBcICCxAAGIAEGLEDGIMBwgIOEAAYgAQYsQMYgwEYigXCAhEQLhiABBixAxjRAxiDARjHAcICCBAAGIAEGLEDwgIEEAAYA8ICCxAuGIAEGLEDGIMBwgIFEC4YgATCAhEQLhiABBixAxiDARjHARivAcICCBAuGIAEGNQCmAMAkgcDMC43oAfoZLIHAzAuN7gH5gfCBwUwLjYuMcgHEA&sclient=gws-wiz'
                )
    webbrowser.open(search_url)
    favicon_url = f'https://{domain}/favicon.ico'
    site_name = domain
    if site_name.startswith('www.'):
        site_name = site_name[4:]
    site_name = site_name.split('.')[0].capitalize()
    display_text = f"חיפוש ב-{site_name}: {search_query}" if search_query else f"פתיחת אתר: {site_name}"
    html_content = f'''
<div class="p-3 rounded-xl shadow-md action-message website-action-message flex items-center gap-3">
  <img src="{favicon_url}" alt="סמל אתר" class="w-6 h-6 rounded-full border border-gray-500 shadow-md">
  <p class="flex-1">{display_text}</p>
  <a href="{search_url}" target="_blank" class="text-white hover:text-blue-300 transition-colors">
    <i class="ph ph-arrow-square-out text-2xl"></i>
  </a>
</div>
'''.strip()
    return html_content

def decrease_brightness():
    pass

def extract_between_markers(text):
    match = re.search(r'!@#\$(.*?)!@#\$', text)
    if match:
        return match.group(1)
    return None

def extract_outside_markers(text):
    parts = re.split(r'!@#\$.*?!@#\$', text)
    return ''.join(parts).strip()

def run_action_from_text(text):
    import unicodedata
    def safe_print(s):
        if isinstance(s, str):
            filtered = []
            for c in s:
                if ord(c) > 0xFFFF:
                    continue
                if c in ('\n', '\r', '\t') or c.isprintable():
                    filtered.append(c)
            s = ''.join(filtered)
        print(s)

    action_call = extract_between_markers(text)
    if not action_call:
        return

    user_message_text = extract_outside_markers(text)
    match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)$', action_call.strip())
    if not match:
        return

    func_name, arg_str = match.groups()

    actions = {
        "play_song": play_song,
        "stop_song": stop_song,
        "increase_volume": increase_volume,
        "open_website": open_website,
        "decrease_brightness": decrease_brightness,
        "run_cmd": run_cmd,
        "run_powershell": run_powershell, # Added run_powershell
    }

    func = actions.get(func_name)
    if func:
        args = []
        if arg_str:
            args = [a.strip().strip('"\'') for a in arg_str.split(',')]

        kwargs = {}
        if user_message_text:
            kwargs['user_message'] = user_message_text

        result = func(*args, **kwargs)

        def format_block(block):
            if block:
                return render_markdown_with_code_blocks(block)
            return block

    if isinstance(result, list):
        safe_print('|||'.join(format_block(b) for b in result if b)) # Added check for empty block
    elif result:
        safe_print(format_block(result))

def run_cmd(command=None, user_message=None):
    if not command:
        return "לא צוינה פקודה."
    safe_command = command.replace(';', ' & ')
    userprofile = os.environ.get('USERPROFILE')
    if userprofile:
        safe_command = re.sub(r'%USERPROFILE%', lambda m: userprofile, safe_command, flags=re.IGNORECASE)

    def strip_quotes_after_redirect(match):
        path = match.group(2).strip('"\' \\')
        return f"{match.group(1)} {path}"
    safe_command = re.sub(r'(>+)[ \t]*["\']?([^&|\n\r]+)["\']?', strip_quotes_after_redirect, safe_command)

    debug_info = []
    try:
        full_cmd = f'cmd.exe /c {safe_command}'
        debug_info.append(f"[DEBUG] full_cmd sent to subprocess: {full_cmd}")
        debug_info.append(f"[DEBUG] cwd: {os.getcwd()}")
        debug_info.append(f"[DEBUG] USERPROFILE: {os.environ.get('USERPROFILE')}")
        result = subprocess.check_output(full_cmd, shell=True, encoding='utf-8', stderr=subprocess.STDOUT)
        debug_info.append("[DEBUG] Command executed successfully.")
    except Exception as e:
        result = f"[EXCEPTION] {type(e).__name__}: {e}"
        debug_info.append(f"[DEBUG] Exception: {type(e).__name__}: {e}")

    result_str = str(result).strip() if result is not None else ''
    output_block = ''
    if result_str:
        output_block = f'''
  <div class="mb-2">
    <p class="font-bold mb-1 mt-2" style="text-align:right;direction:rtl;">פלט הפקודה:</p>
    <pre class="bg-black text-green-400 p-2 rounded-md whitespace-pre-wrap break-words text-xs" style="overflow-x:unset;white-space:pre-wrap;word-break:break-all;text-align:left;">{html.escape(result_str)}</pre>
  </div>'''
    cmd_block = f'''
<div class="p-3 rounded-xl shadow-md action-message cmd-action-message flex flex-col gap-2 items-stretch" style="direction:ltr;text-align:left;">
  <div class="mb-2">
    <p class="font-bold mb-1" style="text-align:right;direction:rtl;">הפקודה שהורצה:</p>
    <pre class="bg-gray-900 text-yellow-300 p-2 rounded-md whitespace-pre-wrap break-words text-xs" style="overflow-x:unset;white-space:pre-wrap;word-break:break-all;text-align:left;">{html.escape(safe_command)}</pre>
  </div>{output_block}
  <details class="mt-2 debug-details">
    <summary class="debug-summary" style="cursor:pointer;font-weight:bold;font-size:1rem;display:flex;align-items:center;gap:0.5em;direction:rtl;text-align:right;transition:color 0.2s;">
      <span class="debug-arrow" style="display:inline-block;transition:transform 0.2s;">
        <svg width="18" height="18" viewBox="0 0 20 20" style="vertical-align:middle;"><polyline points="6 8 10 12 14 8" fill="none" stroke="currentColor" stroke-width="2"/></svg>
      </span>
      <span>מידע דיבאג (הצג מידע נוסף)</span>
    </summary>
    <pre class="bg-gray-800 text-xs text-gray-300 p-2 rounded whitespace-pre-wrap break-words" style="overflow-x:unset;white-space:pre-wrap;word-break:break-all;text-align:left;">{html.escape('\n'.join(debug_info))}</pre>
  </details>
  <style>
    .debug-details[open] .debug-arrow {{ transform: rotate(180deg); }}
    .debug-summary:hover {{ color: #38bdf8; text-decoration: underline; }}
  </style>
</div>
'''.strip()
    summary_html = ''
    if result_str:
        if safe_command.strip().lower().startswith('dir'):
            entries = []
            for line in result_str.splitlines():
                m = re.match(r'\s*\d{2}/\d{2}/\d{4}.*?\s([\w\u0590-\u05FF\-. ]+)$', line)
                if m:
                    name = m.group(1).strip()
                    if name not in ('.', '..'):
                        entries.append(html.escape(name))
            if entries:
                if len(entries) <= 10:
                    summary_html = f'''<div class="system-response max-w-[80%] p-3 rounded-xl shadow-md mb-2"><p>הקבצים/תיקיות שנמצאו:</p><ul class="list-disc list-inside text-right rtl">{''.join(f'<li>{e}</li>' for e in entries)}</ul></div>'''
                elif len(entries) <= 30:
                    summary_html = f'''<div class="system-response max-w-[80%] p-3 rounded-xl shadow-md mb-2"><p>הקבצים/תיקיות שנמצאו:</p><ol class="list-decimal list-inside text-right rtl">{''.join(f'<li>{e}</li>' for e in entries)}</ol></div>'''
                else:
                    summary_html = f'''<div class="system-response max-w-[80%] p-3 rounded-xl shadow-md mb-2"><p>הקבצים/תיקיות שנמצאו:</p><div class="overflow-x-auto"><table class="min-w-full text-xs text-right rtl"><tbody>{''.join(f'<tr><td class="border-b border-gray-700 py-1 px-2">{e}</td></tr>' for e in entries)}</tbody></table></div></div>'''
    blocks = []
    if user_message:
        blocks.append(f'<div class="system-response max-w-[80%] p-3 rounded-xl shadow-md mb-2"><p>{html.escape(user_message)}</p></div>')
    if summary_html:
        blocks.append(summary_html)
    blocks.append(cmd_block)
    return blocks if len(blocks) > 1 else blocks[0]

def run_powershell(command=None, user_message=None):
    """
    Runs a command in PowerShell and returns the output as HTML.
    """
    if not command:
        return "לא צוינה פקודה."

    debug_info = []
    try:
        full_cmd = f'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "{command}"'
        debug_info.append(f"[DEBUG] full_cmd sent to subprocess: {full_cmd}")
        debug_info.append(f"[DEBUG] cwd: {os.getcwd()}")
        result = subprocess.check_output(full_cmd, shell=True, encoding='utf-8', stderr=subprocess.STDOUT)
        debug_info.append("[DEBUG] Command executed successfully.")
    except Exception as e:
        result = f"[EXCEPTION] {type(e).__name__}: {e}"
        debug_info.append(f"[DEBUG] Exception: {type(e).__name__}: {e}")

    result_str = str(result).strip() if result is not None else ''
    output_block = ''
    if result_str:
        output_block = f'''
  <div class="mb-2">
    <p class="font-bold mb-1 mt-2" style="text-align:right;direction:rtl;">פלט הפקודה:</p>
    <pre class="bg-black text-green-400 p-2 rounded-md whitespace-pre-wrap break-words text-xs" style="overflow-x:unset;white-space:pre-wrap;word-break:break-all;text-align:left;">{html.escape(result_str)}</pre>
  </div>'''

    powershell_block = f'''
<div class="p-3 rounded-xl shadow-md action-message cmd-action-message flex flex-col gap-2 items-stretch" style="direction:ltr;text-align:left;">
  <div class="mb-2">
    <p class="font-bold mb-1" style="text-align:right;direction:rtl;">הפקודה שהורצה (PowerShell):</p>
    <pre class="bg-gray-900 text-purple-300 p-2 rounded-md whitespace-pre-wrap break-words text-xs" style="overflow-x:unset;white-space:pre-wrap;word-break:break-all;text-align:left;">{html.escape(command)}</pre>
  </div>{output_block}
  <details class="mt-2 debug-details">
    <summary class="debug-summary" style="cursor:pointer;font-weight:bold;font-size:1rem;display:flex;align-items:center;gap:0.5em;direction:rtl;text-align:right;transition:color 0.2s;">
      <span class="debug-arrow" style="display:inline-block;transition:transform 0.2s;">
        <svg width="18" height="18" viewBox="0 0 20 20" style="vertical-align:middle;"><polyline points="6 8 10 12 14 8" fill="none" stroke="currentColor" stroke-width="2"/></svg>
      </span>
      <span>מידע דיבאג (הצג מידע נוסף)</span>
    </summary>
    <pre class="bg-gray-800 text-xs text-gray-300 p-2 rounded whitespace-pre-wrap break-words" style="overflow-x:unset;white-space:pre-wrap;word-break:break-all;text-align:left;">{html.escape('\n'.join(debug_info))}</pre>
  </details>
  <style>
    .debug-details[open] .debug-arrow {{ transform: rotate(180deg); }}
    .debug-summary:hover {{ color: #38bdf8; text-decoration: underline; }}
  </style>
</div>
'''.strip()

    blocks = []
    if user_message:
        blocks.append(f'<div class="system-response max-w-[80%] p-3 rounded-xl shadow-md mb-2"><p>{html.escape(user_message)}</p></div>')
    blocks.append(powershell_block)
    return blocks if len(blocks) > 1 else blocks[0]

def format_code_block(code, language="python"):
    code_escaped = html.escape(code)
    return f'''
<div class="code-block-container relative my-2">
  <button class="copy-btn absolute top-2 left-2 bg-blue-700 text-white text-xs px-2 py-1 rounded hover:bg-blue-800 transition" onclick="navigator.clipboard.writeText(this.nextElementSibling.innerText)">העתק</button>
  <pre class="rounded-lg bg-[#181825] text-left overflow-x-auto p-4 text-xs ltr" style="direction:ltr;">
    <code class="language-{language}">{code_escaped}</code>
  </pre>
</div>
'''.strip()

def render_markdown_with_code_blocks(text):
    def repl(m):
        lang = m.group(1) or "python"
        code = m.group(2)
        return format_code_block(code, lang)
    html_content = re.sub(r'```([\w\d]*)\n([\s\S]*?)```', repl, text)
    return html_content

if __name__ == "__main__":
    example = 'אני מפעיל את השיר "מלכת השושנים" של עדן בן זקן. !@#$play_song("עדן בן זקן", "מלכת השושנים", "Spotify")!@#$'
    print("--- Running action from text ---")
    run_action_from_text(example)
    print("\n--- End of action ---")

    # Example for run_cmd
    cmd_example = 'מציג את רשימת הקבצים בתיקייה הנוכחית. !@#$run_cmd("dir")!@#$'
    print("\n--- Running CMD action from text ---")
    run_action_from_text(cmd_example)
    print("\n--- End of CMD action ---")

    # Example for run_powershell
    powershell_example = 'מציג את התהליכים הרצים במערכת באמצעות PowerShell. !@#$run_powershell("Get-Process")!@#$'
    print("\n--- Running PowerShell action from text ---")
    run_action_from_text(powershell_example)
    print("\n--- End of PowerShell action ---")
