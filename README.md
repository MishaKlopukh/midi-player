# midi-player
Python launcher of animated MIDI player by @cifkao &amp; Magenta


# Installation

```
!pip install midi-player
```

# Usage

Intended (and only used with) Jupyter Notebooks & Colab: 
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
wandb.log(wandb.Html(mp.html))
wandb.finish()

```

See `examples/` for more.
