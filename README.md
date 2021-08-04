# EraserMapper
Krita plugin that allows you to map specific brushe presets to a specified eraser preset while leaving intact the default eraser functionality for others.

## Installation
<a href="https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html#how-to-install-a-python-plugin">Please download the latest release and then follow the standard Krita plugin installation as described in the official documentation.</a>

## Usage
First, assign the shortcuts for the plugin by going to `Settings > Configure Krita...` from the menu. Then, go to `Keyboard Shortcuts` and find the shortcuts within the `Scripts > Eraser Mapper` section. You should overwrite your existing, native Eraser and Freehand Brush Tool presets with these. In other words, whatever you're currently using for those tools, make them these instead.<br>
Then, open the Eraser Mapper settings from the Scripts menu within Krita to configure the plugin.<br>
<p align="center"><img src="https://raw.githubusercontent.com/kevinmaddox/erasermapper/main/images/config-window.png" alt="Eraser Mapper configuration window"/></p>
Click the `Eraser Preset` image button to select which eraser preset you'd like to use as the primary eraser. Then, in the lists below, find any brushes you want to switch to that eraser preset and move them to the `Will Toggle Brush Preset` list. Finally, check or uncheck the `Enable same-key switching` box depending on the desired behavior. Same-key switching makes it so that, if you hit the eraser shortcut while in eraser mode, you'll be switched back to the last brush you were using. Otherwise, you'll have to hit your assigned Freehand Brush shortcut.

## Reasoning
Krita, unlike other art programs, does not provide an eraser tool. Rather, erasing is a blending mode toggle that allows you to paint with transparent pixels. This is great if you're painting, but not so great if you're drawing, especially if you're drawing with a thin brush. The typical workaround is to leverage the Ten Brushes plugin which comes installed with Krita, but the problem here is that transparent erasing and brush-preset erasing now must be bound to separate hotkeys. This is a normal paradigm in other programs, as most drawing software provides a way to paint with transparent pixels that exists separate from an eraser tool, so for most it's not an issue. Most probably won't even need or want to use both. For me, however, I wanted a way, utilizing the same shortcut key, to switch between those two types of erasing depending on the brush I'm using. That's the purpose behind this plugin.

## Known Bugs
This plugin has a bug which can be replicated via the following steps:
1. Select a brush preset you've mapped.
2. Select a brush preset you have NOT mapped.
3. Select the assigned eraser brush.
4. Press the assigned key for the Freehand Brush tool.
5. It will jump back to the brush selected in Step 1, as opposed to Step 2.
This occurs because I could not figure out a way to listen for changes to the Brush Presets docker. The Krita Python API does not seem to have a way to check if the user has changed their active brush preset, either. If anyone knows a way to do this, please contact me or submit a pull request. It's a minor bug, but any help will be much appreciated.