# HSTP

*HTTP System for Transfer of Podcasts*

[Github Repository](https://github.com/URN/hstp)

VERSION 1.0

## Motivation

I want a standardised way to store podcasts for my radio station (University Radio Nottingham), to move away from the existing audioboom setup. This allows us to store podcasts as static files on a system similar to amazon S3 or azure blobs, reducing overhead costs and making long term archiving easier.

## File Structure (Output)

All json files should contain the following fields:

-   `generated` - ISO8601 compatible date-time from when the json file
    was generated
-   `generator` - The name of the program generating the json file
-   `comments` - Any notes, warnings or errors from the generator
-   `version` - version of the hstp standard to use (as string). Standards will be backwards compatible, but not necessarily forwards compatible (a valid 1.0 HSTP file tree should be valid for all future versions, but a valid HSTP 2.0 tree need not be valid 1.0, and a HSTP 1.0 reader should not attempt to read it)

## Podcasts Root - `/hstp.json`

-   podcasts - JSON array of objects for each podcast. They should be
    ordered by last-updated (most recent first)

    -   `name` - The human-readable name of the podcast. (eg `Holmes' Crime Hour`)
    -   `slug` - The url slug of the podcast. It should consist only of lowecase letters and hypen (eg `holmes-crime-hour`)
    -   `episode-count` - The number of episodes in the series.
    -   `first-episode` - ISO8601 compatible date-time from when the first episode was added.
    -   `last-updated` - ISO8601 compatible date-time from when the latest episode was added.

## Podcast Info - `/holmes-crime-hour.json`

The file name for the podcast should be the `slug` for the podcast
listed in the `htsp.json` file.

JSON Fields:

-   `name` - The human-readable name of the podcast. (eg `Holmes' Crime Hour`)
-   `slug` - The url slug of the podcast. It should consist only of lowecase letters and hypen (eg "holmes-crime-hour")
-   `description` - plain-text formatted description of the podcast.
-   `episodes` - JSON array of objects for each episode. They should be ordered by date (most recent first)
    -   `name` - The name of the podcast episode (eg `The Adventures of the Engineer's Thumb`)
    -   `slug` - The url slug of the podcast. It should consist only of lowecase letters, numbers and hypens (eg `adventures-engineers-thumb`)
    -   `description` - plain-text formatted description of the podcast episode (optional)
    -   `date` - ISO8601 compatible date-time from when the episode was added.
-   `first-episode` - ISO8601 compatible date-time from when the first episode was added.
-   `last-updated` - ISO8601 compatible date-time from when the latest episode was added.

## Images & Media Files

-   Podcast Thumbnail (required) - The thumbnail for the podcast, it should be `/holmes-crime-hour.jpg` (note the lowercase extension)
-   Episode Thumbnail (optional) - The thumbnail for the podcast, it should be `/holmes-crime-hour/adventures-engineers-thumb.jpg` (note the lowercase extension). If the thumbnail is not provided, the default for the podcast should be used.
-   Episode Media (required) - The Media for the podcast, as a high-quality MP3 file. it should be `/holmes-crime-hour/adventures-engineers-thumb.mp3` (note the lowercase extension)

## RSS Feeds

RSS feeds are required should be generated at build-time by the program, but can be easily constructed from the file tree.

## Specification

A copy of this specification should be included in the output directory as `htsp.md`. While not mandatory, it is reccommended, so future implelenters can view the documentation in the event that this repository no longer exists.

## Example

-   `hstp.json`
-   `htsp.md`
-   `holmes-crime-hour.json`
-   `holmes-crime-hour.jpg`
-   `holmes-crime-hour/`
    -   `adventures-engineers-thumb.jpg`
    -   `adventures-engineers-thumb.mp3`
    -   `study-in-scarlet.mp3`
    -   `valley-of-fear.jpg`
    -   `valley-of-fear.mp3`

## HSTP Serialisation Toolkit & Publisher

This is the python codebase included in the repository.

the command `hstp` 

### Input file format

-   `hstp_root.txt` - contains a list of podcasts to ignore (if any)
    -   `podcast_slug/`
        -   `image.jpg` - Thumbnail for the podcast
        -   `podcast.txt` - Description of the podcast
            -   The first line is read as the title
            -   Subsequent lines will be read from the file as its desciption
        -   `episode_slug/`
             -   `episode.txt` - Description for the podcast
                 -   The first line is read as the title
                 -   The second line is read as the date. If it is not there, it will source if from the the created date from the MP3 file
                 -   Subsequent lines will be read from the file as its desciption
             -   `audio.mp3` - The audio of the podcast
             -   `image.jpg` - (Optional) icon for the podcast     
