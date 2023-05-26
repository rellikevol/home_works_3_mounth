import aioschedule
from aiogram import Bot
import asyncio


def kill_task(tag):
    tasks = asyncio.all_tasks()
    for i in tasks:
        if i.get_name() == tag:
            i.cancel()
            return True
    return False


def schedule_(type_, interval, message, chat_id, tag, bot: Bot, time_for_day=''):
    if type_ == 'in_seconds':
        job = aioschedule.every(interval).seconds
    if type_ == 'in_minute':
        job = aioschedule.every(interval).minutes
    if type_ == 'in_days':
        if interval == "Понедельник":
            job = aioschedule.every().monday.at(time_for_day)
        if interval == "Вторник":
            job = aioschedule.every().tuesday.at(time_for_day)
        if interval == "Среда":
            job = aioschedule.every().wednesday.at(time_for_day)
        if interval == "Четверг":
            job = aioschedule.every().thursday.at(time_for_day)
        if interval == "Пятница":
            job = aioschedule.every().friday.at(time_for_day)
        if interval == "Суббота":
            job = aioschedule.every().saturday.at(time_for_day)
        if interval == "Воскресенье":
            job = aioschedule.every().sunday.at(time_for_day)
    job.do(send, chat_id, message, bot)
    job.tag(tag)
    asyncio.create_task(run(job)).set_name(tag)


def schedule_start(type_, interval, message, chat_id, tag, bot: Bot, loop, time_for_day=''):
    if type_ == 'in_seconds':
        job = aioschedule.every(interval).seconds
    if type_ == 'in_minute':
        job = aioschedule.every(interval).minutes
    if type_ == 'in_days':
        if interval == "Понедельник":
            job = aioschedule.every().monday.at(time_for_day)
        if interval == "Вторник":
            job = aioschedule.every().tuesday.at(time_for_day)
        if interval == "Среда":
            job = aioschedule.every().wednesday.at(time_for_day)
        if interval == "Четверг":
            job = aioschedule.every().thursday.at(time_for_day)
        if interval == "Пятница":
            job = aioschedule.every().friday.at(time_for_day)
        if interval == "Суббота":
            job = aioschedule.every().saturday.at(time_for_day)
        if interval == "Воскресенье":
            job = aioschedule.every().sunday.at(time_for_day)
    job.do(send, chat_id, message, bot)
    job.tag(tag)
    loop.create_task(run(job)).set_name(tag)


async def run(job: aioschedule.Job):
    while True:
        if job.should_run:
            await job.run()
        else:
            await asyncio.sleep(0.1)


async def send(chat_id, message, bot: Bot):
    await bot.send_message(chat_id, message)
