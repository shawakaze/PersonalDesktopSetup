#!/bin/bash

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}



#starting utility applications at boot time
lxsession &
run nm-applet &
run pamac-tray &
#run pasystray &
numlockx on &
#blueman-applet &
#run flameshot &
#picom --config $HOME/.config/picom/picom.conf &
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
dunst &
#feh --randomize --bg-fill /usr/share/wallpapers/garuda-wallpapers/*
#starting user applications at boot time
run volctl &
#run discord &
#nitrogen --random --set-zoom-fill &
nitrogen --restore &
#run caffeine -a &
#run vivaldi-stable &
#(sleep 5 &&  run firefox) &
#(sleep 10 && run thunderbird) &
#run thunar &
(sleep 15 && run dropbox) &
(sleep 2 && run mpd) &
#(sleep 30 && run vlc)&
#run insync start &
#run spotify &
#run atom &
#run telegram-desktop &
