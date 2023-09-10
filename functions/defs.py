from db.moderation import mod, dbmoderation
from json import load

with open('translate/enUS.json', encoding = 'UTF-8') as f:
    enUS = load(f)

with open('translate/ptBR.json', encoding = 'UTF-8') as f:
    ptBR = load(f)

def better_time(cd: int):

    time = f"{cd} s"

    if cd > 60:

        minutes = cd - (cd % 60)

        seconds = cd - minutes

        minutes = int(minutes / 60)

        time = f"{minutes}min {seconds}s"

        if minutes > 60:

            hoursglad = minutes - (minutes % 60)

            hours = int(hoursglad / 60)

            minutes = minutes - (hours*60)

            time = f"{hours}h {minutes}min {seconds}s"

    return time

def translates(guild):

    try:

        match mod.find_one({'_id': guild.id})['lang']:

            case 'pt-br':

                lang = ptBR

            case 'en-us':

                lang = enUS

        return lang
    
    except:

        dbmoderation.lang('lang', )