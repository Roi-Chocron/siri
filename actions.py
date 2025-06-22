import webbrowser
import re
import urllib.parse
import subprocess

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

    # This div will contain the textual part of the assistant's response.
    # Using 'system-response' class to match the CSS in index.html
    assistant_html = f'''
<div class="system-response max-w-[80%] p-3 rounded-xl shadow-md">
  <p>{user_message or "מפעיל שיר..."}</p>
</div>
'''.strip()

    # This div is the special music card.
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
    
    # Return a list of HTML blocks. They will be joined later.
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
    # Add https:// if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    domain = re.sub(r'^https?://', '', url).split('/')[0]
    search_url = url
    search_query = None
    if user_message:
        # Detect search intent (e.g., 'חפש ...', 'search ...')
        if user_message.strip().startswith(('חפש', 'search')):
            # Extract the search term (after ':', or after the first word)
            if ':' in user_message:
                search_query = user_message.split(':', 1)[1].strip()
            else:
                search_query = ' '.join(user_message.split()[1:]).strip()
            if search_query:
                encoded_query = urllib.parse.quote_plus(search_query)
                # Full Google search URL with extra params
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
    html = f'''
<div class="p-3 rounded-xl shadow-md action-message website-action-message flex items-center gap-3">
  <img src="{favicon_url}" alt="סמל אתר" class="w-6 h-6 rounded-full border border-gray-500 shadow-md">
  <p class="flex-1">{display_text}</p>
  <a href="{search_url}" target="_blank" class="text-white hover:text-blue-300 transition-colors">
    <i class="ph ph-arrow-square-out text-2xl"></i>
  </a>
</div>
'''.strip()
    return html

def decrease_brightness():
    pass

def extract_between_markers(text):
    match = re.search(r'!@#\$(.*?)!@#\$', text)
    if match:
        return match.group(1)
    return None

def extract_outside_markers(text):
    """
    Extracts all text outside the markers !@#$ ... !@#$
    """
    parts = re.split(r'!@#\$.*?!@#\$', text)
    return ''.join(parts).strip()

def run_action_from_text(text):
    """
    Parses the full text from Gemini, extracts the action and the user-facing message,
    runs the action, and prints the resulting HTML blocks separated by a delimiter.
    Handles UnicodeEncodeError safely for all output, and strips only problematic characters (emoji, non-printable, non-BMP).
    Applies code block formatting to all user/system messages.
    """
    import unicodedata
    def safe_print(s):
        # Remove only emoji and non-printable, but keep all normal text (including Hebrew, English, Windows box chars, etc.)
        if isinstance(s, str):
            filtered = []
            for c in s:
                if ord(c) > 0xFFFF:
                    continue  # skip emoji and non-BMP
                if c in ('\n', '\r', '\t') or c.isprintable():
                    filtered.append(c)
                # else skip control chars
            s = ''.join(filtered)
        print(s)

    action_call = extract_between_markers(text)
    if not action_call:
        return

    # The user-facing text is everything outside the markers.
    user_message_text = extract_outside_markers(text)

    # Basic parsing for function name and arguments
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
    }
    
    func = actions.get(func_name)
    if func:
        # Prepare positional arguments from the argument string
        args = []
        if arg_str:
            args = [a.strip().strip('"\'') for a in arg_str.split(',')]
            
        # Prepare keyword arguments
        kwargs = {}
        if user_message_text:
            kwargs['user_message'] = user_message_text
            
        # Call the function with both positional and keyword arguments
        result = func(*args, **kwargs)
        
        # If the function returns a list of HTML blocks, join them with a special delimiter.
        # Apply code block formatting to all user/system messages (not to CMD blocks)
        def format_block(block):
            if block:
                return render_markdown_with_code_blocks(block)
            return block

    if isinstance(result, list):
        safe_print('|||'.join(format_block(b) for b in result))
    elif result:
        safe_print(format_block(result))

