def wrap_text(text, max_width=40):
    """Returns wrapped text based on given maximum character width"""
    wrapped_text = ""
    for word in text.split():
        last_line = wrapped_text.split('\n')[-1]
        if len(f'{last_line} {word}') > max_width:
            wrap_char = '\n'
        else:
            wrap_char = ' '  # space
        wrapped_text = f'{wrapped_text}{wrap_char}{word.strip()}'
    print(wrapped_text)
    return wrapped_text
