from embeds.data_embed import data_embed

formatting = {
    "Id": {
        "name": "Id",
        "value": "```{value}```",
        "info": "Image's unique id. Based on total images shared.",
        "inline": False
    },
    "Type": {
        "name": "Type",
        "value": "```{value}```",
        "info": "Unknown!",
        "inline": False
    },
    "Accessibility": {
        "name": "Privacy",
        "value": "```{value}```",
        "info": "Defines who is able to see the image on RecNet.",
        "inline": False
    },
    "AccessibilityLocked": {
        "name": "Hidden",
        "value": "```{value}```",
        "info": "If true, then the post is only visible to the publisher and it can't be published.",
        "inline": False
    },
    "ImageName": {
        "name": "Image's name",
        "value": "```{value}```",
        "info": "The image's name on the API.",
        "inline": False
    },
    "Description": {
        "name": "Description",
        "value": "```{value}```",
        "info": "Image's RecNet post's description. An old, now unsupported feature.",
        "inline": False
    },
    "PlayerId": {
        "name": "Publisher's user id",
        "value": "```{value}```",
        "info": "The image's publisher's unique user id.",
        "inline": False
    },
    "TaggedPlayerIds": {
        "name": "Tagged users' id's",
        "value": "```{value}```",
        "info": "Id's of the users' who are tagged in the RecNet post.",
        "inline": False
    },
    "RoomId": {
        "name": "Image's room's id",
        "value": "```{value}```",
        "info": "The id of the room the image was taken in.",
        "inline": False
    },
    "PlayerEventId": {
        "name": "Image's event's id",
        "value": "```{value}```",
        "info": "The id of the event the image was taken in.",
        "inline": False
    },
    "CreatedAt": {
        "name": "Publish date",
        "value": "```{value}```",
        "info": "The date when the image was shared.",
        "inline": False
    },
    "CheerCount": {
        "name": "Cheers",
        "value": "```{value}```",
        "info": "The amount of cheers the RecNet post has.",
        "inline": False
    },
    "CommentCount": {
        "name": "Comments",
        "value": "```{value}```",
        "info": "The amount of comments the RecNet post has.",
        "inline": False
    }
}

def image_data_embed(image_data, explanations=False):
    return data_embed(formatting, image_data, explanations)