
from html import escape
import json
import os
import base64
from .stylers import basic, general, cifka_advanced, default_soundfont
from functools import partial
try:
    from mido import MidiFile
except ModuleNotFoundError:
    MidiFile = type(None)
    import io
try:
    from pretty_midi import PrettyMIDI
    import tempfile
except ModuleNotFoundError:
    PrettyMIDI = type(None)

class MIDIPlayer:
    """
    Jupyter-displayable MIDI player that also works on Colab, WandB.
    Supports local MIDI file and/or web-hosted MIDI file via url
    From some original code from Tony Hirsh: https://blog.ouseful.info/2021/11/24/fragment-embedding-srcdoc-iframes-in-jupyter-notebooks/
    Modified by Scott H. Hawley @drscotthawley
    Modified by Misha Klopukh
    """
    def __init__(self,
        url_or_file,            # url or local filename
        height,                 # Required arg because reasons
        width='100%',
        styler=general,         # optional callback for generating player HTML
        viz_type="piano-roll",  # piano-roll, waterfall, staff, None
        title="",               # optional title/header
        dl=True,                # include a "Download MIDI" link
        debug=False,
        player_html_maker=None, # backward-compatible duplicate of 'styler' [deprecated]
        soundfont=default_soundfont,
        ):
        self.width, self.height, self.viz_type, self.dl, self.debug, self.soundfont, self.styler = width, height, viz_type, dl, debug, soundfont, styler
        self.title = "&nbsp;" if title=="" else title
        if player_html_maker is not None: #backward compatibility, override styler
            raise DeprecationWarning("player_html_maker is deprecated; use styler instead")
            self.styler = player_html_maker  
        self.html = self.to_player_html(url_or_file, styler=self.styler)
        #self.url = url_or_file  # for later, will point to external file or data url

    def _repr_html_(self, **kwargs):
        """The part that displays the MIDIPlayer in a Jupyter notebook."""
        return f'''<iframe srcdoc="{escape(self.html)}" width="{self.width}" height="{self.height}"
            style="border:none !important;"
            "allowfullscreen" "webkitallowfullscreen" "mozallowfullscreen">'
            </iframe>'''

    def to_player_html(self, url_or_file, styler=None):
        styler = styler or self.styler or basic
        if isinstance(url_or_file, PrettyMIDI):
            with tempfile.NamedTemporaryFile('rb') as f:
                url_or_file.write(f.name)
                encoded_string = base64.b64encode(f.read())
            self.url ='data:audio/midi;base64,'+encoded_string.decode('utf-8')
        elif isinstance(url_or_file, MidiFile):
            with io.BytesIO() as f:
                url_or_file.save(file=f)
                encoded_string = base64.b64encode(f.getvalue())
            self.url ='data:audio/midi;base64,'+encoded_string.decode('utf-8')
        elif os.path.isfile(url_or_file): # if url_or_file points to local file, convert file to data url
            self.url = self.to_data_url(url_or_file)
        else: 
            self.url = url_or_file
        return styler(self.url, viz_type=self.viz_type, dl=self.dl, title=self.title, soundfont=self.soundfont)

    def to_data_url(self, midi_filename):  # this is crucial for Colab/WandB support
        with open(midi_filename, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        return 'data:audio/midi;base64,'+encoded_string.decode('utf-8')

    def toJson(self):  # some things want JSON
        return json.dumps(self, default=lambda o: o.__dict__)

    def __getitem__(self, idx, **kwargs): # probly not needed but here anyway
        return self.html[idx]