def run_cmd(command=None, user_message=None):
    """
    Runs a command in the Windows CMD and returns the output as HTML.
    Always runs through 'cmd.exe /c' so that redirection and variables work.
    Displays the command being executed and the result.
    Adds extra debug info: the full command sent to subprocess, and exception type if any.
    Converts ; to & for Windows CMD compatibility.
    Handles echo/type for code files with special characters and removes all quotes around redirection paths.
    Replaces %USERPROFILE% (case-insensitive) בנתיב המלא לפני הרצה (באופן בטוח ל-re.sub).
    Improves HTML: Hebrew labels right-aligned, content left-aligned, debug button is clear ואינטואיטיבי, כולל חץ מסתובב ואפקט hover.
    (No emoji in HTML for maximum compatibility)
    """
    import os
    if not command:
        return "לא צוינה פקודה."
    # Convert ; to & for Windows CMD
    safe_command = command.replace(';', ' & ')
    # Expand %USERPROFILE% (case-insensitive) to the real path, safely for re.sub
    userprofile = os.environ.get('USERPROFILE')
    if userprofile:
        import re as _re
        safe_command = _re.sub(r'%USERPROFILE%', lambda m: userprofile, safe_command, flags=_re.IGNORECASE)
    # Remove any quotes (single or double) around > or >> paths, even if not closed
    import re
    def strip_quotes_after_redirect(match):
        path = match.group(2)
        # Remove leading/trailing quotes and spaces
        path = path.strip('"\' \\')
        return f"{match.group(1)} {path}"
    # Handles > "... or > '... or > ...
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
    # Only show output block if result is not empty (after stripping whitespace)
    result_str = str(result).strip() if result is not None else ''
    output_block = ''
    if result_str:
        output_block = f'''
  <div class="mb-2">
    <p class="font-bold mb-1 mt-2" style="text-align:right;direction:rtl;">פלט הפקודה:</p>
    <pre class="bg-black text-green-400 p-2 rounded-md whitespace-pre-wrap break-words text-xs" style="overflow-x:unset;white-space:pre-wrap;word-break:break-all;text-align:left;">{result_str}</pre>
  </div>'''
    # Build the CMD info block (always shown)
    cmd_block = f'''
<div class="p-3 rounded-xl shadow-md action-message cmd-action-message flex flex-col gap-2 items-stretch" style="direction:ltr;text-align:left;">
  <div class="mb-2">
    <p class="font-bold mb-1" style="text-align:right;direction:rtl;">הפקודה שהורצה:</p>
    <pre class="bg-gray-900 text-yellow-300 p-2 rounded-md whitespace-pre-wrap break-words text-xs" style="overflow-x:unset;white-space:pre-wrap;word-break:break-all;text-align:left;">{safe_command}</pre>
  </div>{output_block}
  <details class="mt-2 debug-details">
    <summary class="debug-summary" style="cursor:pointer;font-weight:bold;font-size:1rem;display:flex;align-items:center;gap:0.5em;direction:rtl;text-align:right;transition:color 0.2s;">
      <span class="debug-arrow" style="display:inline-block;transition:transform 0.2s;">
        <svg width="18" height="18" viewBox="0 0 20 20" style="vertical-align:middle;"><polyline points="6 8 10 12 14 8" fill="none" stroke="currentColor" stroke-width="2"/></svg>
      </span>
      <span>מידע דיבאג (הצג מידע נוסף)</span>
    </summary>
    <pre class="bg-gray-800 text-xs text-gray-300 p-2 rounded whitespace-pre-wrap break-words" style="overflow-x:unset;white-space:pre-wrap;word-break:break-all;text-align:left;">{'\n'.join(debug_info)}</pre>
  </details>
  <style>
    .debug-details[open] .debug-arrow {{ transform: rotate(180deg); }}
    .debug-summary:hover {{ color: #38bdf8; text-decoration: underline; }}
  </style>
</div>
'''.strip()
    # If user_message, show it as a regular system message before the CMD block
    # Add a summary/continuation message for common commands (like dir)
    summary_html = ''
    if result_str:
        # Try to add a summary for 'dir' command
        if safe_command.strip().lower().startswith('dir'):
            import re as _re
            entries = []
            for line in result_str.splitlines():
                m = _re.match(r'\s*\d{2}/\d{2}/\d{4}.*?\s([\w\u0590-\u05FF\-. ]+)$', line)
                if m:
                    name = m.group(1).strip()
                    if name not in ('.', '..'):
                        entries.append(name)
            if entries:
                # Choose format: bulleted list if <10, numbered if 10-30, table if >30
                if len(entries) <= 10:
                    # Bulleted list
                    summary_html = f'''<div class="system-response max-w-[80%] p-3 rounded-xl shadow-md mb-2"><p>הקבצים/תיקיות שנמצאו:</p><ul class="list-disc list-inside text-right rtl">{''.join(f'<li>{e}</li>' for e in entries)}</ul></div>'''
                elif len(entries) <= 30:
                    # Numbered list
                    summary_html = f'''<div class="system-response max-w-[80%] p-3 rounded-xl shadow-md mb-2"><p>הקבצים/תיקיות שנמצאו:</p><ol class="list-decimal list-inside text-right rtl">{''.join(f'<li>{e}</li>' for e in entries)}</ol></div>'''
                else:
                    # Table format for many entries
                    summary_html = f'''<div class="system-response max-w-[80%] p-3 rounded-xl shadow-md mb-2"><p>הקבצים/תיקיות שנמצאו:</p><div class="overflow-x-auto"><table class="min-w-full text-xs text-right rtl"><tbody>{''.join(f'<tr><td class="border-b border-gray-700 py-1 px-2">{e}</td></tr>' for e in entries)}</tbody></table></div></div>'''
    blocks = []
    if user_message:
        blocks.append(f'<div class="system-response max-w-[80%] p-3 rounded-xl shadow-md mb-2"><p>{user_message}</p></div>')
    if summary_html:
        blocks.append(summary_html)
    blocks.append(cmd_block)
    return blocks if len(blocks) > 1 else blocks[0]

