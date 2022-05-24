from embeds.data_embed import data_embed

formatting = {
    "PlayerEventId": {
        "name": "Event's id",
        "value": "```{value}```",
        "info": "The id of the event.",
        "inline": False
    },
    "CreatorPlayerId": {
        "name": "Host's user id",
        "value": "```{value}```",
        "info": "The unique user id of the event's host.",
        "inline": False
    },
    "ImageName": {
        "name": "Image's name",
        "value": "```{value}```",
        "info": "The event thumbnail's name on the API.",
        "inline": False
    },
    "RoomId": {
        "name": "Event's room's id",
        "value": "```{value}```",
        "info": "The id of the room the event is hosted in.",
        "inline": False
    },
    "SubRoomId": {
        "name": "Event's room's subroom's id",
        "value": "```{value}```",
        "info": "The id of the subroom the event is hosted in.",
        "inline": False
    },
    "ClubId": {
        "name": "Event's club's id",
        "value": "```{value}```",
        "info": "The id of the club the event is associated with.",
        "inline": False
    },
    "Name": {
        "name": "Name",
        "value": "```{value}```",
        "info": "The event's name.",
        "inline": False
    },
    "Description": {
        "name": "Description",
        "value": "```{value}```",
        "info": "The event's description.",
        "inline": False
    },
    "StartTime": {
        "name": "Event's start time",
        "value": "```{value}```",
        "info": "The time the event starts.",
        "inline": False
    },
    "EndTime": {
        "name": "Event's ending time",
        "value": "```{value}```",
        "info": "The time the event ends.",
        "inline": False
    },
    "AttendeeCount": {
        "name": "Attendees",
        "value": "```{value}```",
        "info": "The amount of people who will be attending.",
        "inline": False
    },
    "CreatorPlayerId": {
        "name": "Publisher's user id",
        "value": "```{value}```",
        "info": "The event's host's unique user id.",
        "inline": False
    },
    "State": {
        "name": "State",
        "value": "```{value}```",
        "info": "Unknown.",
        "inline": False
    },
    "Accessibility": {
        "name": "Privacy",
        "value": "```{value}```",
        "info": "Defines who is able to see the event.",
        "inline": False
    }
}

def event_data_embed(event_data, explanations=False):
    return data_embed(formatting, event_data, explanations)