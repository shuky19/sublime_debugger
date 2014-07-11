# Sublime Ruby Debugger
A debugger plugin for interactive ruby and RoR debugging on Sublime Text.

![SublimeRubyDebugger](http://i.imgur.com/PwjudlY.png)

By [Shuky chen](https://github.com/shuky19), based on the [Debugger](https://github.com/cldwalker/debugger) and [Byebug](https://github.com/deivid-rodriguez/byebug) gems.

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
In order to start debugging ruby or RoR applications all you need to do is to
[install](#installation) Debugger plugin and press on <kbd>F6</kbd> or
<kbd>Shift+F6</kbd> or <kbd>Alt+Shift+F6</kbd>

## Features
* Local debugging in Ruby and RoR applications.
* Stepping up, down, over, and into while debugging (jumps and goto also available).
* Add watch expression and run immediate code using the current program context.
* Monitoring on stack, threads, output, and local variables in the program.
* Builtin rails support.
* Breakpoints, conditional breakpoints, and temporary breakpoints (goto) support.
* Works in Sublime Text 2 and 3.
* MRI 1.9.3 support (using debugger gem).
* MRI 2.0.0 support (using byebug gem).
* Linux, Window, OSX support

## Soon
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
* Step up - <kbd>Alt+d, u</kbd>
* Step down - <kbd>Alt+d, d</kbd>
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

Sublime Debugger relies on two seperate gems for diffirent ruby versions. For Ruby 1.9.3 you need the debugger gem, which can be installed using ```gem install debugger```, and for Ruby 2.0.0 you need the byebug gem, which can be installed using ```gem install byebug```.

### Unsupported ruby versions

I cannot test this against all ruby versions, so I only explicity support Ruby 1.9.3 and Ruby 2.0.0. [RVM](https://wiki.archlinux.org/index.php/RVM) is a good way to have multiple ruby versions installed at once and switch between them when debugging or running normally. Sublime Debugger will use the ruby version that you set as default, so you must set either Ruby 1.9.3 or Ruby 2.0.0 as the default. Remember to reinstall the byebug or debugger gem when you change ruby versions, or else you will get an ```Connection could not be made: [Errno ##] Connection refused``` error.

If you need to have your ruby program running with an unspported ruby version you can manually add the version to the supported versions list. In the package's directory, which you can get to by going to ```preferences -> browse packages``` in sublime text and then opening the ```Ruby Debugger``` folder, there is a ```ruby_version_discoverer.rb``` file where you can add your ruby version.

### Sublime Ruby Debugger

#### [Package Control](https://sublime.wbond.net/)
Execute __"Package Control: Install Package"__ in the Command Pallette to retrieve a list of available packages.
Search in the list and install package `Ruby Debugger`.

#### Git
Clone the repository by executing the following command in your Packages directory:
```git clone https://github.com/shuky19/sublime_debugger.git "Ruby Debugger"```

#### Download
Get the latest [source from GitHub](https://github.com/shuky19/sublime_debugger/archive/master.zip) and extract the source into your Packages directory to a folder named "Ruby Debugger".


*__Note:__ You can locate your Packages directory in the menu under* `Preferences / Browse Packages...`


## Troubleshoot

#### Why do I get ```Connection could not be made: [Errno 61] Connection refused``` in the output window?

Well, Most of the reasons for this error come from environmental problems, following the steps below will help you fix it:

* Enable logging: preferences -> Package Settings -> Ruby Debugger -> Settings - Default (you can use User as well)
* Run you ruby on a shell and make sure it runs perfectly.
* From that shell run ```which ruby``` and ```ruby --version```
* Run the debugger and compare its output to yours
* Figure out whether your ruby path comes from a different ruby environment (rbenv | rvm | custom executable)
* Figure out whether your ruby default version is not set appropriately


#### Why do I get ```Errno::EADDRINUSE: Address already in use - bind(2)``` in the output window?
Either because there is another process running which is using ports 8989/8990 or the last debugger process is still alive (```killall ruby``` will solve that).

## License

RubyDebugger is released under the [MIT License](http://www.opensource.org/licenses/MIT).

## Todo

* Settings file
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
