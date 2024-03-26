# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Custom imports
from colors import EVERFOREST
# from unicodes import *
from battery import get_battery_icon
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import RectDecoration
import os
import subprocess

mod = "mod4"
terminal = guess_terminal()

# Custom methods
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Multimedia keys
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +3%"), desc="Raise brightness level by 3%"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 3-%"), desc="Lower brightness level by 3%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 3%+"), desc="Raise volume level by 3%"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 3%-"), desc="Lower volume level by 3%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), desc="Mute or unmute volume level"),

    # CustomLaunchers
    Key([mod], "p", lazy.spawn("rofi -show drun"), desc="Launch rofi"),

]

# groups = [Group(i) for i in "123456789"]

groups = [
    Group("1", label="一"),
    Group("2", label="二"),
    Group("3", label="三"),
    Group("4", label="四"),
    Group("5", label="五"),
    Group("6", label="六"),
    Group("7", label="七"),
    Group("8", label="八"),
    Group("9", label="九"),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        # border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_normal=EVERFOREST["dark-gray-0"],
        border_focus=EVERFOREST["red"],
        border_width=3,
        border_on_single=True,
        margin=10
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Mononoki nerd font",
    fontsize=20,
    padding=5,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    # padding_y = 2,
                    # padding_x = 3,
                    borderwidth=0,
                    disable_drag=True,
                    # fontsize=24,
                    active=EVERFOREST["orange"],
                    inactive=EVERFOREST["dark-gray-0"],
                    rounded=False,
                    highlight_method="block",
                    this_current_screen_border=EVERFOREST["green"],
                    # foreground = EVERFOREST["orange"],
                    # background=EVERFOREST["bg3"],
                    block_highlight_text_color=EVERFOREST["bg3"]
                ),
                widget.Sep(
                    linewidth=1,
                    # padding = 5,
                    foreground=EVERFOREST["green"],
                    # background=EVERFOREST["bg3"]
                ),
                widget.Prompt(
                    background=EVERFOREST["bg3"],
                    foreground=EVERFOREST["fg"]
                ),
                widget.WindowName(
                    foreground=EVERFOREST["fg"],
                    # background=EVERFOREST["bg3"]
                ),
                # widget.Net(
                #     foreground = EVERFOREST["red"],
                #     background = EVERFOREST["bg3"],
                #     format = '{down} ↓↑ {up}',
                #     interface = 'enp62s0',
                #     decorations = [
                #         RectDecoration (
                #             colour = "#212121",
                #             padding_y = 3,
                #             radius = 2,
                #             filled = True
                #             ),
                #         ],
                # ),
                widget.CPU(
                    # background=EVERFOREST["bg3"],
                    foreground=EVERFOREST["purple"],
                    # decorations = [
                    #     RectDecoration (
                    #         # colour = "#212121",
                    #         padding_y = 10,
                    #         radius = 50,
                    #         filled = True
                    #     ),
                    # ],
                    format=" {load_percent}%",
                    # margin=200
                ),
                widget.Spacer(
                    length=5
                ),
                widget.Memory(
                    measure_mem='G',
                    foreground=EVERFOREST["yellow"],
                    # background=EVERFOREST["yellow"],
                    format="{MemUsed: .2f}{mm}/{MemTotal: .2f}{mm}",
                    # decorations = [
                    #     RectDecoration (
                    #         colour = "#88c0d0",
                    #         padding_y = 3,
                    #         radius = 2,
                    #         filled = True
                    #     ),
                    # ],
                ),
                widget.Spacer(
                                    length=5
                                ),
                widget.Battery(
                    foreground=EVERFOREST["green"],
                    # background=EVERFOREST["green"],
                    format="{char} {percent:2.0%}",
                    low_background=EVERFOREST["bg"],
                    low_foreground=EVERFOREST["red"],
                    notify_below=10,
                    discharge_char="󱟤",
                    empty_char="󰂎",
                    charge_char="󰂄",
                    full_char="󰁹"
                ),
                widget.Spacer(
                                    length=5
                                ),
                widget.Volume(
                    foreground=EVERFOREST["aqua"],
                    # background=EVERFOREST["orange"],
                    # emoji=True,
                    # emoji_list=[ "󰖁 ", " 󰕿 ", " 󰖀 ", " 󰕾 "]
                ),
                widget.Spacer(
                    length=5
                ),
                widget.Clock(
                    foreground=EVERFOREST["red"],
                    # background=EVERFOREST["red"],
                    format=" %d/%m/%Y",
                    # decorations = [
                    #     RectDecoration (
                    #         colour = "#81a1c1",
                    #         padding_y = 3,
                    #         radius = 2,
                    #         filled = True
                    #     ),
                    # ],
                ),
                widget.Spacer(
                    length=5
                ),
                widget.Clock(
                    foreground=EVERFOREST["blue"],
                    # background=EVERFOREST["blue"],
                    format=" %I:%M %p",
                    # decorations = [
                    #     RectDecoration (
                    #         colour = "#81a1c1",
                    #         padding_y = 3,
                    #         radius = 2,
                    #         filled = True
                    #     ),
                    # ],
                ),
                # # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # # widget.StatusNotifier(),
                widget.Systray(),
            ],
            size=30,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            border_color=["ff00ff", "000000", "ff00ff", "000000"],  # Borders are magenta
            background=EVERFOREST["bg1"],
            margin=10,
            opacity=0.9
        ),
        wallpaper="~/Pictures/wallpapers/everforest/undefined - Imgur.png",
        wallpaper_mode="fill"
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    border_normal=EVERFOREST["dark-gray-0"],
    border_focus=EVERFOREST["purple"],
    border_width=3,
    border_on_single=True,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
