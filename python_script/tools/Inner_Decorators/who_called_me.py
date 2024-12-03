import inspect
import wrapt


@wrapt.decorator
def who_called_me(wrapped, instance, args, kwargs):
    indentence = ''
    output_list = []
    parent_str = ''
    frame = inspect.currentframe()
    caller_frame = frame.f_back

    while caller_frame:
        caller_name = caller_frame.f_code.co_name
        caller_file = caller_frame.f_code.co_filename
        caller_line = caller_frame.f_lineno

        output_list.append(f"""{indentence}<'{wrapped.__name__}'>{parent_str}\n{indentence}File "{caller_file}", line {caller_line}, in <'{caller_name}'>""")
        parent_str += f"""  ->  <'{caller_name}'>"""
        caller_frame = caller_frame.f_back
        indentence += '\t'
    print('\n'.join(output_list))
    return wrapped(*args, **kwargs)