def format_code_block(code, language="python"):
    """
    Returns a styled HTML code block with copy button and syntax highlighting for Python (or other languages).
    The code is always LTR, monospaced, and copyable. Uses PrismJS classes for syntax highlighting.
    """
    # Escape HTML special chars
    import html
    code_escaped = html.escape(code)
    # Wrap in PrismJS code block
    return f'''
<div class="code-block-container relative my-2">
  <button class="copy-btn absolute top-2 left-2 bg-blue-700 text-white text-xs px-2 py-1 rounded hover:bg-blue-800 transition" onclick="navigator.clipboard.writeText(this.nextElementSibling.innerText)">העתק</button>
  <pre class="rounded-lg bg-[#181825] text-left overflow-x-auto p-4 text-xs ltr" style="direction:ltr;">
    <code class="language-{language}">{code_escaped}</code>
  </pre>
</div>
'''.strip()

def render_markdown_with_code_blocks(text):
    """
    Finds markdown code blocks (```lang ... ```) and replaces them with HTML code blocks with copy button and syntax highlighting.
    """
    import re
    def repl(m):
        lang = m.group(1) or "python"
        code = m.group(2)
        return format_code_block(code, lang)
    # Replace all code blocks
    html = re.sub(r'```([\w\d]*)\n([\s\S]*?)```', repl, text)
    return html

if __name__ == "__main__":
    example = 'אני מפעיל את השיר "מלכת השושנים" של עדן בן זקן. !@#$play_song("עדן בן זקן", "מלכת השושנים", "Spotify")!@#$'
    print("--- Running action from text ---")
    run_action_from_text(example)
    print("\n--- End of action ---")

