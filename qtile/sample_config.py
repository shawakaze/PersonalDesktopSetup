###############################################
#   dt inspired muzo mod                      #
###############################################

import os,re,socket,subprocess
import fontawesome as fa

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen, Match
from libqtile.lazy import lazy

from libqtile.dgroups import simple_key_binder

mod = "mod4"

terminal = "urxvt -e tmux -u"
#terminal = "cool-retro-term"

keys = [

    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down(),
        desc="Move focus down in stack pane"),
    Key([mod], "j", lazy.layout.up(),
        desc="Move focus up in stack pane"),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down(),
        desc="Move window down in current stack "),
    Key([mod, "control"], "j", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "),

    # Switch window focus to other pane(s) of stack
    Key([mod], "Tab", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),

    # Switch window focus to float
    Key([mod], "f", lazy.window.toggle_floating(),
        desc="Switch window focus to floating"),


    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Swap panes of split stack"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # Multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),

    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

group_names = [(fa.icons['terminal'], {'layout': 'max'}),
               (fa.icons['google'], {'layout': 'max','matches':[Match(wm_class=["firefox","Chromium"])]}),
               (fa.icons['book'], {'layout': 'max','matches':[Match(wm_class=["TeXstudio","Texmaker"])]}),
               (fa.icons['file-pdf'], {'layout': 'max','matches':[Match(wm_class=["Evince"])]}),
               (fa.icons['film'], {'layout': 'max','matches':[Match(wm_class=["vlc","mplayer"])]}), 
               (fa.icons['cogs'], {'layout': 'max','matches':[Match(wm_class=["Code"])]}),
               (fa.icons['beer'], {'layout': 'MonadTall'}),
               (fa.icons['mask'], {'layout': 'max','matches':[Match(wm_class=["Opera"])]}),
	       (fa.icons['gamepad'], {'layout':'max','matches':[Match(wm_class=["Steam","0ad"])]})
                ]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

#-------------------------------------------------
# #0fc0fc is a sky blue
# #0997b3 is cyan closer to the default powerline status color
# #008b8b is a teal
# #7851a9 is royal purple
#_________________________________________________

fg_col = "#cecece"
bg_col = "#2e2e2e"

# dark background
colors = [[bg_col, bg_col], # panel background ; originally #292dd3e 
          [bg_col, bg_col], # background for current screen tab ; originally #434758
          [fg_col, fg_col], # font color for group names ; originally #ffffff ; 0fc0fc is my bluest fav
          [fg_col, fg_col], # border line color for current tab ; OG #ff5555
          [bg_col, bg_col], # border line color for other tab and odd widgets ; OG #8d62a9
          ["#668bd7", "#668bd7"], # color for the even widgets
          ["#000000", "#000000"]] # window name


# layout_theme
layout_theme = {
                "margin": 1,
                "border_focus": fg_col,
                "border_normal": bg_col,
                "border_width" : 0
                }
layouts = [
    layout.Max(**layout_theme),
#    layout.Stack(num_stacks=2,margin=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
#    layout.Columns(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
#    layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font='Iosevka Nerd Font Mono',
#    font='TerminessTTF Nerd Font',
    fontsize=14,
    padding=2,
    background=colors[0]
)
extension_defaults = widget_defaults.copy()

##### network icons hack ########
net_dw = fa.icons['angle-double-down']
net_up = fa.icons['angle-double-up']

###############################

screens = [
    Screen(
     top=bar.Bar(
            [  
              widget.GroupBox(
                       font = "Font Awesome 5 Free",
                       fontsize = 15,
                       margin_y = 3,
                       margin_x = 3,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[2],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[3],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[0],
                       other_screen_border = colors[0],
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Spacer(length=100),
              widget.Prompt(
                       padding = 0,
                       foreground = colors[2], 
                       record_history = True
                        ),
              widget.Spacer(),
              # widget.Mpd2(
             #           host = 'localhost',
              #          port = 6600,
               #         status_format = '{play_status} {artist} - {title}',
                #        background = colors[0],
                 #       foreground = colors[2],
                  #      padding = 2
                   #     ),
              # widget.Spacer(), 
              widget.TextBox(
                        font = "Font Awesome 5 Free",
                        fontsize = 15,
                        text = net_dw,
                        foreground = colors[2],
                        background = colors[0],
                        padding = 5
                        ),              
              widget.Net(
                       interface = "enp3s0",                 
                       format = '{down}',
                       foreground = colors[2],
                       background = colors[0],
                       padding = 6
                       ),   
             widget.TextBox(
                        font = "Font Awesome 5 Free",
                        fontsize = 15,
                        text = net_up,
                        foreground = colors[2],
                        background = colors[0],
                        padding = 5
                        ),
              widget.Net(
                       interface = "enp3s0",
                       format = '{up}',
                       foreground = colors[2],
                       background = colors[0],
                       padding = 2
                       ),
              widget.Spacer(length=25),
              widget.TextBox(
                        font = "Font Awesome 5 Free",
                        fontsize = 15,
                        text = fa.icons['moon'],
                        foreground = colors[2],
                        background = colors[0],
                        padding = 2
                        ),
              widget.Clock(
                       foreground = colors[2],
                       background = colors[0],
                       format ="%A, %B %d",
                       padding = 2
                       ),
              widget.Spacer(length=10),
              widget.TextBox(
                        font = "Font Awesome 5 Free",
                        fontsize = 15,
                        text = fa.icons['clock'],
                        foreground = colors[2],
                        background = colors[0],
                        padding = 2
                        ),
             widget.Clock(
                       foreground = colors[2],
                       background = colors[0],
                       format ="%H:%M",
                       padding = 2
                       ),
             widget.Spacer(length=50),
             widget.Systray(
                       padding = 10,
                       background = colors[0]
                       )          
            ],
            30,  
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])



follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
#wmname = "LG3D"



wmname = "Qtile: L33T Edition"
