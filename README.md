# midi-player
Python launcher of the [`html-midi-player`](https://github.com/cifkao/html-midi-player) by [@cifkao](https://github.com/cifkao) &amp; [@magenta](https://github.com/magenta)

Works with local and web-hosted MIDI files in Jupyter, Colab, WandB,...probably other contexts. 

# Installation

```
pip install midi-player
```

# Usage

Only tested with Jupyter Notebooks & Colab, but uses no IPython dependencies so it *should* work in other contexts.
```python

from midi_player import MIDIPlayer
from midi_player.stylers import basic, cifka_advanced

midi_file_url = "https://magenta.github.io/magenta-js/music/demos/melody.mid"
midi_file = "data/test_midi.mid"

MIDIPlayer(midi_file_url, 400)  
MIDIPlayer(midi_file, 160, styler=cifka_advanced)
```

With `wandb`:
```python
import wandb

wandb.login()
wandb.init(project="midi-player")
mp = MIDIPlayer(midi_file, 300, viz_type="waterfall")
wandb.log({'player':wandb.Html(mp.html)})
wandb.finish()

```

See `examples/` for more.

# Documentation

TO-DO. Particularly, people will want to know how to add/customize their own "stylers". 
See `midi_player/*.py` for now ;-).

# Known Issues
* Not sure why the staff view is putting out 32nd notes / how to tell it to do 8th notes instead.
* If you need a "Download the MIDI" button, you may need to offer a separate way to do that. See [this Issue](https://github.com/cifkao/html-midi-player/issues/13) in the [`html-midi-player`](https://github.com/cifkao/html-midi-player) repo.

