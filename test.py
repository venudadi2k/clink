import os , re , time , sqlite3
from mydbfunctions import get_pending,approve_url,insert_into_pending,get_valid
from discord.ext import commands

try:
	
    # Connect to DB and create a cursor
    conn = sqlite3.connect('mydb')
    cursor = conn.cursor()
    print('Connected to database')

    
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    bot = commands.Bot(command_prefix="clink.")

    valid_members = ['Ethermon-Team','Lead Mod','Moderator','Mod in Training','Bot']
    channels = ['tests']

    def isValidURL(url):
        regex = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" + "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")
        p = re.compile(regex)
        if (url == None):
                return False
        if(re.search(p, url)):
                return True
        else:
                return False

    def check_permission(context):
        for i in context.message.author.roles:
            if i.name in valid_members:
                return True
        return False

    def ignore(message):
        for i in message.author.roles:
            if i.name in valid_members:
                return True
        return False

    @bot.event
    async def on_ready():
        for i in bot.guilds:
          print(f'{bot.user.name} has connected to server {i.name} ')
    

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return 
        if message.channel.name in channels:
          valid = False
          url = message.content
          if ignore(message) == False: 
            if isValidURL(message.content):
              valid_domain = get_valid(cursor)  
              for i in valid_domain:
                  if i[0] in url:
                      valid = True
              if (valid == False) or ('https' not in url):
                  id = time.time_ns()
                  id = insert_into_pending(cursor,conn,id,url)
                    
                  await message.delete()
                  await message.channel.send('External Link Found id {} assigned to request for link validation !!!'.format(id))
                  

        await bot.process_commands(message)

    @bot.command(help='To check the list of pending url\'s which are to be validated')
    async def plist(context):
        if context.channel.name in channels:
          output = get_pending(cursor)
          if len(output) == 0:
              await context.channel.send('No pending url\'s')
          else :
              pendinglist = '' 
              for i in output:
                  pendinglist += '{} {}\n'.format(i[0],i[1].split('//')[1])
              await context.channel.send(pendinglist)

    @bot.command(help='To check the list of whitelisted url\'s ')
    async def vlist(context):
        if context.channel.name in channels:
          output = get_valid(cursor)
          if len(output) == 0:
              await context.channel.send('No valid url\'s')
          else :
              whitelist = ''
              for i in output:
                  whitelist += '{}\n'.format(i[0])
              await context.channel.send(whitelist)

    @bot.command(help='This is used to approve the pending url\'s ')
    @commands.check(check_permission)
    async def approve(context):
        if context.channel.name in channels:
          a_id = context.message.content.split(" ")[1]
          a_url = approve_url(cursor,conn,a_id)
          await context.channel.send('url : {}\nid : {}\napproved by : {}\n'.format(a_url[0][1],a_id,context.message.author.name))


    @bot.command(help='This is used to delete the pending url\'s ')
    @commands.check(check_permission)
    async def disapprove(context):
        if context.channel.name in channels:
          print('function called')
          d_id = context.message.content.split(" ")[1]
          d_id = delete_from_pending(cursor,conn,d_id)
          print('funtion returned') 
          await context.channel.send('url with id : {} has be disapproved by {}'.format(d_id,context.message.author.name))


    @bot.event
    async def on_command_error(context,error):
        if context.channel.name in channels:
          if isinstance(error, commands.CheckFailure):
            await context.channel.send('You don\'t have permissions to run this command')

    bot.run(DISCORD_TOKEN)


    # Close the cursor
    cursor.close()

# Handle errors
except sqlite3.Error as error:
    print('Error occured - ', error)

# Close DB Connection irrespective of successor failure
finally:
    if conn:
        conn.close()
        print('SQLite Connection closed')