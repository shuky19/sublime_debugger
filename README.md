# SublimeRubyDebugger
debugger plugin for interactive ruby and RoR debugging on Sublime Text.

![SublimeRubyDebugger](http://i.imgur.com/PwjudlY.png)

Based [Debugger gem](https://github.com/cldwalker/debugger) package by [Shuky chen](https://github.com/shuky19).

## Overview
* [First Steps](#first-steps)
* [Features](#features)
* [Soon](#soon)
* [Commands](#commands)
* [Installation](#installation)
* [Troubleshoot](#troubleshoot)
* [License](#license)
* [Todos](#todo)
* [Screen Shots](#screen-shots)


## First steps
In order to start debugging ruby or RoR applications all you need to do

is to [install](#installation) Debugger plugin and press on
<kbd>F6</kbd> or <kbd>Shift+F6</kbd> or <kbd>Alt+Shift+F6</kbd>

## Features
* Local debugging Ruby and RoR applications.
* Stepping up, down ,over and into while debugging (jumps and goto also available).
* Add watch expression and run immidiate code using the current program context.
* Monitoring on stack, threads, output and local variables in the program.
* Builtin rails support.
* Breakpoints, conditional breakpoints and temporary breakpoints (goto) support.
* Works on Sublime Text 3 (later version will work on both 2 and 3)
* MRI 1.9.3 support (using debugger gem).
* MRI 2.0.0 support (using my fork for byebug gem).
* Linux, Window, OSX support

## Soon
* Sublime 2 support
* Edit and remove watch expressions

## Commands
Here is a complete list of commands you can find Command Pallette under the `Debugger` namespace or in the menu under `Tools / Debugger`:

#### Start/Stop debugging session
* Start Debugging - <kbd>F6</kbd>
* Start Debugging Rails - <kbd>Shift+F6</kbd>
* Start Debugging (Current file) - <kbd>Alt+Shift+F6</kbd>
* Pause Debugger - <kbd>Alt+d, b</kbd>
* Stop Debugging - <kbd>Alt+d, k</kbd>

#### Breakpoints
* Toggle Breakpoint - <kbd>F9</kbd>
* Toggle Conditional Breakpoint - <kbd>Shift+F9</kbd>
* Clear Breakpoints - <kbd>Alt+Shift+F9</kbd>

#### Cursor control
* Step Over - <kbd>F10</kbd>
* Step Into - <kbd>F11</kbd>
* Step up -  - <kbd>Alt+d, u</kbd>
* Step down -  - <kbd>Alt+d, d</kbd>
* Continue - <kbd>F8</kbd>
* Run To Line (goto) - <kbd>ctrl+F10</kbd> or <kbd>⌘+F10</kbd>
* Jumo to line - <kbd>Ctrl+Shift+F10</kbd> or <kbd>⌘+Shift+F10</kbd>

#### Expressions commands
* Run expression (evaluate) - <kbd>F7</kbd>
* Add watch expression - <kbd>Alt+d, w</kbd>
* Send input (to stdin) - <kbd>Alt+d, i</kbd>

#### Layout commands
* Show debug windows - <kbd>Alt+l, s</kbd>
* Hide debug windows - <kbd>Alt+l, h</kbd>

## Installation

### Gem dependencies
#### Ruby 1.9.3
Run command ```gem install debugger```

#### Ruby 2.0.0
Run command ```gem install byebug --version '>=2.5.0'```

### Sublime Ruby Debugger

#### [Package Control](https://sublime.wbond.net/)
Execute __"Package Control: Install Package"__ in the Command Pallette to retrieve a list of available packages.
Search in the list and install package `Ruby Debugger`.

#### Git
Clone the repository by executing the following command in your Packages directory:
```git clone https://github.com/shuky19/sublime_debugger.git "Ruby Debugger"```

#### Download
Get the latest [source from GitHub](https://github.com/shuky19/sublime_debugger/archive/master.zip) and extract the source into your Packages directory
to a folder named "Ruby Debugger".


*__Note:__ You can locate your Packages directory in the menu under* `Preferences / Browse Packages...`


## Troubleshoot

#### Why do i get on the output window "Errno::EADDRINUSE: Address already in use - bind(2)"?
Thats because there is another process running on your OS who is using the port 8989/8990

Another option is that the last debugger process is still alive

## License

SublimeTextXdebug is released under the [MIT License](http://www.opensource.org/licenses/MIT).

## Todo

* Break point windows updates
* Set view cursor on debug cursor change
* Nice message when port is taken
* Document & Refacor
* Ruby 1.8.7 support

## Screen Shots

![SublimeRubyDebugger](http://i.imgur.com/PwjudlY.png)

![SublimeRubyDebugger](http://i.imgur.com/Ny6TjMU.png)

![SublimeRubyDebugger](http://i.imgur.com/TkKnrsL.png)

![SublimeRubyDebugger](http://i.imgur.com/nJQ9oTy.png)
