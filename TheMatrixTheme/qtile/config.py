# mod of the original

import re
import socket
import os
import sys
import subprocess
import fontawesome as fa

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
#terminal = guess_terminal()
terminal = "urxvt -e tmux -u"

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
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

group_names = [(fa.icons['terminal'], {'layout': 'monadtall','matches':[Match(wm_class=["urxvt","URxvt"])]}),
               (fa.icons['firefox'], {'layout': 'max','matches':[Match(wm_class=["firefox","Chromium"])]}),
               (fa.icons['mailchimp'], {'layout': 'monadtall','matches':[Match(wm_class=["Thunderbird"])]}),
               (fa.icons['book'], {'layout': 'max','matches':[Match(wm_class=["TeXstudio","Texmaker"])]}),
               (fa.icons['file-pdf'], {'layout': 'max','matches':[Match(wm_class=["Evince"])]}),
               (fa.icons['film'], {'layout': 'monadtall','matches':[Match(wm_class=["vlc","smplayer"])]}), 
               (fa.icons['eye'], {'layout': 'monadtall'}),
               (fa.icons['opera'], {'layout': 'max','matches':[Match(wm_class=["Opera"])]}),
	       (fa.icons['gamepad'], {'layout':'monadtall','matches':[Match(wm_class=["Steam","0ad"])]})
                ]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group
##################################################################################################################

################# The Matrix #################
bg_kala = '#040904'
fg_kala = '#044b04'
volt = '#00ff41'
####################################################

monadtall_theme = dict(
        border_focus = volt,
        border_normal = bg_kala,
        border_width = 2,
        margin = 16
        )

layouts = [
    layout.Columns(border_focus_stack=["#859900", "#2aa198"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**monadtall_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font = 'OCRA',
    fontsize=12,
    padding=10,
    background = bg_kala,
    foreground = fg_kala
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(font = 'Font Awesome 5 Free', 
                    fontsize = 15, 
                    padding_x = 5,padding_y = 3, 
                    margin_x = 3, 
                    borderwidth = 1, 
                    active = volt, 
                    rounded = False, 
                    this_current_screen_border = volt, 
                    highlight_method = "line", highlight_color = bg_kala, 
                    background = bg_kala),
                widget.Spacer(length = 5),
                widget.Prompt(background = bg_kala, foreground = volt, prompt = 'open: '),
                widget.Spacer(length = 20),
                widget.Mpd2(foreground = volt, host = '127.0.0.1', port = 6601, status_format = ' {play_status} {artist} - {title}', update_interval = 1),
#                widget.Spacer(length = 15),
#                widget.NvidiaSensors(foreground = volt, fmt = 'GPU Temp : {}', update_interval = 2),
                widget.Spacer(length = 20),
                ####
                widget.OpenWeather(foreground = volt, app_key = '3bbca9935bdd06f3a56f955c4a70fba1',cityid = '909137', padding = 5),
                widget.Spacer(length = 5),
                widget.Net(prefix = 'k', format = fa.icons['angle-double-down']+"{down}/s", update_interval = 1, foreground = volt),
                #widget.NetGraph(interface = 'enp0s20u2', bandwidth_type = 'down', graph_color = 'ceff00', start_pos = 'bottom', frequency = 1, border_color = bg_kala, border_width = 1),
                widget.Spacer(),
                widget.Systray(),
                widget.Clock(format="%a %H:%M", foreground = volt),
                
            ],
            30, opacity=0.6,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color= "ceff00" #["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

follow_mouse_focus = True
bring_front_click = False
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
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "q-tile L33T"
