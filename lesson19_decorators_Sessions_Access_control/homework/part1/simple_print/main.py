# Напишите декоратор called, 
# который при вызове функции будет перед 
# вызовом функции выводить в консоль "функция вызвана"


# TODO напишите декратор called здесь

def called (f):
    def wrapper ():
        # print (f'The function is called.')
        print ('функция вызвана')
        f()
    return wrapper

# Ниже следует код для самопроверки:
# TODO Вы можете попробовать задекорировать функцию func
# в теле которой ничего не происходит.

@called
def func():
    pass
    # print ('The function is in progress..')

if __name__=="__main__":
    func()