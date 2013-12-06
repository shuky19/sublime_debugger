begin
  require 'debugger'
rescue LoadError
  puts "Debugger gem is not installed for this ruby version: #{RUBY_VERSION}"
  puts "please run 'gem install debugger' while using your default ruby version"
  exit
end

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
