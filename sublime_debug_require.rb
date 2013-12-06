require 'debugger'

pid = Process.pid
at_exit {
  if $! and pid == Process.pid
    puts "Last exception: #{$!.inspect}"
    puts "Backtrace: \n#{$@}"
  end
}

Debugger.wait_connection = true
Debugger.start_remote "localhost"

debugger
