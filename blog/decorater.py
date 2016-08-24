from functools import wraps
import time
import json



def login():
    """
    ***记录下api调用的输入和输出***

    """
    def decorator(func):
        """
        装饰器
        """

        def inner_decorator(view, *args, **kwargs):
            """
            **装饰器内部逻辑实现**
            """

            now = time.time()
            setattr(view.request, 'timestamp', now)
            response = func(view, *args, **kwargs)
            #setattr(response, 'elapsed_time', time.time() - now)
            access_logger.info('{model} {action}\n{request_body}\n Response: {response}'.format(
                action=view.request.method, model=view.__class__.__name__,
                request_body=view.request.body.decode('utf-8'), response=view._write_buffer))
            return None
        return wraps(func)(inner_decorator)
    return decorator