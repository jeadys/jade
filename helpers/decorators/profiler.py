import cProfile


def check_function_profile(func):

    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        try:
            result = func(*args, **kwargs)
        finally:
            profiler.disable()
            profiler.print_stats(sort="cumtime")
        return result

    return wrapper
