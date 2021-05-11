import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord import Embed as embed
from pymongo import MongoClient
from randomvalue import random_strnum

coll = MongoClient('mongodb://localhost:27017/').Click.user

a = discord.AllowedMentions.none()

class Make_Clicks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = coll


    @commands.command(name='도움', aliases=['ehdnaakf', '도움말', 'ehdna', '명령어', 'help', "Help", "ㅗ디ㅔ"])
    async def _help(self, ctx):
        embed = discord.Embed(title='Click - 도움말', description=' ', colour=0x00FFFF, inline=False)
        embed.add_field(name='Click 이란?', value='이모지 이동을 한 번 한 것을 말합니다.', inline=False)
        embed.add_field(name='스토리 제작하기', value='`c.제작 [스토리 이름]`', inline=False)
        embed.add_field(name='스토리 관리하기', value='`c.삭제 [스토리 이름]`\n`c.수정 [스토리 이름]`', inline=False)
        embed.add_field(name='스토리 보기', value='`c.목록`(스토리 목록 불러오기)\n`c.보기 [스토리 고유 코드]`', inline=False)
        return await ctx.reply(embed=embed, allowed_mentions=a)

    @commands.command(name='제작', aliases=['wpwkr', 'create', '만들기'])
    async def _make_story(self, ctx, *, name):
        if self.coll.find_one({"_id": str(ctx.author.id)}):
            pass
        else:
            self.coll.insert_one({
                "_id": str(ctx.author.id),
                "one": None,
                "two": None,
                "three": None
            })

        dd = self.coll.find_one({"_id": str(ctx.author.id)})
        find = {"_id": str(ctx.author.id)}
        ran_strnum = random_strnum(length=10)

        if dd['one'] == None:
            setdata = {"$set": {"one": str(ran_strnum)}}

        elif dd['two'] == None:
            setdata = {"$set": {"two": str(ran_strnum)}}

        elif dd['three'] == None:
            setdata = {"$set": {"three": str(ran_strnum)}}

        self.coll.update_one(find, setdata)

        await ctx.reply('이제 내용을 입력해주세요. 다음 페이지 작성을 원할 경우 `np` 를 입력해주세요.\n스토리가 끝났다면 `end`를 입력해주세요.', allowed_mentions=a)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        now_pg = 1

        while not msg == 'end':
            msg = await self.bot.wait_for('message', check=check)
            msg = msg.content

            if msg == 'np':
                now_pg += 1

                with open(f'Stories/{str(ran_strnum)}.txt', 'w', encoding="UTF-8") as f:
                    f.write(f'\n\nPage:{str(now_pg)}\n{msg}')

                await ctx.message.add_reaction('✅')

            elif msg == 'end':
                break

        await ctx.reply(f'스토리 제작이 완료되었습니다.\n스토리의 고유 번호는 `{ran_strnum}`입니다.')


    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, CommandNotFound):
            e = embed(title=':warning: 주의', description='명령어를 찾을 수 없습니다.\n`c.도움`으로 도움말을 확인해보세요.', color=0xE1AA00)
            return await ctx.reply(embed=e, allowed_mentions=a)
        raise error



def setup(bot):
    bot.add_cog(Make_Clicks(bot))