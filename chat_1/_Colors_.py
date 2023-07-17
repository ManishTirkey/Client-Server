class colors:
    '''Colors class:reset all colors with colors.reset; two
    sub classes fg for foreground
    and bg for background; use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold'''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg():
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

# print(colors.reset, end="")
# print(colors.fg.black, "hello")
# print(colors.reset, end="")
# print(colors.fg.red, "hello")
# print(colors.reset, end="")
# print(colors.fg.green, "hello")
# print(colors.reset, end="")
# print(colors.fg.orange, "hello")
# print(colors.reset, end="")
# print(colors.fg.blue, "hello")
# print(colors.reset, end="")
# print(colors.fg.purple, "hello")
# print(colors.reset, end="")
# print(colors.fg.cyan, "hello")
# print(colors.reset, end="")
# print(colors.fg.lightgrey, "hello")
# print(colors.reset, end="")
# print(colors.fg.darkgrey, "hello")
# print(colors.reset, end="")
# print(colors.fg.lightred, "hello")
# print(colors.reset, end="")
# print(colors.fg.lightgreen, "hello")
# print(colors.reset, end="")
# print(colors.fg.lightblue, "hello")
# print(colors.reset, end="")
# print(colors.fg.pink, "hello", colors.fg.lightblue)
# print(colors.reset, end="")
# print("----------------------------")
# print(colors.invisible, "hello")
# print(colors.reset, end="")
# print(colors.strikethrough, "hello")
# print(colors.reset, end="")
# print(colors.reverse, "hello")
# print(colors.reset, end="")
# print(colors.underline, "hello", colors.underline)
# print(colors.reset, end="")
# print(colors.disable, "hello")
# print(colors.reset, end="")
# print(colors.bold, "hello", colors.bold)
# print(colors.reset, end="")
