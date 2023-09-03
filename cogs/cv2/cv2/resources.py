import discord
from discord.commands import slash_command, Option
from utils.converters import FetchInvention
from utils import format_json_block
from embeds import get_default_embed

@slash_command(
    name="resources",
    description="Resources for Circuits V2, such as useful links."
)
async def resources(
    self, 
    ctx: discord.ApplicationContext
):
    await ctx.interaction.response.defer()

    em_header = get_default_embed()
    em_header.title = "Circuits V2 Resources"
    em_header.description = "[Source](<https://tyleo-rec.github.io/CircuitsV2Resources/>)"

    em_official = get_default_embed()
    em_official.title = "Official Resources"
    em_official.description = """
- [Designs](<https://tyleo-rec.github.io/CircuitsV2Resources/designs/>)
- Circuits Design System
  - If you make a Figma account, you can use these to make fancy images of chips and graphs.
  - [Chip, Port and Wire Designs](<https://www.figma.com/community/file/1070750698042818512>)
  - [Colors](<https://www.figma.com/community/file/1070759222767700948>)
- [How To Circuits V2 Blog Post](<https://blog.recroom.com/posts/2020/8/3/how-2-circuits-2>)
- [The Circuits Handbook Blog Post](<https://blog.recroom.com/posts/2021/5/03/the-circuits-handbook>)
- [Rec Room Discord](<https://discord.com/channels/193073071802941451/746858632301510708>)
  - Use the #circuits channel for Circuits info.
  - Need help? Make a thread in #circuits-help.
- [How to Create](<https://recroom.com/howtocreate>)
  - Browse to the **Circuits V2 Beginners** section.
- [Creative Classes and Events](<https://recroom.com/creative>)
  - This is a curated list of classes and events for learning how to build. Check back periodically for Circuits V2 class availability.
  - [Circuit Think Tank (Rec Room Event Link)](<https://rec.net/room/CircuitThinkTank/events>)
  - [THE Circuits V2 Class](<https://discord.gg/5AvzZt4fFh>)
- [Chip JSON](<https://github.com/tyleo-rec/CircuitsV2Resources/blob/master/misc/circuitsv2.json>)"""
    
    em_unofficial = get_default_embed()
    em_unofficial.title = "Unofficial Resources"
    em_unofficial.description = """These are additional lists of resources which may contain content not listed here.

- [rec-room Fandom Wiki Circuits V2 Page](<https://rec-room.fandom.com/wiki/Circuits_V2>)
- [It's Time For YOU To Learn Circuits V2](<https://www.youtube.com/watch?v=L4yvvoWdpWA>)
- [CV2 Chip Searcher](<https://cv2.aleteoryx.me>)
- [This Page on Cloudflare](<https://cv2.pages.dev>)
- [Circuits Documentation](<https://circuits.pages.dev/>)"""
    

    await ctx.respond(embeds=[em_header, em_official, em_unofficial])