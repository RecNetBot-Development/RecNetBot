import discord
import random
from typing import Optional, Dict
from discord.ext import pages
from discord.ext.pages import Page, PageGroup
from resources import get_emoji
from recnetpy.dataclasses.account import Account
from recnetpy.dataclasses.room import Room
from recnetpy.dataclasses.event import Event
from recnetpy.dataclasses.invention import Invention
from embeds import event_embed, fetch_profile_embed, fetch_invention_embed, room_embed, fetch_image_embed, fetch_event_embed
from recnetpy.dataclasses.image import Image
from typing import List, Optional, Union
from discord.ext.bridge import BridgeContext
from discord.ext.commands import Context
        
class RNBPaginatorButton(discord.ui.Button):
    def __init__(
        self,
        button_type: str,
        label: str = None,
        emoji: Union[str, discord.Emoji, discord.PartialEmoji] = None,
        style: discord.ButtonStyle = discord.ButtonStyle.green,
        disabled: bool = False,
        custom_id: str = None,
        row: int = 0,
        loop_label: str = None,
    ):
        super().__init__(
            label=label if label or emoji else button_type.capitalize(),
            emoji=emoji,
            style=style,
            disabled=disabled,
            custom_id=custom_id,
            row=row,
        )
        self.button_type = button_type
        self.label = label if label or emoji else button_type.capitalize()
        self.emoji: Union[str, discord.Emoji, discord.PartialEmoji] = emoji
        self.style = style
        self.disabled = disabled
        self.loop_label = self.label if not loop_label else loop_label
        self.paginator = None

    async def callback(self, interaction: discord.Interaction):
        # Make sure it's the author using the component
        if interaction.message.interaction and interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.response.send_message("You're not authorized!", ephemeral=True)

        if self.button_type == "first":
            self.paginator.current_page = 0
            
        elif self.button_type == "prev":
            if self.paginator.loop_pages and self.paginator.current_page == 0:
                self.paginator.current_page = self.paginator.page_count
            else:
                self.paginator.current_page -= 1
                
        elif self.button_type == "next":
            if (
                self.paginator.loop_pages
                and self.paginator.current_page == self.paginator.page_count
            ):
                self.paginator.current_page = 0
            else:
                self.paginator.current_page += 1
                
        elif self.button_type == "prev10":
            if self.paginator.loop_pages and self.paginator.current_page == 0:
                self.paginator.current_page = self.paginator.page_count
            else:
                self.paginator.current_page -= 10
                
        elif self.button_type == "next10":
            if (
                self.paginator.loop_pages
                and self.paginator.current_page == self.paginator.page_count
            ):
                self.paginator.current_page = 0
            else:
                self.paginator.current_page += 10
                
        elif self.button_type == "random":
            self.paginator.current_page = random.randint(0, self.paginator.page_count)
                
        elif self.button_type == "last":
            self.paginator.current_page = self.paginator.page_count
            
        await self.paginator.goto_page(
            page_number=self.paginator.current_page, interaction=interaction
        )
        
class RNBPage(Page):
    def __init__(self, *args, **kwargs):
        if args: self.data = args[0]
        self.index = kwargs.pop("index", 0)
        self.page_count = kwargs.pop("page_count", 0)
        
        super().__init__(*args, **kwargs)
    

    async def callback(self, interaction: Optional[discord.Interaction] = None):
        """
        Executes when the page is displayed
        """
    
        if isinstance(self.content, Account):
            self.embeds.append(await fetch_profile_embed(self.data))
            self.content = None
            
        elif isinstance(self.content, Room):
            room = await self.data.client.rooms.fetch(self.data.id, 78)
            self.embeds.append(room_embed(room))
            self.content = None
            
        elif isinstance(self.content, Event):
            self.embeds.append(await fetch_event_embed(self.data))
            self.content = None
            
        elif isinstance(self.content, Invention):
            self.embeds.append(await fetch_invention_embed(self.data))
            self.content = None
            
        elif isinstance(self.content, Image):
            self.embeds.append(await fetch_image_embed(self.data))
            self.content = None
            
        self.embeds[-1].set_footer(text=f"{self.index:,}/{self.page_count:,}")


