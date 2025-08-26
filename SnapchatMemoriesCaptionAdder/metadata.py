from dataclasses import dataclass
from datetime import datetime, tzinfo
from enum import StrEnum, auto
from typing import NamedTuple
from timezonefinderL import TimezoneFinder
import pytz
import logging

# Get the central logger
logger = logging.getLogger("__snap")

# Photo identifier
MID = str
tf = TimezoneFinder()

class MediaType(StrEnum):
    """The two types of media that can exist."""

    Image = auto()
    Video = auto()


class Location(NamedTuple):
    """Location where a photo was taken."""

    latitude: float
    longitude: float


@dataclass(frozen=True)
class Metadata:
    """Metadata for a Memories file."""

    date: datetime
    type: MediaType
    location: Location
    mid: MID


def make_local_metadata(m: Metadata, tz: tzinfo = None) -> Metadata:
    """Convert metadata to the given time zone or determine by lat/lon.

    If tz is provided, it takes priority. Otherwise, tries to find by lat/lon.
    Falls back to system local timezone if nothing is found.
    """
    local_date = None

    # If a timezone is explicitly given, use it
    if tz is not None:
        local_date = m.date.astimezone(tz)
    else:
        # Try to determine timezone from lat/lon
        tz_name = tf.timezone_at(lat=m.location.latitude, lng=m.location.longitude)
        if tz_name:
            local_tz = pytz.timezone(tz_name)
            local_date = m.date.astimezone(local_tz)
        else:
            # fallback: system local timezone
            local_date = m.date.astimezone()
            logger.warning(
                f"No timezone found for lat={m.location.latitude}, lon={m.location.longitude}. "
                f"Falling back to system local timezone."
            )

    return Metadata(local_date, m.type, m.location, m.mid)
