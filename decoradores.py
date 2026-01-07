import datetime

def log_operacao(func):
    def wrapped(*args, **kwargs):
        agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"[{agora}] Função a ser executada [{func.__name__}]")
        return func(*args, **kwargs)
    return wrapped