class RNBPaginator(pages.Paginator):
    def __init__(self, *args, **kwargs):
        self.constant_embed = kwargs.pop("constant_embed", None)
        self.hidden_items = kwargs.pop("hidden_items", [])
        super().__init__(*args, **kwargs)

        # Component timeout
        self.timeout = 600
        self.disable_on_timeout = True

        # For indicator
        for i, page in enumerate(self.pages, start=1):
            page.index, page.page_count = i, self.page_count + 1
        
    
    def update_buttons(self) -> Dict:
        for key, button in self.buttons.items():
            if key == "first":
                if self.page_count >= 1:
                    if self.current_page <= 1:
                        button["hidden"] = True
                    elif self.current_page >= 1:
                        button["hidden"] = False
                else:
                    self.hidden_items.append(key)
            elif key == "last":
                if self.page_count >= 1:
                    if self.current_page >= self.page_count - 1:
                        button["hidden"] = True
                    if self.current_page < self.page_count - 1:
                        button["hidden"] = False
                else:
                    self.hidden_items.append(key)
            elif key == "next":
                if self.page_count >= 1:
                    if self.current_page == self.page_count:
                        if not self.loop_pages:
                            button["hidden"] = True
                            button["object"].label = button["label"]
                        else:
                            button["object"].label = button["loop_label"]
                    elif self.current_page < self.page_count:
                        button["hidden"] = False
                        button["object"].label = button["label"]
                else:
                    self.hidden_items.append(key)
            elif key == "next10":
                if self.page_count >= 10:
                    if self.current_page + 10 > self.page_count:
                        if not self.loop_pages:
                            button["hidden"] = True
                            button["object"].label = button["label"]
                        else:
                            button["object"].label = button["loop_label"]
                    elif self.current_page + 10 <= self.page_count:
                        button["hidden"] = False
                        button["object"].label = button["label"]
                else:
                    self.hidden_items.append(key)
            elif key == "prev10":
                if self.page_count >= 10:
                    if self.current_page - 10 < 0:
                        if not self.loop_pages:
                            button["hidden"] = True
                            button["object"].label = button["label"]
                        else:
                            button["object"].label = button["loop_label"]
                    elif self.current_page - 10 < self.page_count:
                        button["hidden"] = False
                        button["object"].label = button["label"]
                else:
                    self.hidden_items.append(key)
            elif key == "prev":
                if self.page_count >= 1:
                    if self.current_page <= 0:
                        if not self.loop_pages:
                            button["hidden"] = True
                            button["object"].label = button["label"]
                        else:
                            button["object"].label = button["loop_label"]
                    elif self.current_page >= 0:
                        button["hidden"] = False
                        button["object"].label = button["label"]
                else:
                    self.hidden_items.append(key)
            elif key == "random":
                if self.page_count >= 1:
                    button["hidden"] = False
                else:
                    self.hidden_items.append(key)
                    
        self.clear_items()
        if self.show_indicator:
            self.buttons["page_indicator"]["object"].label = f"{self.current_page + 1}/{self.page_count + 1}"
        for key, button in self.buttons.items():
            if key in self.hidden_items:
                continue
            
            if key != "page_indicator":
                if button["hidden"]:
                    button["object"].disabled = True
                    if self.show_disabled:
                        self.add_item(button["object"])
                else:
                    button["object"].disabled = False
                    self.add_item(button["object"])
            elif self.show_indicator:
                self.add_item(button["object"])

        if self.show_menu:
            self.add_menu()

        # We're done adding standard buttons and menus, so we can now add any specified custom view items below them
        # The bot developer should handle row assignments for their view before passing it to Paginator
        if self.custom_view:
            self.update_custom_view(self.custom_view)

        return self.buttons
        
        
    async def goto_page(
        self, page_number: int = 0, *, interaction: Optional[discord.Interaction] = None
    ) -> None:
        self.update_buttons()
        self.current_page = page_number
        if self.show_indicator:
            self.buttons["page_indicator"][
                "object"
            ].label = f"{self.current_page + 1}/{self.page_count + 1}"

        if self.trigger_on_display:
            await self.page_action(interaction=interaction)

        page = self.pages[page_number]
        page = self.get_page_content(page)

        if page.custom_view:
            self.update_custom_view(page.custom_view)

        files = page.update_files()

        if interaction:
            if not interaction.response.is_done():
                await interaction.response.defer()  # needed to force webhook message edit route for files kwarg support
            await interaction.followup.edit_message(
                message_id=self.message.id,
                content=page.content,
                embeds=page.embeds,
                attachments=[],
                files=files or [],
                view=self,
            )
        else:
            await self.message.edit(
                content=page.content,
                embeds=page.embeds,
                attachments=[],
                files=files or [],
                view=self,
            )
            
    async def respond(
        self,
        interaction: Union[discord.Interaction, BridgeContext],
        ephemeral: bool = False,
        target: Optional[discord.abc.Messageable] = None,
        target_message: str = "Paginator sent!",
    ) -> Union[discord.Message, discord.WebhookMessage]:
        if not isinstance(interaction, (discord.Interaction, BridgeContext)):
            raise TypeError(
                f"expected Interaction or BridgeContext, not {interaction.__class__!r}"
            )

        if target is not None and not isinstance(target, discord.abc.Messageable):
            raise TypeError(f"expected abc.Messageable not {target.__class__!r}")

        if ephemeral and (self.timeout >= 900 or self.timeout is None):
            raise ValueError(
                "paginator responses cannot be ephemeral if the paginator timeout is 15 minutes or greater"
            )

        self.update_buttons()

        if self.trigger_on_display:
            await self.page_action(interaction=interaction)

        page: Union[Page, str, discord.Embed, List[discord.Embed]] = self.pages[
            self.current_page
        ]
        page_content: Page = self.get_page_content(page)

        if page_content.custom_view:
            self.update_custom_view(page_content.custom_view)

        if isinstance(interaction, discord.Interaction):
            self.user = interaction.user

            if target:
                await interaction.response.send_message(
                    target_message, ephemeral=ephemeral
                )
                msg = await target.send(
                    content=page_content.content,
                    embeds=page_content.embeds,
                    files=page_content.files,
                    view=self,
                )
            elif interaction.response.is_done():
                msg = await interaction.followup.send(
                    content=page_content.content,
                    embeds=page_content.embeds,
                    files=page_content.files,
                    view=self,
                    ephemeral=ephemeral,
                )
                # convert from WebhookMessage to Message reference to bypass
                # 15min webhook token timeout (non-ephemeral messages only)
                if not ephemeral:
                    msg = await msg.channel.fetch_message(msg.id)
            else:
                msg = await interaction.response.send_message(
                    content=page_content.content,
                    embeds=page_content.embeds,
                    files=page_content.files,
                    view=self,
                    ephemeral=ephemeral,
                )
        else:
            ctx = interaction
            self.user = ctx.author
            if target:
                await ctx.respond(target_message, ephemeral=ephemeral)
                msg = await ctx.send(
                    content=page_content.content,
                    embeds=page_content.embeds,
                    files=page_content.files,
                    view=self,
                )
            else:
                msg = await ctx.respond(
                    content=page_content.content,
                    embeds=page_content.embeds,
                    files=page_content.files,
                    view=self,
                )
        if isinstance(msg, (discord.Message, discord.WebhookMessage)):
            self.message = msg
        elif isinstance(msg, discord.Interaction):
            self.message = await msg.original_response()

        return self.message
    
    
    async def edit(
        self,
        message: discord.Message,
        suppress: Optional[bool] = None,
        allowed_mentions: Optional[discord.AllowedMentions] = None,
        delete_after: Optional[float] = None,
    ) -> Optional[discord.Message]:
        if not isinstance(message, discord.Message):
            raise TypeError(f"expected Message not {message.__class__!r}")

        self.update_buttons()

        if self.trigger_on_display:
            await self.page_action()

        page: Union[Page, str, discord.Embed, List[discord.Embed]] = self.pages[
            self.current_page
        ]
        page_content: Page = self.get_page_content(page)

        if page_content.custom_view:
            self.update_custom_view(page_content.custom_view)

        self.user = message.author

        try:
            self.message = await message.edit(
                content=page_content.content,
                embeds=page_content.embeds,
                files=page_content.files,
                attachments=[],
                view=self,
                suppress=suppress,
                allowed_mentions=allowed_mentions,
                delete_after=delete_after,
            )
        except (discord.NotFound, discord.Forbidden):
            pass

        return self.message
    
    
    async def send(
        self,
        ctx: Context,
        target: Optional[discord.abc.Messageable] = None,
        target_message: Optional[str] = None,
        reference: Optional[
            Union[discord.Message, discord.MessageReference, discord.PartialMessage]
        ] = None,
        allowed_mentions: Optional[discord.AllowedMentions] = None,
        mention_author: Optional[bool] = None,
        delete_after: Optional[float] = None,
    ) -> discord.Message:
        if not isinstance(ctx, Context):
            raise TypeError(f"expected Context not {ctx.__class__!r}")

        if target is not None and not isinstance(target, discord.abc.Messageable):
            raise TypeError(f"expected abc.Messageable not {target.__class__!r}")

        if reference is not None and not isinstance(
            reference,
            (discord.Message, discord.MessageReference, discord.PartialMessage),
        ):
            raise TypeError(
                f"expected Message, MessageReference, or PartialMessage not {reference.__class__!r}"
            )

        if allowed_mentions is not None and not isinstance(
            allowed_mentions, discord.AllowedMentions
        ):
            raise TypeError(
                f"expected AllowedMentions not {allowed_mentions.__class__!r}"
            )

        if mention_author is not None and not isinstance(mention_author, bool):
            raise TypeError(f"expected bool not {mention_author.__class__!r}")

        self.update_buttons()
        
        if self.trigger_on_display:
            await self.page_action()
        
        page = self.pages[self.current_page]
        page_content = self.get_page_content(page)

        if page_content.custom_view:
            self.update_custom_view(page_content.custom_view)

        self.user = ctx.author

        if target:
            if target_message:
                await ctx.send(
                    target_message,
                    reference=reference,
                    allowed_mentions=allowed_mentions,
                    mention_author=mention_author,
                )
            ctx = target

        self.message = await ctx.send(
            content=page_content.content,
            embeds=page_content.embeds,
            files=page_content.files,
            view=self,
            reference=reference,
            allowed_mentions=allowed_mentions,
            mention_author=mention_author,
            delete_after=delete_after,
        )

        return self.message

    
    
    #@staticmethod
    def get_page_content(
        self,
        page: Union[Page, str, discord.Embed, List[discord.Embed]]
    ) -> Page:
        """Converts a page into a :class:`Page` object based on its content."""
        return_page = None
        
        if isinstance(page, Page):
            return_page = page
        elif isinstance(page, str):
            return_page = Page(content=page, embeds=[], files=[])
        elif isinstance(page, discord.Embed):
            return_page = Page(content=None, embeds=[page], files=[])
        elif isinstance(page, discord.File):
            return_page = Page(content=None, embeds=[], files=[page])
        elif isinstance(page, List):
            if all(isinstance(x, discord.Embed) for x in page):
                return_page = Page(content=None, embeds=page, files=[])
            if all(isinstance(x, discord.File) for x in page):
                return_page = Page(content=None, embeds=[], files=page)
            else:
                raise TypeError("All list items must be embeds or files.")
        else:
            raise TypeError(
                "Page content must be a Page object, string, an embed, a list of embeds, a file, or a list of files."
            )
            
        if self.constant_embed:
            return_page.embeds.insert(0, self.constant_embed)
            return return_page
        return return_page
            

    async def update(
        self,
        pages: Optional[
            Union[
                List[PageGroup],
                List[Page],
                List[str],
                List[Union[List[discord.Embed], discord.Embed]],
            ]
        ] = None,
        show_disabled: Optional[bool] = None,
        show_indicator: Optional[bool] = None,
        show_menu: Optional[bool] = None,
        author_check: Optional[bool] = None,
        menu_placeholder: Optional[str] = None,
        disable_on_timeout: Optional[bool] = None,
        use_default_buttons: Optional[bool] = None,
        default_button_row: Optional[int] = None,
        loop_pages: Optional[bool] = None,
        custom_view: Optional[discord.ui.View] = None,
        timeout: Optional[float] = None,
        custom_buttons: Optional[List[RNBPaginatorButton]] = None,
        trigger_on_display: Optional[bool] = None,
        interaction: Optional[discord.Interaction] = None,
    ):

        # Update pages and reset current_page to 0 (default)
        self.pages: Union[
            List[PageGroup],
            List[str],
            List[Page],
            List[Union[List[discord.Embed], discord.Embed]],
        ] = (
            pages if pages is not None else self.pages
        )
        self.show_menu = show_menu if show_menu is not None else self.show_menu
        if pages is not None and all(isinstance(pg, PageGroup) for pg in pages):
            self.page_groups = self.pages if self.show_menu else None
            if sum(pg.default is True for pg in self.page_groups) > 1:
                raise ValueError("Only one PageGroup can be set as the default.")
            for pg in self.page_groups:
                if pg.default:
                    self.default_page_group = self.page_groups.index(pg)
                    break
            self.pages: List[Page] = self.get_page_group_content(
                self.page_groups[self.default_page_group]
            )
        self.page_count = max(len(self.pages) - 1, 0)
        
        # For indicator
        for i, page in enumerate(self.pages, start=1):
            page.index, page.page_count = i, self.page_count + 1
        
        self.current_page = 0
        # Apply config changes, if specified
        self.show_disabled = (
            show_disabled if show_disabled is not None else self.show_disabled
        )
        self.show_indicator = (
            show_indicator if show_indicator is not None else self.show_indicator
        )
        self.usercheck = author_check if author_check is not None else self.usercheck
        self.menu_placeholder = (
            menu_placeholder if menu_placeholder is not None else self.menu_placeholder
        )
        self.disable_on_timeout = (
            disable_on_timeout
            if disable_on_timeout is not None
            else self.disable_on_timeout
        )
        self.use_default_buttons = (
            use_default_buttons
            if use_default_buttons is not None
            else self.use_default_buttons
        )
        self.default_button_row = (
            default_button_row
            if default_button_row is not None
            else self.default_button_row
        )
        self.loop_pages = loop_pages if loop_pages is not None else self.loop_pages
        self.custom_view: discord.ui.View = None if custom_view is None else custom_view
        self.timeout: float = timeout if timeout is not None else self.timeout
        self.trigger_on_display = (
            trigger_on_display
            if trigger_on_display is not None
            else self.trigger_on_display
        )
        if custom_buttons and not self.use_default_buttons:
            self.buttons = {}
            for button in custom_buttons:
                self.add_button(button)
        else:
            self.buttons = {}
            self.add_default_buttons()

        await self.goto_page(self.current_page, interaction=interaction)
        

    def add_default_buttons(self):
        default_buttons = [
            RNBPaginatorButton(
                "first",
                emoji=get_emoji("first"),
                style=discord.ButtonStyle.gray,
                row=self.default_button_row + 1,
            ),
            RNBPaginatorButton(
                "prev10",
                label="10",
                emoji=get_emoji("prev_bulk"),
                style=discord.ButtonStyle.blurple,
                loop_label="↪",
                row=self.default_button_row,
            ),
            RNBPaginatorButton(
                "prev",
                emoji=get_emoji("prev"),
                style=discord.ButtonStyle.blurple,
                loop_label="↪",
                row=self.default_button_row,
            ),
            RNBPaginatorButton(
                "page_indicator",
                style=discord.ButtonStyle.gray,
                disabled=True,
                row=self.default_button_row,
            ),
            RNBPaginatorButton(
                "next",
                emoji=get_emoji("next"),
                style=discord.ButtonStyle.blurple,
                loop_label="↩",
                row=self.default_button_row,
            ),
            RNBPaginatorButton(
                "next10",
                label="10",
                emoji=get_emoji("next_bulk"),
                style=discord.ButtonStyle.blurple,
                loop_label="↩",
                row=self.default_button_row,
            ),
            RNBPaginatorButton(
                "last",
                emoji=get_emoji("last"),
                style=discord.ButtonStyle.gray,
                row=self.default_button_row + 1,
            ),
            RNBPaginatorButton(
                "random",
                emoji=get_emoji("random"),
                style=discord.ButtonStyle.gray,
                row=self.default_button_row + 1,
            ),
        ]
        for button in default_buttons:
            self.add_button(button)

