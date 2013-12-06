require 'debugger'

pid = Process.pid
at_exit {
  if $! and pid == Process.pid
    puts "Last exception: #{$!.inspect}"
    puts "Backtrace: "
    puts "#{$@}"
  end
}

Debugger.wait_connection = true
Debugger.start_remote "127.0.0.1"

debugger
