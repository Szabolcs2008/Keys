# Keys
A simple program to play sounds when keyboard keys are pressed

## Usage
> Don't expect a great documentation, as english is not my first language

- Download a release, or the latest python file
- Run the downloaded file, the it will generate its config
- You can edit the config to customise almost everything

## Config
The defaut config:
```
{
  "sounds": {
    "examplesound1": {
      "press-sound": "sound/path/here",
      "release-sound": null
    },
    "examplesound2": {
      "press-sound": "sound/path/here",
      "release-sound": "sound/path/here"
    }
  },
  "keys": {
    "default": "examplesound1",
    "Key.space": "examplesound1",
    "Key.enter": [
      "examplesound1",
      "examplesound2"
    ]
  }
}
```
### Sounds
You can create multiple sounds in the `sounds` section. All sounds should have a `press-sound` and a `release-sound`. Set either of them to `null`, to disable it. This means that if you set `press-sound` to `null`, it will be completely ignored, and sound will only play on key release.
```
"sounds": {
  "example": {
    "press-sound": null
    "release-sound": "path/to/sound"
  }
}
```

### Keys
The program uses pynput, so it's key codes are used in the config.

If you want to bind a non special key, you can type in it's value, for example `s`, `)`, `/`.

For special keys, you need to use it's pynput representation. For example `Key.esc`, `Key.enter` (For all the keys, refer to pynput's docs)
