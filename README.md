# Paindrop

## Introduction

Paindrop is a command line utility that helps you export your pins from
[Pinboard](https://pinboard.in/) and import them into
[Raindrop](https://raindrop.io).

While Raindrop already supports importing Pinboard data just fine, it was
missing two things that were important to me:

- Support for public/private bookmarks.
- Support for an "unread" status.

So I wrote Paindrop to solve this particular problem for me. It works for
me. This might not work for you.

The solution for me is to use just two collections in Raindrop: one for
public bookmarks, one for private bookmarks. Pins that are marked as
"unread" are left with no collection (so the act of "marking read" will be
dropping it into either the Public or Private collection).

## Installing

### pipx

The package can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
$ pipx install paindrop
```

### Homebrew

The package is available via Homebrew. Use the following commands to install:

```sh
$ brew tap davep/homebrew
$ brew install paindrop
```

## Usage

### Getting ready to use

There's 3 things you need to do to use this importer:

#### Create public and private collections in Raindrop

In Raindrop create two collections, one will be the collection for public
pins, the other will be the one for private pins. You don't need to make the
public collection public just yet, but the idea is that you will at some
point in the future.

#### Get your Pinboard access token

You can find it [in your account
settings](https://pinboard.in/settings/password).

#### Generate a Raindrop access token

This is a little more involved in Raindrop, but not difficult. In your
account settings [go to
*Integrations*](https://app.raindrop.io/settings/integrations) and under the
*For Developers* heading click on `Create new app`. Give it a name (probably
*Paindrop* so you can remember what it was for). Accept the API terms and
guidelines and hit `Create`.

Now click on the newly-created application and towards the bottom of the
dialog that appears click on `Create test token`; say `ok` when asked. Copy
the token and keep it to hand as you'll need this too.

## Running an import

After you've done the above steps you're ready to import. Assuming you named
your public and private collections `Public` and `Private`, you can run the
command like this:

```sh
paindrop example:xxxxxxxxxxxxxxxxxxxx xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

where the first parameter is the Pinboard access token and the second the
Raindrop access token.

If all goes well, after a few moments, you the importer should finish and
you should find that all of your Pins have migrated to Raindrop, all public
pins are in the `Public` collection and all private pins are in the
`Private` collection. Any pins that were marked as unread will be
*Unsorted*.

Note that if you used different names for your public and private
collections you can pass those names to `paindrop` with the `--public` and
`--private` switches.

## Getting help

If you need help please feel free to [raise an
issue](https://github.com/davep/paindrop/issues).

[//]: # (README.md ends here)
