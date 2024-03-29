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

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Custom imports
from colors import CATPPUCCIN
# from unicodes import *
# from battery import get_battery_icon
# from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras import widget
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
    Key([mod], "l", lazy.spawn("powermenu"), desc="Launch powermenu"),
    Key([mod], "w", lazy.spawn("rofi-wifi-menu"), desc="Launch wifimenu"),


]

groups = [Group(i) for i in "123456789"]

# groups = [
#     Group("1", label="一"),
#     Group("2", label="二"),
#     Group("3", label="三"),
#     Group("4", label="四"),
#     Group("5", label="五"),
#     Group("6", label="六"),
#     Group("7", label="七"),
#     Group("8", label="八"),
#     Group("9", label="九"),
# ]

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

layout_theme = {
    "border_normal": CATPPUCCIN["dark-gray-0"],
    "border_focus": CATPPUCCIN["purple"],
    "border_width": 3,
    "border_on_single": True,
    "margin": 8
}
layouts = [
    layout.Columns(
        # border_focus_stack=["#d75f5f", "#8f3d3d"],
        **layout_theme
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
    font="Jetbrainsmono nerd font bold",
    fontsize=21, # Icon size
    padding=5,
    foreground=CATPPUCCIN["bg"],
)

DEFAULT_TEXT_FONT_SIZE = 17
DEFAULT_SPACER_LENGTH = 15
RECT_DECORATION_RADIUS = 10
extension_defaults = widget_defaults.copy()

def generate_default_rect_decorations(color) -> list:
    return [
        RectDecoration(
            colour=CATPPUCCIN[color],
            radius=RECT_DECORATION_RADIUS,
            filled=True,
            group=True,
            padding_y=4
        )
    ]

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="Jetbrainsmono nerd font",
                    borderwidth=0,
                    fontsize=19,
                    padding_x=15,
                    disable_drag=True,
                    # hide_unused=True,
                    active=CATPPUCCIN["pink"], # Active workspaces text color
                    rounded=True,
                    highlight_method="block",
                    this_current_screen_border=CATPPUCCIN["green"], # underLine color
                    block_highlight_text_color=CATPPUCCIN["bg"], # Highlighted text color
                ),
                widget.Sep(
                    linewidth=1,
                    foreground=CATPPUCCIN["green"],
                ),
                widget.Prompt(
                    # background=CATPPUCCIN["bg3"],
                    fontsize=DEFAULT_TEXT_FONT_SIZE,
                ),
                widget.WindowName(
                    # font="Jetbrainsmono nerd font",
                    fontsize=DEFAULT_TEXT_FONT_SIZE,
                    foreground=CATPPUCCIN["fg"],
                ),
                widget.Spacer(
                    length=5
                ),
                widget.TextBox(
                    text="",
                    # background=CATPPUCCIN["orange"],
                    decorations=generate_default_rect_decorations("orange")
                ),
                widget.Memory(
                    # background=CATPPUCCIN["orange"],
                    fontsize=DEFAULT_TEXT_FONT_SIZE,
                    measure_mem='G',
                    format="{MemUsed:.2f}{mm} / {MemTotal:.2f}{mm}",
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn("alacritty -e htop")
                    },
                    decorations=generate_default_rect_decorations("orange")
                ),
                widget.Spacer(
                    length=DEFAULT_SPACER_LENGTH
                ),
                widget.Battery(
                    fontsize=DEFAULT_TEXT_FONT_SIZE,
                    format="{char} {percent:2.0%}",
                    low_background=CATPPUCCIN["bg"],
                    low_foreground=CATPPUCCIN["red"],
                    notify_below=10,
                    discharge_char="󱟤",
                    empty_char="󰂎",
                    charge_char="󰂄",
                    full_char="󰁹",
                    decorations=generate_default_rect_decorations("green")
                ),
                widget.Spacer(
                    length=DEFAULT_SPACER_LENGTH
                ),
                widget.TextBox(
                    text="󰕾",
                    decorations=generate_default_rect_decorations("red")
                ),
                widget.Volume(
                    fontsize=DEFAULT_TEXT_FONT_SIZE,
                    decorations=generate_default_rect_decorations("red")
                ),
                widget.Spacer(
                    length=DEFAULT_SPACER_LENGTH
                ),
                widget.TextBox(
                    text="󰤨 ",
                    decorations=generate_default_rect_decorations("purple"),
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn("rofi-wifi-menu")
                    }
                    # fontsize=19,
                ),
                widget.GenPollCommand(
                    decorations=generate_default_rect_decorations("purple"),
                    cmd="nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d ':' -f 2",
                    shell=True,
                    update_interval=10,
                    fontsize=DEFAULT_TEXT_FONT_SIZE,
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn("rofi-wifi-menu")
                    }
                ),
                widget.Spacer(
                    length=DEFAULT_SPACER_LENGTH
                ),
                widget.Sep(
                    # length=DEFAULT_SPACER_LENGTH
                    foreground=CATPPUCCIN["fg"]
                ),
                widget.CheckUpdates(
                    distro="Fedora",
                    display_format="\ueb9a {updates} available",
                    no_update_string="\ueaa2 0",
                    colour_have_updates=CATPPUCCIN["red"],
                    colour_no_updates=CATPPUCCIN["green"],
                    update_interval=60,
                    padding=8,
                    fontsize=DEFAULT_TEXT_FONT_SIZE,
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn("alacritty -e sudo dnf update")
                    }
                ),
                widget.Sep(
                    foreground=CATPPUCCIN["fg"]
                ),
                widget.TextBox(
                    text="󰥔",
                    foreground=CATPPUCCIN["blue"],
                ),
                widget.Clock(
                    foreground=CATPPUCCIN["blue"],
                    # decorations=[
                    #     RectDecoration(
                    #         colour=CATPPUCCIN["blue"],
                    #         radius=RECT_DECORATION_RADIUS,
                    #         filled=True,
                    #         group=True,
                    #     )
                    # ],
                    fontsize=DEFAULT_TEXT_FONT_SIZE,
                    format="%I:%M %p ",
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn("gnome-calendar")
                    }
                ),
                widget.Sep(
                    foreground=CATPPUCCIN["fg"]
                ),
                widget.CurrentLayoutIcon(
                    fontsize=DEFAULT_TEXT_FONT_SIZE,
                    scale=0.5,
                ),
                widget.Spacer(
                    length=5
                ),
                # # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # # widget.StatusNotifier(),
                widget.Systray(),
            ],
            size=40,
            # border_width=[0, 2, 0, 2],  # Top right bottom left
            border_color=[CATPPUCCIN["orange"], CATPPUCCIN["orange"], CATPPUCCIN["orange"], CATPPUCCIN["orange"]],  # Borders are magenta
            background=CATPPUCCIN["bg"],
            margin=10,
            opacity=1
        ),
        # wallpaper="~/Pictures/wallpapers/everforest/undefined - Imgur.png",
        # wallpaper_mode="fill"
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
    border_normal=CATPPUCCIN["dark-gray-0"],
    border_focus=CATPPUCCIN["red"],
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
